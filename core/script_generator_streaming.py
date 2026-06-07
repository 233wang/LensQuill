"""流式剧本生成器 - 大模型流式输出 + 后端SSE转发"""

from typing import List, Dict, Optional
from datetime import datetime
import json
import asyncio
import aiohttp


class StreamingScriptGenerator:
    """流式剧本生成器 - 使用大模型流式输出"""

    def __init__(self, llm_api=None):
        self.llm_api = llm_api

    async def generate_script_stream(self, chapters: List[Dict[str, str]], characters: List[Dict] = None):
        """
        流式生成剧本，逐章返回结果

        Yields:
            dict: SSE 格式的事件数据
        """
        # 1. 初始化
        yield {
            "type": "init",
            "message": "开始生成剧本...",
            "total_chapters": len(chapters)
        }

        # 2. 加载人物信息
        if characters:
            yield {
                "type": "characters_loaded",
                "count": len(characters),
                "characters": characters
            }
        else:
            # 使用关键词简单提取人物
            detected_characters = self._detect_characters(chapters)
            yield {
                "type": "characters_loaded",
                "count": len(detected_characters),
                "characters": detected_characters
            }
            characters = detected_characters

        # 3. 逐章处理
        for i, chapter in enumerate(chapters):
            chapter_index = i + 1
            chapter_title = chapter.get("title", f"第{chapter_index}章")

            yield {
                "type": "processing_chapter",
                "chapter_index": chapter_index,
                "chapter_title": chapter_title,
                "message": f"正在生成第 {chapter_index}/{len(chapters)} 章..."
            }

            try:
                # 实时流式生成章节
                async for event in self._generate_chapter_stream(chapter, chapter_index):
                    yield event

            except Exception as e:
                yield {
                    "type": "chapter_error",
                    "chapter_index": chapter_index,
                    "error": str(e)
                }

        # 4. 完成
        yield {
            "type": "complete",
            "message": "剧本生成完成！"
        }

    async def _generate_chapter_stream(self, chapter: Dict[str, str], chapter_index: int):
        """流式生成单个章节，实时推送生成进度"""
        if not self.llm_api:
            yield {"type": "chapter_complete", "chapter_index": chapter_index, "chapter": self._generate_fallback_chapter(chapter, chapter_index)}
            return

        prompt = self._build_chapter_prompt(chapter, chapter_index)

        # 收集流式输出
        full_content = ""
        async for chunk in self._call_llm_stream_async(prompt):
            full_content += chunk
            # 实时推送当前生成的文本（非完整 JSON）
            yield {
                "type": "chapter_streaming",
                "chapter_index": chapter_index,
                "content": full_content,
                "is_complete": False
            }

        # 流式结束后，解析完整 JSON
        chapter_script = self._parse_chapter_response(full_content, chapter_index)

        yield {
            "type": "chapter_complete",
            "chapter_index": chapter_index,
            "chapter": chapter_script
        }

    async def _call_llm_stream_async(self, prompt: str):
        """异步调用大模型流式输出"""
        import os
        from dotenv import load_dotenv
        load_dotenv()

        api_url = os.getenv("OPENAI_API_URL", "https://maas-api.cn-huabei-1.xf-yun.com/v2/chat/completions")
        api_key = os.getenv("OPENAI_API_KEY")
        model_id = os.getenv("OPENAI_MODEL_ID", "astron-code-latest")

        if not api_key:
            yield "【LLM API 未配置】"
            return

        request_data = {
            "model": model_id,
            "messages": [
                {"role": "system", "content": "你是一个专业的剧本创作助手。你生成的内容必须是有效的JSON格式。"},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 8192,
            "stream": True,
            "extra_body": {
                "response_format": {"type": "json_object"}
            }
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    api_url,
                    json=request_data,
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json"
                    },
                    timeout=aiohttp.ClientTimeout(total=120)
                ) as response:
                    async for line in response.content:
                        if line:
                            line_str = line.decode('utf-8')
                            if line_str.startswith('data:'):
                                data_str = line_str[5:].strip()
                                if data_str == '[DONE]':
                                    break
                                try:
                                    data = json.loads(data_str)
                                    if "choices" in data and len(data["choices"]) > 0:
                                        delta = data["choices"][0].get("delta", {})
                                        content = delta.get("content", "")
                                        if content:
                                            yield content
                                except (json.JSONDecodeError, UnicodeDecodeError):
                                    pass
        except Exception as e:
            print(f"API调用失败: {e}")
            yield f"【错误: {str(e)}】"

    def _detect_characters(self, chapters: List[Dict[str, str]]) -> List[Dict]:
        """简单人物检测"""
        import re
        seen_names = set()
        characters = []
        char_id = 1

        for chapter in chapters:
            content = chapter.get("content", "")
            words = re.findall(r'[一-龥]{2,3}(?:先生|小姐|女士|老师|同学|医生|警察|老板)', content)
            for name in words:
                clean_name = name.rstrip('先生小姐女士老师同学医生警察老板')
                if clean_name and clean_name not in seen_names and len(clean_name) <= 4:
                    seen_names.add(clean_name)
                    characters.append({
                        "id": f"char_{char_id:03d}",
                        "name": clean_name,
                        "role": "unknown",
                        "description": "",
                        "aliases": [],
                        "relationships": []
                    })
                    char_id += 1

        return characters

    def _build_chapter_prompt(self, chapter: Dict[str, str], chapter_index: int) -> str:
        """构建提示词"""
        return f"""你是一个专业的剧本创作助手。

【任务】将以下小说章节转换为结构化剧本格式。

【要求】
1. 保留原著的文学性和细节描写
2. 将叙述性内容转换为剧本格式（动作、对话、场景描述）
3. 合理划分场景和分镜，每个场景2-4个分镜
4. 严格输出 JSON 格式，不要包含任何额外解释或 Markdown 代码块

【JSON Schema】
{{
    "chapter_index": {chapter_index},
    "chapter_title": "字符串",
    "scenes": [
        {{
            "scene_index": 1,
            "scene_title": "字符串",
            "location": "字符串",
            "time": "字符串",
            "description": "字符串",
            "shots": [
                {{
                    "shot_index": 1,
                    "shot_type": "字符串",
                    "time_of_day": "字符串",
                    "camera_direction": "字符串",
                    "action": "字符串",
                    "dialogue": [
                        {{"character": "字符串", "line": "字符串", "action_description": "字符串"}}
                    ],
                    "effects": [],
                    "sound": []
                }}
            ]
        }}
    ]
}}

【输出要求】
- 直接输出 JSON 格式
- 所有文本使用中文
- 不要包含 ```json 或 ``` 等 Markdown 标记

【小说内容】
{chapter['title']}
{chapter['content']}
"""

    def _parse_chapter_response(self, response: str, chapter_index: int) -> Dict:
        """解析响应"""
        try:
            data = json.loads(response)
            data["chapter_index"] = chapter_index
            return data
        except json.JSONDecodeError as e:
            print(f"解析失败: {e}")
            return self._generate_fallback_chapter({}, chapter_index)

    def _generate_fallback_chapter(self, chapter: Dict[str, str], chapter_index: int) -> Dict:
        """降级处理"""
        return {
            "chapter_index": chapter_index,
            "chapter_title": chapter.get("title", f"第{chapter_index}章"),
            "scenes": [
                {
                    "scene_index": 1,
                    "scene_title": "场景1",
                    "location": "未知地点",
                    "time": "未知时间",
                    "description": chapter.get("content", "")[:200],
                    "shots": [
                        {
                            "shot_index": 1,
                            "shot_type": "内景",
                            "time_of_day": "白天",
                            "camera_direction": "中景",
                            "action": "",
                            "dialogue": [],
                            "effects": [],
                            "sound": []
                        }
                    ]
                }
            ]
        }

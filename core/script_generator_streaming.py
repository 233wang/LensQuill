"""剧本生成器 - 流式生成器，大模型流式输出 + 后端SSE转发"""

from typing import List, Dict, Optional
from datetime import datetime
import json
import asyncio


class StreamingScriptGenerator:
    """流式剧本生成器 - 按章节流式生成剧本"""

    def __init__(self, llm_api=None):
        """
        初始化流式剧本生成器

        Args:
            llm_api: LLM API 实例，用于智能生成
        """
        self.llm_api = llm_api

    async def generate_script_stream(self, chapters: List[Dict[str, str]], characters: List[Dict] = None):
        """
        流式生成剧本，逐章返回结果

        Args:
            chapters: 章节列表
            characters: 人物列表（可选）

        Yields:
            dict: SSE 格式的事件数据
        """
        # 1. 发送初始化信息
        yield {
            "type": "init",
            "message": "开始生成剧本...",
            "total_chapters": len(chapters)
        }

        # 2. 发送人物信息（如果有）
        if characters:
            yield {
                "type": "characters_loaded",
                "count": len(characters),
                "characters": characters
            }
        else:
            # 检测并加载人物
            yield {
                "type": "detecting_characters",
                "message": "正在识别角色..."
            }
            detected_characters = self._detect_characters(chapters)
            yield {
                "type": "characters_loaded",
                "count": len(detected_characters),
                "characters": detected_characters
            }
            characters = detected_characters

        # 3. 逐章生成剧本（使用大模型流式输出）
        script_chapters = []
        for i, chapter in enumerate(chapters):
            chapter_index = i + 1

            yield {
                "type": "processing_chapter",
                "chapter_index": chapter_index,
                "chapter_title": chapter.get("title", f"第{chapter_index}章"),
                "message": f"正在生成第 {chapter_index}/{len(chapters)} 章..."
            }

            try:
                # 使用大模型流式输出生成当前章节
                chapter_script = await self._generate_chapter_stream_async(chapter, chapter_index)

                yield {
                    "type": "chapter_complete",
                    "chapter_index": chapter_index,
                    "chapter": chapter_script
                }

                script_chapters.append(chapter_script)

            except Exception as e:
                yield {
                    "type": "chapter_error",
                    "chapter_index": chapter_index,
                    "error": str(e)
                }

        # 4. 发送完成信息
        yield {
            "type": "complete",
            "script": {
                "metadata": {
                    "version": "1.0",
                    "generated_by": "AI Tool v3.0 (Streaming)",
                    "generated_at": datetime.now().isoformat(),
                    "source_chapters": len(chapters),
                    "llm_model": self.llm_api.model_id if self.llm_api else "unknown"
                },
                "characters": characters,
                "chapters": script_chapters
            },
            "message": "剧本生成完成！"
        }

    async def _generate_chapter_stream_async(self, chapter: Dict[str, str], chapter_index: int) -> Dict:
        """
        异步流式生成单个章节的剧本
        从大模型流式接收数据，最后组合成完整的 JSON
        """
        if self.llm_api:
            prompt = self._build_chapter_prompt(chapter, chapter_index)

            # 收集流式输出的所有片段
            full_content = ""
            async for chunk in self.llm_api.call_llm_stream_async(prompt, use_json_mode=True, max_tokens=8192):
                full_content += chunk

            return self._parse_chapter_response(full_content)
        else:
            return self._generate_fallback_chapter(chapter, chapter_index)

    def _detect_characters(self, chapters: List[Dict[str, str]]) -> List[Dict]:
        """
        简单的人物检测（降级方案）
        """
        seen_names = set()
        characters = []
        char_id = 1

        for chapter in chapters:
            content = chapter.get("content", "")
            import re
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
        """构建章节剧本生成提示词"""
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

    def _parse_chapter_response(self, response: str) -> Dict:
        """解析章节响应"""
        try:
            data = json.loads(response)
            return data
        except json.JSONDecodeError as e:
            print(f"解析失败: {e}")
            return self._generate_fallback_chapter({}, 1)

    def _generate_fallback_chapter(self, chapter: Dict[str, str], chapter_index: int) -> Dict:
        """生成降级章节剧本"""
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

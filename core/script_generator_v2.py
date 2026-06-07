"""剧本生成器 v2 - 按章节整体生成剧本"""

from typing import List, Dict, Optional
from datetime import datetime
import json


class ScriptGeneratorV2:
    """剧本生成器类 v2 - 按章节整体生成"""

    def __init__(self, llm_api=None):
        """
        初始化剧本生成器

        Args:
            llm_api: LLM API 实例，用于智能生成
        """
        self.llm_api = llm_api

    def generate_script_from_chapter(self, chapter: Dict[str, str], chapter_index: int) -> Dict:
        """
        从单个章节生成剧本

        Args:
            chapter: 章节数据
            chapter_index: 章节索引

        Returns:
            剧本章节数据
        """
        if self.llm_api:
            # 使用 LLM 生成剧本
            prompt = self._build_chapter_prompt(chapter, chapter_index)
            response = self.llm_api.call_llm(prompt, use_json_mode=True)
            return self._parse_chapter_response(response)
        else:
            # 降级：生成基础结构
            return self._generate_fallback_chapter(chapter, chapter_index)

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
            # 尝试解析 JSON
            data = json.loads(response)
            return data
        except json.JSONDecodeError as e:
            print(f"解析失败: {e}")
            print(f"响应内容: {response[:500]}")
            return {}

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

    def convert_to_script_format(self, chapters: List[Dict[str, str]], characters: List[Dict] = None) -> Dict:
        """
        转换为完整剧本格式

        Args:
            chapters: 章节列表
            characters: 人物列表（可选）

        Returns:
            完整剧本对象
        """
        # 构建剧本结构
        script = {
            "metadata": {
                "version": "1.0",
                "generated_by": "AI Tool v2.0",
                "generated_at": datetime.now().isoformat(),
                "source_chapters": len(chapters),
                "llm_model": self.llm_api.model_id if self.llm_api else "unknown"
            },
            "characters": characters or [],
            "chapters": []
        }

        # 为每个章节生成剧本
        for i, chapter in enumerate(chapters):
            chapter_script = self.generate_script_from_chapter(chapter, i + 1)
            script["chapters"].append(chapter_script)

        return script

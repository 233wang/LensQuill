"""剧本生成器 v3 - 分块处理，不降级"""

from typing import List, Dict, Optional
from datetime import datetime
import json
import re


class ScriptGeneratorV3:
    """剧本生成器类 v3 - 分块处理，确保所有用户输入都能正常处理"""

    def __init__(self, llm_api=None):
        """
        初始化剧本生成器

        Args:
            llm_api: LLM API 实例，用于智能生成
        """
        self.llm_api = llm_api
        self.max_chunk_size = 15000  # 每个 chunk 最大字符数（留出提示词空间）

    def split_content_into_chunks(self, content: str, title: str) -> List[Dict[str, str]]:
        """
        将长内容分割成多个小块

        Args:
            content: 原始内容
            title: 章节标题

        Returns:
            分割后的块列表
        """
        if len(content) <= self.max_chunk_size:
            return [{"title": title, "content": content}]

        # 尝试按自然段落分割
        paragraphs = re.split(r'[\n\r]{2,}', content)
        chunks = []
        current_chunk = ""
        chunk_title = title

        for para in paragraphs:
            if len(current_chunk) + len(para) + 2 <= self.max_chunk_size:
                if current_chunk:
                    current_chunk += "\n\n" + para
                else:
                    current_chunk = para
            else:
                if current_chunk:
                    chunks.append({"title": chunk_title, "content": current_chunk})
                if len(para) > self.max_chunk_size:
                    # 单个段落太长，按句子分割
                    sentences = re.split(r'([。！？])', para)
                    temp_chunk = ""
                    for sent in sentences:
                        if len(temp_chunk) + len(sent) <= self.max_chunk_size:
                            temp_chunk += sent
                        else:
                            chunks.append({"title": chunk_title, "content": temp_chunk})
                            temp_chunk = sent
                    current_chunk = temp_chunk
                else:
                    current_chunk = para
                    chunk_title = f"{title} - 续"

        if current_chunk:
            chunks.append({"title": chunk_title, "content": current_chunk})

        return chunks

    def merge_script_chunks(self, chunks: List[Dict]) -> Dict:
        """
        合并多个脚本块

        Args:
            chunks: 脚本块列表

        Returns:
            合并后的完整脚本
        """
        if not chunks:
            return {}

        merged = {
            "chapter_index": chunks[0].get("chapter_index", 1),
            "chapter_title": chunks[0].get("chapter_title", "未知章节"),
            "scenes": [],
            "combined_from_chunks": len(chunks)
        }

        scene_id = 1
        for chunk in chunks:
            for scene in chunk.get("scenes", []):
                scene["scene_index"] = scene_id
                merged["scenes"].append(scene)
                scene_id += 1

        return merged

    def generate_script_from_chapter(self, chapter: Dict[str, str], chapter_index: int) -> Dict:
        """
        从单个章节生成剧本（支持长文本分块处理）

        Args:
            chapter: 章节数据
            chapter_index: 章节索引

        Returns:
            剧本章节数据
        """
        if not self.llm_api:
            raise ValueError("LLM API 未配置")

        # 分割长内容
        chunks = self.split_content_into_chunks(chapter["content"], chapter["title"])

        if len(chunks) == 1:
            # 内容较短，直接生成
            prompt = self._build_chapter_prompt(chapter, chapter_index)
            response = self.llm_api.call_llm(prompt, use_json_mode=True, max_tokens=8192)
            return self._parse_chapter_response(response, chapter_index)
        else:
            # 内容较长，分块处理
            return self._generate_chunked_script(chunks, chapter_index)

    def _generate_chunked_script(self, chunks: List[Dict], chapter_index: int) -> Dict:
        """
        分块生成脚本

        Args:
            chunks: 分割后的块
            chapter_index: 章节索引

        Returns:
            合并后的脚本
        """
        script_chunks = []

        for i, chunk in enumerate(chunks):
            # 构建提示词，告知这是分块处理
            prompt = f"""你是一个专业的剧本创作助手。

【任务】将以下小说内容转换为结构化剧本格式（这是分块处理的一部分）。

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

【小说内容 - 第 {i + 1} 部分】
{chunk['title']}
{chunk['content']}
"""

            response = self.llm_api.call_llm(prompt, use_json_mode=True, max_tokens=8192)
            script_chunk = self._parse_chapter_response(response, chapter_index)

            # 清理掉重复的元信息，只保留 scenes
            script_chunk = {
                "chapter_index": chapter_index,
                "chapter_title": chunks[0]["title"],
                "scenes": script_chunk.get("scenes", [])
            }

            script_chunks.append(script_chunk)

        return self.merge_script_chunks(script_chunks)

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

    def _parse_chapter_response(self, response: str, chapter_index: int) -> Dict:
        """解析章节响应"""
        try:
            data = json.loads(response)
            # 确保有正确的 chapter_index
            data["chapter_index"] = chapter_index
            return data
        except json.JSONDecodeError as e:
            print(f"解析失败: {e}")
            print(f"响应内容: {response[:500]}")
            raise ValueError(f"无法解析 LLM 响应: {str(e)}")

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
                "generated_by": "AI Tool v3.0 (Chunking)",
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

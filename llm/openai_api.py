"""LLM集成层 - OpenAI API集成（兼容OpenAI格式）"""

import os
import json
import requests
from typing import Dict, List, Optional
from dotenv import load_dotenv

load_dotenv()


class OpenAIAPI:
    """OpenAI API类（兼容OpenAI格式）"""

    def __init__(self):
        """初始化API客户端"""
        self.api_url = os.getenv("OPENAI_API_URL", "https://api.openai.com/v1/chat/completions")
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model_id = os.getenv("OPENAI_MODEL_ID", "gpt-3.5-turbo")
        self.is_configured = bool(self.api_key)

    def call_llm(self, prompt: str, temperature: float = 0.7) -> str:
        """
        调用LLM生成文本

        Args:
            prompt: 提示词
            temperature: 温度参数

        Returns:
            生成的文本
        """
        if not self.is_configured:
            return self._get_fallback_response(prompt)

        # 构建请求体
        request_data = {
            "model": self.model_id,
            "messages": [
                {"role": "system", "content": "你是一个专业的剧本创作助手。你生成的内容必须是有效的JSON格式。"},
                {"role": "user", "content": prompt}
            ],
            "temperature": temperature,
            "max_tokens": 2048
        }

        try:
            response = requests.post(
                self.api_url,
                json=request_data,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                timeout=60
            )
            response.raise_for_status()
            result = response.json()

            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"]
            else:
                return self._get_fallback_response(prompt)

        except Exception as e:
            print(f"API调用失败: {e}")
            return self._get_fallback_response(prompt)

    def analyze_novel(self, chapters: List[Dict[str, str]]) -> Dict:
        """
        分析小说内容

        Args:
            chapters: 章节列表

        Returns:
            分析结果
        """
        prompt = self._build_analysis_prompt(chapters)
        response = self.call_llm(prompt)
        return self._parse_analysis_response(response)

    def extract_characters(self, text: str) -> List[Dict[str, str]]:
        """
        从文本中提取人物

        Args:
            text: 文本内容

        Returns:
            人物列表
        """
        prompt = f"""请从以下文本中提取人物信息，以JSON格式返回：
文本：
{text}

返回格式：
[
    {{"id": "char_001", "name": "姓名", "role": "主角/配角/其他", "description": "角色描述"}}
]"""

        response = self.call_llm(prompt)
        return self._parse_characters_response(response)

    def extract_scenes(self, text: str) -> List[Dict[str, str]]:
        """
        从文本中提取场景

        Args:
            text: 文本内容

        Returns:
            场景列表
        """
        prompt = f"""请从以下文本中提取场景信息，以JSON格式返回：
文本：
{text}

返回格式：
[
    {{"id": "scene_001", "title": "场景标题", "location": "地点", "time": "时间", "summary": "场景摘要"}}
]"""

        response = self.call_llm(prompt)
        return self._parse_scenes_response(response)

    def _build_analysis_prompt(self, chapters: List[Dict[str, str]]) -> str:
        """构建分析提示词"""
        text = "\n\n".join([f"第{chr(65+i)}章：\n{c['content']}" for i, c in enumerate(chapters[:3])])
        return f"""请分析以下小说内容，提取人物、场景、情节等信息：

{text}

请以JSON格式返回分析结果，包含：
1. characters: 人物列表
2. scenes: 场景列表
3. relationships: 人物关系
4. key_events: 关键事件"""

    def _parse_analysis_response(self, response: str) -> Dict:
        """解析分析响应"""
        try:
            # 尝试解析JSON
            for line in response.split('\n'):
                if '{' in line and '}' in line:
                    start = line.find('{')
                    end = line.rfind('}') + 1
                    json_str = line[start:end]
                    data = json.loads(json_str)
                    if isinstance(data, dict):
                        return data
        except json.JSONDecodeError:
            pass

        return {
            "characters": [],
            "scenes": [],
            "relationships": [],
            "key_events": []
        }

    def _parse_characters_response(self, response: str) -> List[Dict[str, str]]:
        """解析人物响应"""
        try:
            for line in response.split('\n'):
                if '[' in line and ']' in line:
                    start = line.find('[')
                    end = line.rfind(']') + 1
                    json_str = line[start:end]
                    data = json.loads(json_str)
                    if isinstance(data, list):
                        return data
        except json.JSONDecodeError:
            pass

        return []

    def _parse_scenes_response(self, response: str) -> List[Dict[str, str]]:
        """解析场景响应"""
        try:
            for line in response.split('\n'):
                if '[' in line and ']' in line:
                    start = line.find('[')
                    end = line.rfind(']') + 1
                    json_str = line[start:end]
                    data = json.loads(json_str)
                    if isinstance(data, list):
                        return data
        except json.JSONDecodeError:
            pass

        return []

    def _get_fallback_response(self, prompt: str) -> str:
        """
        获取降级响应（当API未配置时）

        Args:
            prompt: 提示词

        Returns:
            降级响应文本
        """
        if "人物" in prompt:
            return '[{"id": "char_001", "name": "林舟", "role": "主角", "description": "故事主角"}]'
        elif "场景" in prompt:
            return '[{"id": "scene_001", "title": "场景一", "location": "办公室", "time": "白天", "summary": "主要场景"}]'
        return "这是降级响应，实际内容应由LLM生成。"

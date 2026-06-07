"""LLM集成层 - 讯飞星火API集成"""

import os
import json
import re
import requests
from typing import Dict, List, Optional
from dotenv import load_dotenv

load_dotenv()


class XunFeiAPI:
    """讯飞星火API类（兼容OpenAI格式）"""

    def __init__(self):
        """初始化API客户端"""
        # 讯飞 API 配置
        self.api_url = os.getenv("OPENAI_API_URL", "https://maas-coding-api.cn-huabei-1.xf-yun.com/v2")
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model_id = os.getenv("OPENAI_MODEL_ID", "qwen3.6-35b-a3b")
        self.is_configured = bool(self.api_key and self.api_url)

    def _extract_json(self, text: str) -> str:
        """
        从文本中提取 JSON 对象

        处理以下情况：
        1. 纯 JSON
        2. 包含 ```json ... ``` 代码块
        3. 包含 ``` ... ``` 代码块
        4. JSON 作为字符串在字典中
        """
        # 尝试查找 ```json ... ``` 块
        json_match = re.search(r'```json\s*(.*?)\s*```', text, re.DOTALL)
        if json_match:
            return json_match.group(1)

        # 尝试查找 ``` ... ``` 块
        json_match = re.search(r'```\s*(.*?)\s*```', text, re.DOTALL)
        if json_match:
            return json_match.group(1)

        # 返回原文本
        return text

    def call_llm(self, prompt: str, temperature: float = 0.7, use_json_mode: bool = False, max_tokens: int = 8192) -> str:
        """
        调用LLM生成文本

        Args:
            prompt: 提示词
            temperature: 温度参数
            use_json_mode: 是否启用 JSON Mode
            max_tokens: 最大输出 tokens 数量（默认 8192，满足高质量剧本生成需求）

        Returns:
            生成的文本
        """
        if not self.is_configured:
            return self._get_fallback_response(prompt)

        # 构建请求体 - 兼容 OpenAI 格式
        request_data = {
            "model": self.model_id,
            "messages": [
                {"role": "system", "content": "你是一个专业的剧本创作助手。你生成的内容必须是有效的JSON格式。"},
                {"role": "user", "content": prompt}
            ],
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        # 如果启用 JSON Mode，添加额外配置
        if use_json_mode:
            request_data["extra_body"] = {
                "response_format": {"type": "json_object"}
            }

        try:
            response = requests.post(
                self.api_url,
                json=request_data,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                timeout=120
            )

            print(f"API响应状态码: {response.status_code}")
            print(f"API响应内容: {response.text[:200]}")

            response.raise_for_status()
            result = response.json()

            if "choices" in result and len(result["choices"]) > 0:
                content = result["choices"][0]["message"]["content"]
                # 提取 JSON（处理可能的 Markdown 代码块）
                return self._extract_json(content)
            else:
                return self._get_fallback_response(prompt)

        except Exception as e:
            print(f"API调用失败: {e}")
            return self._get_fallback_response(prompt)

    def call_llm_stream(
        self,
        prompt: str,
        temperature: float = 0.7,
        use_json_mode: bool = False,
        max_tokens: int = 8192
    ):
        """
        调用LLM生成文本（流式版本）

        Args:
            prompt: 提示词
            temperature: 温度参数
            use_json_mode: 是否启用 JSON Mode
            max_tokens: 最大输出 tokens 数量

        Yields:
            str: 流式响应的文本片段
        """
        if not self.is_configured:
            yield self._get_fallback_response(prompt)
            return

        # 构建请求体 - 兼容 OpenAI 格式
        request_data = {
            "model": self.model_id,
            "messages": [
                {"role": "system", "content": "你是一个专业的剧本创作助手。你生成的内容必须是有效的JSON格式。"},
                {"role": "user", "content": prompt}
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": True  # 启用流式
        }

        # 如果启用 JSON Mode，添加额外配置
        if use_json_mode:
            request_data["extra_body"] = {
                "response_format": {"type": "json_object"}
            }

        try:
            response = requests.post(
                self.api_url,
                json=request_data,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                timeout=120,
                stream=True  # 启用流式响应
            )

            print(f"API响应状态码: {response.status_code}")

            response.raise_for_status()

            # 流式读取响应
            full_content = ""
            for line in response.iter_lines():
                if line:
                    # 解析 SSE 格式的数据
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
                                    full_content += content
                                    yield content
                        except json.JSONDecodeError:
                            pass

            # 返回完整的 JSON（处理可能的 Markdown 代码块）
            yield self._extract_json(full_content)

        except Exception as e:
            print(f"API调用失败: {e}")
            yield self._get_fallback_response(prompt)

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
            # 先尝试直接解析整个响应
            data = json.loads(response)
            if isinstance(data, list):
                return data
            # 如果是字典，尝试提取列表类型的字段
            if isinstance(data, dict):
                for key in ['characters', 'data', 'result']:
                    if key in data and isinstance(data[key], list):
                        return data[key]
            # 查找第一个 [ 和最后一个 ]
            start = response.find('[')
            end = response.rfind(']') + 1
            if start != -1 and end > start:
                json_str = response[start:end]
                data = json.loads(json_str)
                if isinstance(data, list):
                    return data
        except json.JSONDecodeError:
            pass

        return []

    def _parse_scenes_response(self, response: str) -> List[Dict[str, str]]:
        """解析场景响应"""
        try:
            # 先尝试直接解析整个响应
            data = json.loads(response)
            if isinstance(data, list):
                return data
            # 如果是字典，尝试提取列表类型的字段
            if isinstance(data, dict):
                for key in ['scenes', 'data', 'result']:
                    if key in data and isinstance(data[key], list):
                        return data[key]
            # 查找第一个 [ 和最后一个 ]
            start = response.find('[')
            end = response.rfind(']') + 1
            if start != -1 and end > start:
                json_str = response[start:end]
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

    async def call_llm_stream_async(
        self,
        prompt: str,
        temperature: float = 0.7,
        use_json_mode: bool = False,
        max_tokens: int = 8192
    ):
        """
        异步调用LLM生成文本（流式版本）

        Args:
            prompt: 提示词
            temperature: 温度参数
            use_json_mode: 是否启用 JSON Mode
            max_tokens: 最大输出 tokens 数量

        Yields:
            str: 流式响应的文本片段
        """
        import asyncio
        import aiohttp

        if not self.is_configured:
            yield self._get_fallback_response(prompt)
            return

        # 构建请求体
        request_data = {
            "model": self.model_id,
            "messages": [
                {"role": "system", "content": "你是一个专业的剧本创作助手。"},
                {"role": "user", "content": prompt}
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": True
        }

        if use_json_mode:
            request_data["extra_body"] = {
                "response_format": {"type": "json_object"}
            }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.api_url,
                    json=request_data,
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    timeout=aiohttp.ClientTimeout(total=120)
                ) as response:
                    print(f"API响应状态码: {response.status}")

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
            yield self._get_fallback_response(prompt)


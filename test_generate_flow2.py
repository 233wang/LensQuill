import sys
sys.path.insert(0, '.')
import json
import re

from dotenv import load_dotenv
load_dotenv()

from llm.xunfei_api import XunFeiAPI

# 读取示例小说的第一章
with open("examples/input_novel.txt", "r", encoding="utf-8") as f:
    content = f.read()

chapter = {
    "title": "第1章 塞壬小镇",
    "content": content.split(" 第2章")[0][:3000]  # 限制长度
}

# 测试提示词
prompt = f"""你是一个专业的剧本创作助手。

【任务】将以下小说章节转换为结构化剧本格式。

【要求】
1. 保留原著的文学性和细节描写
2. 将叙述性内容转换为剧本格式（动作、对话、场景描述）
3. 合理划分场景和分镜
4. 严格输出 JSON 格式，不要包含任何额外解释或 Markdown 代码块

【JSON Schema】
{{
    "chapter_index": 1,
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

print("测试提示词长度:", len(prompt))
print("\n调用 LLM...")

# 调用 LLM
llm_api = XunFeiAPI()
response = llm_api.call_llm(prompt, use_json_mode=True)

print("\n响应内容:")
print(response[:500])
print("\n长度:", len(response))

# 尝试解析 JSON
try:
    data = json.loads(response)
    print("\n✓ JSON 解析成功!")
    print("章节标题:", data.get('chapter_title'))
    print("场景数:", len(data.get('scenes', [])))
except json.JSONDecodeError as e:
    print(f"\n✗ JSON 解析失败: {e}")

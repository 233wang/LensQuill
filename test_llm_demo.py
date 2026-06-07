"""
讯飞星火 API 测试脚本
基于官方 Python Demo 修改，用于验证 LLM 对话功能
"""

import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

def test_llm_chat():
    """测试基础聊天功能"""
    print("=" * 60)
    print("讯飞星火 API 测试 - 基础聊天")
    print("=" * 60)
    
    api_url = os.getenv("OPENAI_API_URL", "https://maas-api.cn-huabei-1.xf-yun.com/v2/chat/completions")
    api_key = os.getenv("OPENAI_API_KEY")
    model_id = os.getenv("OPENAI_MODEL_ID", "astron-code-latest")
    
    print(f"API URL: {api_url}")
    print(f"Model ID: {model_id}")
    print(f"API Key: {api_key[:10]}...{api_key[-10:] if len(api_key) > 10 else ''}")
    
    # 构建请求体 - 兼容 OpenAI 格式
    request_data = {
        "model": model_id,
        "messages": [
            {"role": "system", "content": "你是一个专业的剧本创作助手，善于将小说内容转换为剧本格式。"},
            {"role": "user", "content": "你好，请介绍一下你自己。"}
        ],
        "temperature": 0.7,
        "max_tokens": 1024
    }
    
    try:
        response = requests.post(
            api_url,
            json=request_data,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            timeout=60
        )
        
        print(f"\n响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"响应ID: {result.get('id')}")
            print(f"模型: {result.get('model')}")
            
            if "choices" in result and len(result["choices"]) > 0:
                content = result["choices"][0]["message"]["content"]
                print(f"\nAI 回复:\n{content}")
                print("\n✓ 基础聊天测试通过")
                return True
            else:
                print("✗ 响应格式错误")
                return False
        else:
            print(f"✗ 请求失败: {response.text}")
            return False
            
    except Exception as e:
        print(f"✗ 请求异常: {e}")
        return False


def test_json_mode():
    """测试 JSON Mode - 用于结构化输出"""
    print("\n" + "=" * 60)
    print("讯飞星火 API 测试 - JSON Mode (结构化输出)")
    print("=" * 60)
    
    api_url = os.getenv("OPENAI_API_URL", "https://maas-api.cn-huabei-1.xf-yun.com/v2/chat/completions")
    api_key = os.getenv("OPENAI_API_KEY")
    model_id = os.getenv("OPENAI_MODEL_ID", "astron-code-latest")
    
    # 构建请求体 - 启用 JSON Mode
    request_data = {
        "model": model_id,
        "messages": [
            {"role": "system", "content": "你是一个专业的剧本创作助手。你生成的内容必须是有效的JSON格式。"},
            {"role": "user", "content": """请根据以下小说内容，提取人物信息并以JSON格式返回：

小说内容：
"白柳皱起眉来。'这是哪里？'他自言自语道。'我为什么在这里？'"

返回格式：
{
    "characters": [
        {"id": "char_001", "name": "姓名", "description": "角色描述", "role": "主角"}
    ]
}"""}
        ],
        "temperature": 0.7,
        "max_tokens": 2048,
        "extra_body": {
            "response_format": {"type": "json_object"}
        }
    }
    
    try:
        response = requests.post(
            api_url,
            json=request_data,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            timeout=60
        )
        
        print(f"\n响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            
            if "choices" in result and len(result["choices"]) > 0:
                content = result["choices"][0]["message"]["content"]
                print(f"\n原始响应:\n{content}")
                
                # 尝试解析 JSON
                try:
                    parsed = json.loads(content)
                    print(f"\n✓ JSON 解析成功:")
                    print(json.dumps(parsed, indent=2, ensure_ascii=False))
                    print("\n✓ JSON Mode 测试通过")
                    return True
                except json.JSONDecodeError as e:
                    print(f"\n✗ JSON 解析失败: {e}")
                    return False
            else:
                print("✗ 响应格式错误")
                return False
        else:
            print(f"✗ 请求失败: {response.text}")
            return False
            
    except Exception as e:
        print(f"✗ 请求异常: {e}")
        return False


def test_chapter_to_script():
    """测试章节转换为剧本"""
    print("\n" + "=" * 60)
    print("讯飞星火 API 测试 - 章节转剧本")
    print("=" * 60)
    
    api_url = os.getenv("OPENAI_API_URL", "https://maas-api.cn-huabei-1.xf-yun.com/v2/chat/completions")
    api_key = os.getenv("OPENAI_API_KEY")
    model_id = os.getenv("OPENAI_MODEL_ID", "astron-code-latest")
    
    # 读取示例小说的第一章
    with open("examples/input_novel.txt", "r", encoding="utf-8") as f:
        chapter_content = f.read()
        # 只取第一章内容
        chapter_content = chapter_content.split(" 第2章")[0]
    
    # Prompt 模板
    prompt = f"""你是一个专业的剧本创作助手。

【任务】将以下小说章节转换为结构化剧本格式。

【要求】
1. 保留原著的文学性和细节描写
2. 将叙述性内容转换为剧本格式（动作、对话、场景描述）
3. 合理划分场景和分镜
4. 严格输出 JSON 格式，不要添加任何额外解释

【JSON Schema】
{{
    "chapter_index": 数字,
    "chapter_title": "字符串",
    "scenes": [
        {{
            "scene_index": 数字,
            "scene_title": "字符串",
            "location": "字符串",
            "time": "字符串",
            "description": "字符串",
            "shots": [
                {{
                    "shot_index": 数字,
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

【小说内容】
{chapter_content}

【输出要求】
请直接输出 JSON 格式，不要包含任何额外文本。
"""

    request_data = {
        "model": model_id,
        "messages": [
            {"role": "system", "content": "你是一个专业的剧本创作助手。"},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 4096,
        "extra_body": {
            "response_format": {"type": "json_object"}
        }
    }
    
    try:
        response = requests.post(
            api_url,
            json=request_data,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            timeout=120
        )
        
        print(f"\n响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            
            if "choices" in result and len(result["choices"]) > 0:
                content = result["choices"][0]["message"]["content"]
                
                # 尝试解析 JSON
                try:
                    parsed = json.loads(content)
                    print(f"\n✓ JSON 解析成功!")
                    print(f"章节: {parsed.get('chapter_title')}")
                    print(f"场景数: {len(parsed.get('scenes', []))}")
                    print(f"\n剧本预览:")
                    print(json.dumps(parsed, indent=2, ensure_ascii=False)[:1000] + "...")
                    print("\n✓ 章节转剧本测试通过")
                    return True
                except json.JSONDecodeError as e:
                    print(f"\n✗ JSON 解析失败: {e}")
                    print(f"原始响应:\n{content[:500]}...")
                    return False
            else:
                print("✗ 响应格式错误")
                return False
        else:
            print(f"✗ 请求失败: {response.text}")
            return False
            
    except Exception as e:
        print(f"✗ 请求异常: {e}")
        return False


if __name__ == "__main__":
    print("\n讯飞星火 API 测试套件")
    print("Based on 官方 Python Demo")
    
    # 测试1: 基础聊天
    test1_pass = test_llm_chat()
    
    # 测试2: JSON Mode
    test2_pass = test_json_mode()
    
    # 测试3: 章节转剧本
    test3_pass = test_chapter_to_script()
    
    # 总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    print(f"基础聊天测试: {'✓ 通过' if test1_pass else '✗ 失败'}")
    print(f"JSON Mode测试: {'✓ 通过' if test2_pass else '✗ 失败'}")
    print(f"章节转剧本测试: {'✓ 通过' if test3_pass else '✗ 失败'}")
    
    all_pass = test1_pass and test2_pass and test3_pass
    print(f"\n总体: {'✓ 全部通过' if all_pass else '✗ 部分测试失败'}")

import sys
sys.path.insert(0, '.')

from dotenv import load_dotenv
load_dotenv()

from llm.xunfei_api import XunFeiAPI
from core.script_generator_v2 import ScriptGeneratorV2

# 读取示例小说的第一章
with open("examples/input_novel.txt", "r", encoding="utf-8") as f:
    content = f.read()

# 按章节分割（简单处理）
chapters = [
    {
        "title": "第1章 塞壬小镇",
        "content": content.split(" 第2章")[0]
    },
    {
        "title": "第2章 塞壬小镇", 
        "content": content.split(" 第2章")[1].split(" 第3章")[0] if " 第2章" in content else ""
    },
    {
        "title": "第3章 塞壬小镇",
        "content": content.split(" 第3章")[1] if " 第3章" in content else ""
    }
]

print(f"共读取 {len(chapters)} 个章节")
print(f"第一章长度: {len(chapters[0]['content'])} 字符")

# 初始化 LLM API
print("\n初始化 LLM API...")
llm_api = XunFeiAPI()
print(f"API 配置状态: {llm_api.is_configured}")

# 创建剧本生成器
print("\n创建剧本生成器...")
generator = ScriptGeneratorV2(llm_api=llm_api)

# 为第一章生成剧本
print("\n生成第一章剧本...")
chapter_script = generator.generate_script_from_chapter(chapters[0], 1)

print(f"\n章节标题: {chapter_script.get('chapter_title')}")
print(f"场景数量: {len(chapter_script.get('scenes', []))}")

if chapter_script.get('scenes'):
    scene = chapter_script['scenes'][0]
    print(f"\n第一个场景:")
    print(f"  标题: {scene.get('scene_title')}")
    print(f"  地点: {scene.get('location')}")
    print(f"  描述: {scene.get('description', '')[:100]}...")
    
    if scene.get('shots'):
        shot = scene['shots'][0]
        print(f"\n第一个分镜:")
        print(f"  类型: {shot.get('shot_type')}")
        print(f"  动作: {shot.get('action', '')[:100]}...")
        print(f"  对话: {len(shot.get('dialogue', []))} 条")

# 生成完整剧本
print("\n生成完整剧本...")
full_script = generator.convert_to_script_format(chapters, [])

print(f"\n完整剧本结构:")
print(f"  元信息版本: {full_script.get('metadata', {}).get('version')}")
print(f"  源章节数: {full_script.get('metadata', {}).get('source_chapters')}")
print(f"  生成模型: {full_script.get('metadata', {}).get('llm_model')}")
print(f"  人物数量: {len(full_script.get('characters', []))}")
print(f"  剧本章节数: {len(full_script.get('chapters', []))}")
print("\n✓ 测试完成")

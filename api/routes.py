"""API路由 - 剧本生成 API"""

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import StreamingResponse
from typing import List, Dict, Optional
from io import StringIO
import chardet
import json
import asyncio

router = APIRouter(prefix="/api", tags=["API"])


@router.post("/upload")
async def upload_text(input_data: Dict):
    """
    上传小说文本

    支持直接粘贴文本或上传文件
    """
    content = input_data.get("content", "")
    format_type = input_data.get("format", "text")
    filename = input_data.get("filename", "")

    if not content:
        raise HTTPException(status_code=400, detail="内容不能为空")

    # 如果是文件上传，尝试检测编码
    if format_type == "file" and filename:
        content = _detect_and_convert_encoding(content)

    return {
        "status": "success",
        "filename": filename,
        "content_length": len(content),
        "content": content
    }


@router.post("/analyze")
async def analyze_novel(chapters: List[Dict]):
    """
    分析小说内容

    提取人物、场景、情节等信息
    """
    if not chapters:
        raise HTTPException(status_code=400, detail="章节列表不能为空")

    from llm.xunfei_api import XunFeiAPI
    from core.novel_analyzer import NovelAnalyzer

    # 初始化 LLM API
    llm_api = XunFeiAPI()
    analyzer = NovelAnalyzer(llm_api=llm_api)

    # 使用 LLM 提取人物和场景
    characters = analyzer.extract_characters(chapters)
    scenes = analyzer.extract_scenes(chapters)
    relationships = analyzer.analyze_relationships(characters)
    key_events = analyzer.extract_key_events(chapters)

    return {
        "status": "success",
        "analysis": {
            "characters": characters,
            "scenes": scenes,
            "relationships": relationships,
            "key_events": key_events
        }
    }


async def stream_script_generator(input_data: Dict):
    """
    流式生成剧本的异步生成器

    Args:
        input_data: 包含 chapters 和 analysis 的请求体

    Yields:
        str: SSE 格式的事件数据
    """
    from llm.xunfei_api import XunFeiAPI
    from core.script_generator_streaming import StreamingScriptGenerator

    chapters = input_data.get("chapters", [])
    analysis = input_data.get("analysis")

    # 初始化 LLM API
    llm_api = XunFeiAPI()

    # 获取人物列表（如果有）
    characters = analysis.get("characters", []) if analysis else []

    # 创建流式剧本生成器
    generator = StreamingScriptGenerator(llm_api=llm_api)

    async for event in generator.generate_script_stream(chapters, characters):
        yield f"data: {json.dumps(event, ensure_ascii=False)}\n\n"
        # 添加小延迟，让前端有时间渲染
        await asyncio.sleep(0.1)


@router.post("/generate")
async def generate_script(input_data: Dict):
    """
    生成剧本（流式版本）

    按章节整体生成剧本，每个章节包含完整的场景和分镜

    Args:
        input_data: 包含 chapters 和 analysis 的请求体

    Returns:
        SSE 流式响应
    """
    chapters = input_data.get("chapters", [])

    if not chapters:
        raise HTTPException(status_code=400, detail="章节列表不能为空")

    # 返回流式响应
    return StreamingResponse(
        stream_script_generator(input_data),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )


@router.post("/export")
async def export_to_yaml(script: Dict):
    """
    导出YAML格式

    将剧本转换为YAML格式字符串
    """
    if not script:
        raise HTTPException(status_code=400, detail="剧本数据不能为空")

    from core.yaml_exporter import YamlExporter

    exporter = YamlExporter()

    # 验证数据
    if not exporter.validate_schema(script):
        raise HTTPException(status_code=400, detail="数据结构不符合YAML Schema")

    yaml_content = exporter.export_yaml(script)
    formatted_yaml = exporter.format_yaml(yaml_content)

    return {
        "status": "success",
        "yaml": formatted_yaml
    }


def _detect_and_convert_encoding(content: str) -> str:
    """
    检测并转换编码

    Args:
        content: 原始内容（字节串）

    Returns:
        转换后的Unicode字符串
    """
    try:
        # 尝试直接作为字符串处理
        if isinstance(content, str):
            return content
        # 尝试检测编码
        detected = chardet.detect(content)
        if detected['encoding']:
            return content.decode(detected['encoding'])
        return content.decode('utf-8', errors='ignore')
    except Exception:
        return content

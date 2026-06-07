"""API路由 - 流式剧本生成"""

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
    content = input_data.get("content", "")
    format_type = input_data.get("format", "text")
    filename = input_data.get("filename", "")

    if not content:
        raise HTTPException(status_code=400, detail="内容不能为空")

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
    if not chapters:
        raise HTTPException(status_code=400, detail="章节列表不能为空")

    from llm.xunfei_api import XunFeiAPI
    from core.novel_analyzer import NovelAnalyzer

    llm_api = XunFeiAPI()
    analyzer = NovelAnalyzer(llm_api=llm_api)

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
    逐章调用大模型流式输出，通过 SSE 转发给前端
    """
    from llm.xunfei_api import XunFeiAPI
    from core.script_generator_streaming import StreamingScriptGenerator

    chapters = input_data.get("chapters", [])
    analysis = input_data.get("analysis")

    llm_api = XunFeiAPI()
    characters = analysis.get("characters", []) if analysis else []

    generator = StreamingScriptGenerator(llm_api=llm_api)

    async for event in generator.generate_script_stream(chapters, characters):
        yield f"data: {json.dumps(event, ensure_ascii=False)}\n\n"
        await asyncio.sleep(0.1)


@router.post("/generate")
async def generate_script(input_data: Dict):
    """
    生成剧本 - 流式版本
    逐章流式调用大模型，前端实时显示处理进度
    """
    chapters = input_data.get("chapters", [])

    if not chapters:
        raise HTTPException(status_code=400, detail="章节列表不能为空")

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
    if not script:
        raise HTTPException(status_code=400, detail="剧本数据不能为空")

    from core.yaml_exporter import YamlExporter

    exporter = YamlExporter()

    if not exporter.validate_schema(script):
        raise HTTPException(status_code=400, detail="数据结构不符合YAML Schema")

    yaml_content = exporter.export_yaml(script)
    formatted_yaml = exporter.format_yaml(yaml_content)

    return {
        "status": "success",
        "yaml": formatted_yaml
    }


def _detect_and_convert_encoding(content: str) -> str:
    try:
        if isinstance(content, str):
            return content
        detected = chardet.detect(content)
        if detected['encoding']:
            return content.decode(detected['encoding'])
        return content.decode('utf-8', errors='ignore')
    except Exception:
        return content

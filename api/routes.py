"""API路由"""

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from typing import List, Dict, Optional
from io import StringIO
import chardet

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

    from core.novel_analyzer import NovelAnalyzer
    analyzer = NovelAnalyzer()

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


@router.post("/generate")
async def generate_script(chapters: List[Dict], analysis: Optional[Dict] = None):
    """
    生成剧本

    将小说内容转换为剧本格式
    """
    if not chapters:
        raise HTTPException(status_code=400, detail="章节列表不能为空")

    from core.script_generator import ScriptGenerator
    from core.novel_analyzer import NovelAnalyzer

    # 如果没有提供分析结果，先进行分析
    if not analysis:
        analyzer = NovelAnalyzer()
        analysis = {
            "characters": analyzer.extract_characters(chapters),
            "scenes": analyzer.extract_scenes(chapters),
            "relationships": analyzer.analyze_relationships([]),
            "key_events": analyzer.extract_key_events(chapters)
        }

    generator = ScriptGenerator()
    script = generator.convert_to_script_format(chapters, analysis)

    return {
        "status": "success",
        "script": script
    }


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

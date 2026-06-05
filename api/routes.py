"""API路由"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List, Dict
import io

router = APIRouter(prefix="/api", tags=["API"])


@router.post("/upload")
async def upload_text(input_data: Dict):
    """
    上传小说文本
    """
    pass


@router.post("/analyze")
async def analyze_novel(chapters: List[Dict]):
    """
    分析小说内容
    """
    pass


@router.post("/generate")
async def generate_script(chapters: List[Dict], analysis: Dict):
    """
    生成剧本
    """
    pass


@router.post("/export")
async def export_to_yaml(script: Dict):
    """
    导出YAML格式
    """
    pass

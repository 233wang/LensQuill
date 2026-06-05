"""API数据模型"""

from pydantic import BaseModel
from typing import List, Dict, Optional


class TextInput(BaseModel):
    """文本输入模型"""
    content: str
    format: str = "text"


class FileInput(BaseModel):
    """文件输入模型"""
    filename: str
    content: str


class Chapter(BaseModel):
    """章节模型"""
    title: str
    content: str


class AnalysisResult(BaseModel):
    """分析结果模型"""
    characters: List[Dict]
    scenes: List[Dict]
    relationships: List[Dict]


class ScriptOutput(BaseModel):
    """剧本输出模型"""
    script: Dict


class YamlExportRequest(BaseModel):
    """YAML导出请求"""
    script: Dict


class YamlExportResponse(BaseModel):
    """YAML导出响应"""
    yaml: str

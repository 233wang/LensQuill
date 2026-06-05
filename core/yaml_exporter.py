"""YAML导出器 - 导出YAML格式的剧本"""

from typing import Dict
import yaml


class YamlExporter:
    """YAML导出器类"""

    def __init__(self):
        """初始化YAML导出器"""
        pass

    def export_yaml(self, data: Dict) -> str:
        """
        导出为YAML格式

        Args:
            data: 数据对象

        Returns:
            YAML字符串
        """
        return yaml.dump(data, allow_unicode=True, indent=2, sort_keys=False)

    def validate_schema(self, data: Dict) -> bool:
        """
        验证数据结构是否符合Schema

        Args:
            data: 数据对象

        Returns:
            验证结果
        """
        required_keys = ['metadata', 'source', 'characters', 'scenes', 'beats']

        for key in required_keys:
            if key not in data:
                return False

        # 验证metadata
        if not isinstance(data['metadata'], dict):
            return False

        # 验证source
        if not isinstance(data['source'], dict):
            return False

        # 验证characters
        if not isinstance(data['characters'], list):
            return False

        # 验证scenes
        if not isinstance(data['scenes'], list):
            return False

        # 验证beats
        if not isinstance(data['beats'], list):
            return False

        return True

    def format_yaml(self, yaml_str: str) -> str:
        """
        格式化YAML字符串

        Args:
            yaml_str: YAML字符串

        Returns:
            格式化后的YAML字符串
        """
        # 添加文件头注释
        header = "# AI 小说转剧本输出\n# 本文件由AI工具自动生成，可继续编辑修改\n\n"
        return header + yaml_str

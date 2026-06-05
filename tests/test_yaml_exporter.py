"""YAML导出器测试"""

import pytest
from core.yaml_exporter import YamlExporter


class TestYamlExporter:
    """YAML导出器测试类"""

    def setup_method(self):
        """每个测试前的初始化"""
        self.exporter = YamlExporter()

    def test_export_yaml_basic(self):
        """测试基本YAML导出"""
        data = {
            "metadata": {"version": "1.0"},
            "title": "测试剧本"
        }

        yaml_str = self.exporter.export_yaml(data)

        assert "version: '1.0'" in yaml_str
        assert "title: 测试剧本" in yaml_str

    def test_export_yaml_with_chinese(self):
        """测试中文内容导出"""
        data = {
            "title": "测试剧本",
            "description": "这是一个测试用的剧本",
            "characters": [
                {"name": "林舟", "description": "主角"}
            ]
        }

        yaml_str = self.exporter.export_yaml(data)

        assert "这是一个测试用的剧本" in yaml_str
        assert "林舟" in yaml_str

    def test_validate_schema_valid(self):
        """测试有效数据结构验证"""
        data = {
            "metadata": {"version": "1.0", "generated_by": "test"},
            "source": {"type": "novel", "title": "测试", "chapters_count": 1, "chapters": []},
            "characters": [],
            "scenes": [],
            "beats": []
        }

        assert self.exporter.validate_schema(data) is True

    def test_validate_schema_missing_required_fields(self):
        """测试缺失必填字段验证"""
        data = {
            "metadata": {"version": "1.0"},
            # 缺少 source, characters, scenes, beats
        }

        assert self.exporter.validate_schema(data) is False

    def test_validate_schema_invalid_types(self):
        """测试错误类型验证"""
        data = {
            "metadata": {"version": "1.0"},
            "source": {"type": "novel"},
            "characters": "not a list",  # 错误类型
            "scenes": [],
            "beats": []
        }

        assert self.exporter.validate_schema(data) is False

    def test_validate_schema_empty_valid(self):
        """测试空列表情况"""
        data = {
            "metadata": {"version": "1.0"},
            "source": {"type": "novel", "title": "", "chapters_count": 0, "chapters": []},
            "characters": [],
            "scenes": [],
            "beats": []
        }

        assert self.exporter.validate_schema(data) is True

    def test_format_yaml_with_header(self):
        """测试YAML格式化添加文件头"""
        yaml_content = "title: 测试\n"
        formatted = self.exporter.format_yaml(yaml_content)

        assert "# AI 小说转剧本输出" in formatted
        assert "# 本文件由AI工具自动生成，可继续编辑修改" in formatted
        assert "title: 测试" in formatted

    def test_export_yaml_nested_structure(self):
        """测试嵌套结构导出"""
        data = {
            "metadata": {
                "version": "1.0",
                "generated_at": "2024-01-01T12:00:00",
                "nested": {
                    "level": 2,
                    "value": "deep"
                }
            },
            "scenes": [
                {
                    "id": "scene_001",
                    "beats": [
                        {"type": "action", "content": "测试内容"}
                    ]
                }
            ]
        }

        yaml_str = self.exporter.export_yaml(data)

        assert "version: '1.0'" in yaml_str
        assert "level: 2" in yaml_str
        assert "type: action" in yaml_str
        assert "content: 测试内容" in yaml_str

    def test_export_yaml_special_characters(self):
        """测试特殊字符处理"""
        data = {
            "title": "测试: 剧本",
            "content": "包含特殊字符: = - * [] {}"
        }

        yaml_str = self.exporter.export_yaml(data)

        # 确保特殊字符被正确处理
        assert "测试: 剧本" in yaml_str

    def test_full_workflow(self):
        """测试完整工作流"""
        data = {
            "metadata": {
                "version": "1.0",
                "generated_by": "AI Tool",
                "generated_at": "2024-01-01T12:00:00"
            },
            "source": {
                "type": "novel",
                "title": "测试小说",
                "chapters_count": 1,
                "chapters": ["第一章"]
            },
            "characters": [
                {"id": "char_001", "name": "林舟", "role": "protagonist"}
            ],
            "scenes": [
                {
                    "id": "scene_001",
                    "title": "场景一",
                    "location": "办公室",
                    "time": "白天",
                    "characters": ["char_001"],
                    "beats": [
                        {"type": "dialogue", "content": "你好"}
                    ]
                }
            ],
            "beats": [
                {"type": "dialogue", "content": "你好"}
            ]
        }

        # 验证数据
        assert self.exporter.validate_schema(data) is True

        # 导出YAML
        yaml_str = self.exporter.export_yaml(data)

        # 格式化
        final_str = self.exporter.format_yaml(yaml_str)

        # 确保关键内容存在
        assert "林舟" in final_str
        assert "办公室" in final_str
        assert "你好" in final_str


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

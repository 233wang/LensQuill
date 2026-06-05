"""章节解析器测试"""

import pytest
from core.chapter_parser import ChapterParser


class TestChapterParser:
    """章节解析器测试类"""

    def setup_method(self):
        """每个测试前的初始化"""
        self.parser = ChapterParser()

    def test_parse_chapters_with_standard_titles(self):
        """测试标准章节标题解析"""
        text = """第一章 雨夜

林舟撑着伞，快步穿过巷子。

第二章 旧书店

第二天，他来到旧书店。

第三章 真相

老人讲述了秘密。"""

        chapters = self.parser.parse_chapters(text)

        assert len(chapters) == 3
        assert chapters[0]["title"] == "第一章 雨夜"
        assert "林舟撑着伞" in chapters[0]["content"]
        assert chapters[1]["title"] == "第二章 旧书店"
        assert chapters[2]["title"] == "第三章 真相"

    def test_parse_chapters_with_numbered_titles(self):
        """测试数字章节标题解析"""
        text = """第1章 初遇

故事开始于一个雨天。

第2章 发展

情节逐渐展开。

第3章 高潮

故事达到高潮。"""

        chapters = self.parser.parse_chapters(text)

        assert len(chapters) == 3
        assert chapters[0]["title"].startswith("第")
        assert chapters[1]["title"].startswith("第")
        assert chapters[2]["title"].startswith("第")

    def test_parse_chapters_single_chapter(self):
        """测试单章节解析"""
        text = """这是一个没有明显章节标题的故事。

第一段内容。

第二段内容。"""

        chapters = self.parser.parse_chapters(text)

        # 没有检测到章节标题时，整个文本作为一章
        assert len(chapters) == 1
        assert chapters[0]["title"] == "第一章"
        assert "这是一个没有明显章节标题的故事" in chapters[0]["content"]

    def test_detect_chapter_titles(self):
        """测试章节标题检测"""
        text = """第一章 开始

内容...

第二章 发展

内容...

第三章 结尾

内容..."""

        titles = self.parser.detect_chapter_titles(text)

        assert len(titles) == 3
        assert any("第一章" in t[0] for t in titles)
        assert any("第二章" in t[0] for t in titles)
        assert any("第三章" in t[0] for t in titles)

    def test_split_chapter_content(self):
        """测试章节内容分段"""
        title = "第一章 测试"
        content = """第一段内容。

第二段内容。

第三段内容。"""

        paragraphs = self.parser.split_chapter_content(title, content)

        assert len(paragraphs) == 3
        assert "第一段内容" in paragraphs[0]
        assert "第二段内容" in paragraphs[1]
        assert "第三段内容" in paragraphs[2]

    def test_parse_chapters_empty_text(self):
        """测试空文本处理"""
        chapters = self.parser.parse_chapters("")

        # 空文本应该返回一个空内容的章节
        assert len(chapters) == 1

    def test_parse_chapters_with_chinese_numbers(self):
        """测试中文数字章节标题"""
        text = """第一千零一章 新篇章

内容...

第一千零二章 继续

内容..."""

        chapters = self.parser.parse_chapters(text)

        assert len(chapters) == 2
        assert "第一千零一章" in chapters[0]["title"]
        assert "第一千零二章" in chapters[1]["title"]

    def test_chapter_content_trimming(self):
        """测试章节内容修剪"""
        text = """第一章 测试

内容开始...

第二章 第二节

内容继续..."""

        chapters = self.parser.parse_chapters(text)

        # 确保内容被正确修剪
        assert "内容开始..." in chapters[0]["content"]
        assert "内容继续..." in chapters[1]["content"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

"""章节解析器 - 解析小说文本中的章节结构

使用 txt_to_epub 库进行智能章节解析，正则表达式作为降级策略。
"""

from typing import List, Dict, Optional
import re

try:
    from txt_to_epub.parser import parse_chapters_from_content
    TXT_TO_EPUB_AVAILABLE = True
except ImportError:
    TXT_TO_EPUB_AVAILABLE = False


class ChapterParser:
    """章节解析器类"""

    def __init__(self):
        """初始化章节解析器"""
        self.chapter_patterns = [
            r'第[零一二三四五六七八九十百千0-9]+[章篇回节集]',  # 第一章、第1章
            r'序[章言言]',  # 序章、序言
            r'后[记语]',  # 后记、后语
        ]

    def parse_chapters(self, text: str) -> List[Dict[str, str]]:
        """
        解析小说文本中的章节

        Args:
            text: 小说文本内容

        Returns:
            章节列表，每个元素为 dict，包含 title 和 content
        """
        # 首先尝试使用 txt_to_epub 库
        if TXT_TO_EPUB_AVAILABLE and len(text) > 100:
            try:
                chapters = self._parse_with_txt_to_epub(text)
                if chapters:
                    return chapters
            except Exception as e:
                print(f"txt_to_epub 解析失败，使用降级策略: {e}")

        # 降级策略：使用正则表达式
        return self._parse_with_regex(text)

    def _parse_with_txt_to_epub(self, text: str) -> List[Dict[str, str]]:
        """
        使用 txt_to_epub 库解析章节

        Args:
            text: 小说文本内容

        Returns:
            章节列表
        """
        chapters = parse_chapters_from_content(text, language='chinese')

        result = []
        for chap in chapters:
            result.append({
                "title": chap.title,
                "content": chap.content.strip()
            })

        return result

    def _parse_with_regex(self, text: str) -> List[Dict[str, str]]:
        """
        使用正则表达式解析章节（降级策略）

        Args:
            text: 小说文本内容

        Returns:
            章节列表
        """
        chapters = []
        chapters_with_titles = self.detect_chapter_titles(text)

        if not chapters_with_titles:
            # 如果没有检测到章节标题，将整个文本作为一章
            return [{
                "title": "第一章",
                "content": text.strip()
            }]

        # 过滤掉子标题（如"第二节"在"第二章 第二节"中）
        filtered_titles = self._filter_sub_titles(chapters_with_titles)

        # 按章节标题分割文本
        for i, (title, position) in enumerate(filtered_titles):
            next_position = filtered_titles[i + 1][1] if i + 1 < len(filtered_titles) else len(text)
            content = text[position:next_position].strip()

            chapters.append({
                "title": title,
                "content": content
            })

        return chapters

    def detect_chapter_titles(self, text: str) -> List[tuple]:
        """
        检测章节标题

        Args:
            text: 小说文本内容

        Returns:
            章节标题列表，每个元素为 (title, position) 元组
        """
        titles = []

        for match in re.finditer(self.chapter_pattern, text):
            position = match.start()
            full_title = self._extract_full_title(text, position)
            titles.append((full_title, position))

        return titles

    def _extract_full_title(self, text: str, start_pos: int) -> str:
        """
        从文本中提取完整的标题行

        Args:
            text: 文本内容
            start_pos: 标题匹配的起始位置

        Returns:
            完整的标题字符串
        """
        match = re.search(self.chapter_pattern, text[start_pos:])
        if not match:
            return ""

        title = match.group(0)
        position = start_pos + match.end()

        while position < len(text) and text[position] in ' \t':
            position += 1

        line_end = text.find('\n', position)
        if line_end == -1:
            line_end = len(text)

        title_suffix = text[position:line_end].strip()
        full_title = title + ' ' + title_suffix if title_suffix else title

        return full_title.strip()

    def _filter_sub_titles(self, titles: List[tuple]) -> List[tuple]:
        """
        过滤掉子标题（如"第二节"在"第二章 第二节"中）

        Args:
            titles: 标题列表

        Returns:
            过滤后的标题列表
        """
        if not titles:
            return titles

        # 只保留章节标题（带"第...章"的）
        result = []
        for title, pos in titles:
            if re.match(r'第[零一二三四五六七八九十百千0-9]+章', title):
                result.append((title, pos))

        return result if result else titles

    def split_chapter_content(self, title: str, content: str) -> List[str]:
        """
        拆分章节内容为段落

        Args:
            title: 章节标题
            content: 章节内容

        Returns:
            段落列表
        """
        # 按空行分隔段落
        paragraphs = re.split(r'\n\s*\n', content)
        return [p.strip() for p in paragraphs if p.strip()]

    @property
    def chapter_pattern(self):
        """章节标题匹配模式"""
        return r'第[零一二三四五六七八九十百千0-9]+[章篇回节集]'

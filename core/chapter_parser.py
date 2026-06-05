"""章节解析器 - 解析小说文本中的章节结构"""

from typing import List, Dict, Optional
import re


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
        chapters = []
        chapters_with_titles = self.detect_chapter_titles(text)

        if not chapters_with_titles:
            # 如果没有检测到章节标题，将整个文本作为一章
            return [{
                "title": "第一章",
                "content": text.strip()
            }]

        # 按章节标题分割文本
        for i, (title, position) in enumerate(chapters_with_titles):
            next_position = chapters_with_titles[i + 1][1] if i + 1 < len(chapters_with_titles) else len(text)
            content = text[position:].strip()
            if i + 1 < len(chapters_with_titles):
                content = text[position:chapters_with_titles[i + 1][1]].strip()

            chapters.append({
                "title": title,
                "content": content.strip()
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
        combined_pattern = '|'.join(self.chapter_patterns)

        for match in re.finditer(combined_pattern, text):
            title = match.group(0)
            position = match.start()

            # 尝试提取完整标题（包括可能的标题后内容）
            end_pos = match.end()
            while end_pos < len(text) and text[end_pos] in ' \t\n':
                end_pos += 1

            # 提取标题行的剩余部分
            line_end = text.find('\n', end_pos)
            if line_end == -1:
                line_end = len(text)

            title_suffix = text[end_pos:line_end].strip()
            full_title = title + ' ' + title_suffix if title_suffix else title

            titles.append((full_title.strip(), position))

        return titles

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

"""小说分析器 - 分析小说内容，提取人物、场景、情节等信息"""

from typing import List, Dict, Optional
import re


class NovelAnalyzer:
    """小说分析器类"""

    def __init__(self):
        """初始化小说分析器"""
        self.character_patterns = [
            r'^[姓名名称][：:]\s*(.+)$',  # 姓名：xxx
            r'^[角色人物][名称称][：:]\s*(.+)$',  # 角色名称：xxx
        ]
        self.location_keywords = [
            '家里', '办公室', '学校', '公园', '街道', '咖啡厅', '餐厅',
            '医院', '车站', '机场', '酒店', '房间', '大厅', '花园'
        ]
        self.time_keywords = [
            '早上', '上午', '中午', '下午', '晚上', '夜晚', '深夜',
            '清晨', '傍晚', '午后', '凌晨', '早晨', '黄昏'
        ]

    def extract_characters(self, chapters: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        提取小说中的人物

        Args:
            chapters: 章节列表

        Returns:
            人物列表，每个元素为 dict，包含 id, name, description 等
        """
        characters = []
        seen_names = set()

        for chapter in chapters:
            content = chapter['content']
            # 简单提取：查找可能的人名
            # 这里使用简单的模式，实际应该使用NER模型
            words = re.findall(r'[一-龥]{1,3}(?:先生|小姐|女士|老师|同学|医生|警察|老板|老板娘)', content)
            for name in words:
                clean_name = name.rstrip('先生小姐女士老师同学医生警察老板老板娘')
                if clean_name and clean_name not in seen_names and len(clean_name) <= 3:
                    seen_names.add(clean_name)
                    characters.append({
                        "id": f"char_{len(characters) + 1:03d}",
                        "name": clean_name,
                        "role": "unknown",
                        "description": "",
                        "aliases": [],
                        "relationships": []
                    })

        return characters

    def extract_scenes(self, chapters: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        提取小说中的场景

        Args:
            chapters: 章节列表

        Returns:
            场景列表，每个元素为 dict，包含 id, title, location, time 等
        """
        scenes = []
        scene_id = 1

        for chapter in chapters:
            content = chapter['content']
            # 简单场景提取：查找地点关键词
            for location in self.location_keywords:
                if location in content:
                    scenes.append({
                        "id": f"scene_{scene_id:03d}",
                        "title": f"{chapter['title']} - {location}",
                        "chapter_ref": chapter['title'],
                        "location": location,
                        "time": "",
                        "date": "",
                        "characters": [],
                        "summary": "",
                        "beats": []
                    })
                    scene_id += 1
                    break  # 每章只提取一个场景

        return scenes

    def analyze_relationships(self, characters: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        分析人物关系

        Args:
            characters: 人物列表

        Returns:
            关系列表，每个元素为 dict，包含人物对和关系类型
        """
        relationships = []

        # 简单关系分析：在同场景中出现的人物可能存在关系
        if len(characters) > 1:
            relationships.append({
                "character1": characters[0]["id"],
                "character2": characters[1]["id"],
                "type": "unknown",
                "description": ""
            })

        return relationships

    def extract_key_events(self, chapters: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        提取关键事件

        Args:
            chapters: 章节列表

        Returns:
            事件列表，每个元素为 dict，包含事件描述、相关人物等
        """
        events = []
        event_keywords = ['发现', '遇见', '得知', '决定', '冲突', '转折', '高潮']

        for chapter in chapters:
            content = chapter['content']
            for keyword in event_keywords:
                if keyword in content:
                    events.append({
                        "id": f"event_{len(events) + 1:03d}",
                        "title": f"{chapter['title']} - {keyword}",
                        "description": f"在{chapter['title']}中提到了{keyword}",
                        "characters": [],
                        "location": "",
                        "time": ""
                    })
                    break

        return events

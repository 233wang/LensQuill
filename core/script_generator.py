"""剧本生成器 - 将小说内容转换为剧本结构"""

from typing import List, Dict, Optional
from datetime import datetime


class ScriptGenerator:
    """剧本生成器类"""

    def __init__(self, llm_api=None):
        """
        初始化剧本生成器

        Args:
            llm_api: LLM API 实例，用于智能生成
        """
        self.llm_api = llm_api

    def generate_scenes(self, chapters: List[Dict[str, str]], analysis: Dict) -> List[Dict[str, str]]:
        """
        生成剧本场景

        Args:
            chapters: 章节列表
            analysis: 小说分析结果

        Returns:
            场景列表
        """
        scenes = []
        scene_id = 1

        for chapter in chapters:
            chapter_scenes = [s for s in analysis.get('scenes', []) if s.get('chapter_ref') == chapter['title']]

            if not chapter_scenes:
                chapter_scenes = [{
                    "id": f"scene_{scene_id:03d}",
                    "title": f"{chapter['title']} - 场景1",
                    "chapter_ref": chapter['title'],
                    "location": "未知地点",
                    "time": "未知时间",
                    "date": "",
                    "characters": [],
                    "summary": "",
                    "beats": []
                }]
                scene_id += 1

            scenes.extend(chapter_scenes)

        return scenes

    def create_beats(self, scene: Dict[str, str]) -> List[Dict[str, str]]:
        """
        创建情节节点

        Args:
            scene: 场景信息

        Returns:
            情节节点列表
        """
        beats = []
        beat_types = ['action', 'dialogue', 'narration']

        for i, beat_type in enumerate(beat_types):
            beats.append({
                "id": f"beat_{i + 1:03d}",
                "type": beat_type,
                "content": "",
                "character": "",
                "speaker_name": "",
                "location_ref": "",
                "time_ref": "",
                "notes": []
            })

        return beats

    def convert_to_script_format(self, chapters: List[Dict[str, str]], analysis: Dict) -> Dict:
        """
        转换为剧本格式

        Args:
            chapters: 章节列表
            analysis: 小说分析结果

        Returns:
            完整剧本对象
        """
        metadata = {
            "version": "1.0",
            "generated_by": "AI Tool v1.0",
            "generated_at": datetime.now().isoformat(),
            "source_files": [],
            "llm_model": "qwen3.6-35b-a3b"
        }

        source = {
            "type": "novel",
            "title": "未知标题",
            "author": "未知作者",
            "chapters_count": len(chapters),
            "chapters": [c['title'] for c in chapters]
        }

        characters = analysis.get('characters', [])

        scenes = self.generate_scenes(chapters, analysis)

        script = {
            "metadata": metadata,
            "source": source,
            "characters": characters,
            "scenes": scenes,
            "beats": [],
            "notes": []
        }

        for scene in scenes:
            scene['beats'] = self.create_beats(scene)
            script['beats'].extend(scene['beats'])

        return script

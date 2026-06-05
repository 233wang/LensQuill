// 章节类型
export interface Chapter {
  title: string
  content: string
}

// 人物类型
export interface Character {
  id: string
  name: string
  role: string
  description: string
  aliases: string[]
  relationships: string[]
}

// 场景类型
export interface Scene {
  id: string
  title: string
  chapter_ref: string
  location: string
  time: string
  date: string
  characters: string[]
  summary: string
  beats: Beat[]
}

// 情节节点类型
export interface Beat {
  id: string
  type: 'action' | 'dialogue' | 'narration' | 'description'
  content: string
  character: string
  speaker_name: string
  location_ref: string
  time_ref: string
  notes: string[]
}

// 分析结果类型
export interface AnalysisResult {
  characters: Character[]
  scenes: Scene[]
  relationships: any[]
  key_events: any[]
}

// 脚本数据类型
export interface ScriptData {
  metadata: {
    version: string
    generated_by: string
    generated_at: string
    source_files: string[]
    llm_model: string
  }
  source: {
    type: string
    title: string
    author: string
    chapters_count: number
    chapters: string[]
  }
  characters: Character[]
  scenes: Scene[]
  beats: Beat[]
  notes: any[]
}

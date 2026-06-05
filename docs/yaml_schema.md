"""YAML Schema 文档

剧本YAML格式定义

本文件定义了AI小说转剧本工具输出的YAML格式结构。
"""

# === YAML Schema 定义 ===

"""
剧本YAML结构：

metadata:              # 元信息
  version: string      # YAML格式版本
  generated_by: string # 生成工具名称
  generated_at: string # 生成时间 (ISO 8601格式)
  source_files: array  # 源文件列表
  llm_model: string    # 使用的LLM模型名称

source:               # 来源信息
  type: string        # 来源类型 (固定为 "novel")
  title: string       # 原小说标题
  author: string      # 原作者
  chapters_count: int # 章节数量
  chapters: array     # 章节标题列表

characters:           # 人物列表
  - id: string        # 人物唯一标识
    name: string      # 人物名称
    role: string      # 角色类型 (protagonist/antagonist/side/other)
    description: string # 人物描述
    aliases: array    # 别名列表
    relationships: array # 关系列表

scenes:               # 场景列表
  - id: string        # 场景唯一标识
    title: string     # 场景标题
    chapter_ref: string # 关联的章节标题
    location: string  # 地点
    time: string      # 时间
    date: string      # 日期
    characters: array # 出场人物ID列表
    summary: string   # 场景摘要
    beats: array      # 情节节点列表

beats:                # 情节节点列表
  - id: string        # 节点唯一标识
    type: string      # 节点类型 (action/dialogue/narration/description)
    content: string   # 内容文本
    character: string # 关联的人物ID
    speaker_name: string # 说话者名称
    location_ref: string # 关联的地点ID
    time_ref: string  # 关联的时间引用
    notes: array      # 备注列表

notes:                # 全局备注列表 (可选)
  - id: string        # 备注唯一标识
    type: string      # 备注类型 (editorial/author/ai)
    content: string   # 备注内容
    referenced_id: string # 关联的ID
    author: string    # 备注作者 (ai/user)
"""

# === 字段类型说明 ===

"""
字段类型定义：

必填字段：
- metadata: object (必填)
- source: object (必填)
- characters: array (必填)
- scenes: array (必填)
- beats: array (必填)

可选字段：
- notes: array (可选)

字符串类型字段：
- version, generated_by, generated_at, source_files[], llm_model
- type, title, author, chapters[]
- id, name, role, description, aliases[], relationships[]
- chapter_ref, location, time, date, characters[], summary
- type, content, character, speaker_name, location_ref, time_ref, notes[]
- type, referenced_id, author

整数类型字段：
- chapters_count

数组类型字段：
- source_files, chapters
- characters, scenes, beats, notes

枚举值字段：
- role: "protagonist" | "antagonist" | "side" | "other"
- type (beats): "action" | "dialogue" | "narration" | "description"
- type (notes): "editorial" | "author" | "ai"
"""

# === 设计原因说明 ===

"""
1. 面向作者编辑
   YAML相比纯文本更结构化，但仍然容易阅读和手动修改，适合小说作者快速编辑。

2. 面向程序解析
   稳定的字段结构便于后续接入：
   - 前端可视化编辑器
   - 剧本导出工具
   - 分镜生成工具
   - 人物关系图
   - 剧情时间线
   - 多轮AI修改

3. 保留小说来源信息
   通过 chapter_ref、source 等字段，可以追踪每个剧本场景来自哪一章小说，
   方便作者对照原文修改。

4. 支持剧本创作流程
   将剧本拆分为 scenes、beats、dialogue、action、narration 等结构，
   更符合剧本创作和影视化改编流程。

5. 支持后续扩展
   Schema允许未来扩展：
   - 分镜字段
   - 镜头语言
   - 情绪标签
   - 场景时长
   - 人物弧光
   - 剧集结构
   - 多版本剧本管理
"""

# === 完整YAML示例 ===

"""
metadata:
  version: "1.0"
  generated_by: "AI Tool v1.0"
  generated_at: "2026-06-05T12:00:00"
  source_files:
    - "examples/input_novel.txt"
  llm_model: "qwen3.6-35b-a3b"

source:
  type: "novel"
  title: "测试小说"
  author: "未知作者"
  chapters_count: 3
  chapters:
    - "第一章 雨夜"
    - "第二章 旧书店"
    - "第三章 真相"

characters:
  - id: "char_001"
    name: "林舟"
    role: "protagonist"
    description: "故事主角，警惕性高"
    aliases: []
    relationships: []

scenes:
  - id: "scene_001"
    title: "雨夜相遇"
    chapter_ref: "第一章 雨夜"
    location: "狭窄的巷子"
    time: "夜晚"
    date: ""
    characters:
      - "char_001"
    summary: "林舟在雨夜遇见神秘女子"
    beats:
      - id: "beat_001"
        type: "action"
        content: "林舟撑着伞，快步穿过狭窄的巷子。"
        character: "char_001"
        speaker_name: ""
        location_ref: ""
        time_ref: ""
        notes: []

beats: []

notes:
  - id: "note_001"
    type: "editorial"
    content: "神秘女孩的身份需要在后续章节中揭示"
    referenced_id: ""
    author: "ai"
"""

# YAML Schema 说明

## 设计理念

本工具采用**按章节整体生成**的策略，而非分别提取人物、场景后拼接。这样可以确保剧本的连贯性和可用性。

### 设计原则

1. **章节完整性** - 每个章节的剧本都是完整的、可独立阅读的单元
2. **结构化输出** - 大模型严格按 Schema 生成 JSON，再转换为 YAML
3. **包含完整剧本要素** - 分镜、场景、对话、动作、特效等

## YAML Schema 定义

```yaml
script:
  # 元信息
  metadata:
    version: "1.0"                    # Schema 版本
    generated_by: "AI Tool v1.0"      # 生成工具
    generated_at: "2026-06-07T12:00:00" # 生成时间
    source_chapters: 3                # 源小说章节数
    llm_model: "astron-code-latest"   # 使用的模型

  # 全局人物列表
  characters:
    - id: "char_001"                  # 人物唯一ID
      name: "白柳"                    # 人物姓名
      role: "protagonist"             # 角色类型 (主角/配角/次要/群演)
      description: "25岁，失业青年，对金钱有强烈渴望..." # 人物描述
      attributes:                     # 人物属性 (可选)
        intelligence: 89
        courage: 50
        luck: 0

  # 剧本主体 - 按章节组织
  chapters:
    - chapter_index: 1                # 章节序号
      chapter_title: "第1章 塞壬小镇" # 章节标题
      source_content_length: 5234    # 源内容长度

      # 本章节的场景列表
      scenes:
        - scene_index: 1             # 场景序号
          scene_title: "醒来"        # 场景标题
          location: "面包车后座"     # 场景地点
          time: "白天"               # 场景时间
          description: |             # 场景描述 (文学性描述)
            白柳醒来，发现自己坐在一辆破旧的面包车后座上。车窗上滑落着不成股的水流，
            鼻腔里萦绕着一丝淡淡的咸鱼腥味。他的面前飘浮着一个面板，上面写着【游戏须知】。

          # 分镜列表 - 剧本的核心部分
          shots:
            - shot_index: 1          # 分镜序号
              shot_type: "内景"       # 分镜类型 (内景/外景/切镜/闪回/淡入/淡出)
              time_of_day: "白天"     # 白天/夜晚/黄昏/黎明
              camera_direction: "中景"  # 镜头方向/景别

              # 动作描述 - 叙述性文字
              action: |
                白柳皱起眉来，手指轻轻敲击着面板边缘。

              # 人物对话 - 对话部分
              dialogue:
                - character: "白柳"
                  line: "这是哪里？我为什么在这里？这个面板又是什么东西？"
                  action_description: "(自言自语)"

              # 场景特效 - 特殊效果
              effects:
                - type: "面板显现"
                  description: "面板上的文字依次显现"

              # 音效
              sound:
                - type: "环境音"
                  description: "细雨淅淅沥沥的声音"

        - scene_index: 2
          scene_title: "人物互动"
          location: "面包车内部"
          time: "白天"
          description: |
            露西转过头来，用热情的笑容打破了车内的沉默。

          shots:
            - shot_index: 1
              shot_type: "中景"
              time_of_day: "白天"
              camera_direction: "平视"

              dialogue:
                - character: "露西"
                  line: "白柳，嘿，我的小甜心，你终于醒了！"
                  action_description: "(对着白柳挤眉弄眼)"

    - chapter_index: 2
      chapter_title: "第2章 塞壬小镇"
      source_content_length: 4892
      scenes:
        # ... 第2章的场景

# 输出说明
output_notes: |
  1. 每个章节独立生成，包含完整的场景和分镜
  2. 分镜是剧本的基本单元，包含动作、对话、特效等要素
  3. 场景按叙事顺序排列
  4. 所有文本使用中文，保持文学性和剧本格式的平衡
```

## 生成流程

```
用户输入小说 (3+章节)
    ↓
按章节分割
    ↓
┌─────────────────────────────────────────┐
│ 对每个章节调用大模型:                    │
│                                         │
│ "请将以下章节内容转换为剧本格式，      │
│  严格遵循 YAML Schema，输出 JSON..."   │
│                                         │
└─────────────────────────────────────────┘
    ↓
大模型返回 JSON (结构化剧本数据)
    ↓
转换为 YAML 格式
    ↓
返回给前端
```

## 大模型 Prompt 模板

```
你是一个专业的剧本创作助手。

【任务】将以下小说章节转换为结构化剧本格式。

【要求】
1. 保留原著的文学性和细节描写
2. 将叙述性内容转换为剧本格式（动作、对话、场景描述）
3. 合理划分场景和分镜
4. 严格遵循以下 Schema:

<schema>
{YAML Schema 定义}
</schema>

【输出格式】
请直接输出 JSON 格式，不要添加任何额外解释。

【小说内容】
{章节原文}
```

## 与旧 Schema 的区别

| 对比项 | 旧 Schema | 新 Schema |
|--------|-----------|-----------|
| 组织方式 | 按类型扁平组织 | 按章节树状组织 |
| 场景生成 | 分别提取后拼接 | 整体生成，保持连贯 |
| 分镜内容 | 空洞的结构占位 | 完整的动作和对话 |
| 可用性 | 需要大量人工编辑 | 可直接使用或微调 |
| 大模型参与 | 部分环节 | 全程参与核心创作 |

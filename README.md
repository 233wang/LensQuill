# AI 小说转剧本工具

将3个章节以上的小说文本自动转换为结构化YAML格式剧本的AI工具。

## 项目简介

本工具帮助小说作者将小说作品改编成剧本。支持自动识别章节结构，**按章节整体生成**剧本，包含分镜设计、人物对话、场景描述、人物动作等完整剧本要素。

### 核心特性

- 支持3个及以上章节的小说输入
- 自动章节解析
- **按章节整体生成剧本** - 每个章节都是完整的、可独立阅读的单元
- AI角色识别与属性定义
- 场景与分镜自动设计
- 包含完整剧本要素：动作、对话、特效、音效
- YAML格式输出
- 可直接编辑使用的剧本初稿

## 技术栈

- 后端: Python + FastAPI
- AI: 讯飞星火API (astron-code-latest)
- 前端: Vue 3 + Pinia + Element Plus
- 数据格式: YAML

## 安装方式

```bash
# 克隆仓库
git clone https://github.com/your-username/ai-novel-to-script.git
cd ai-novel-to-script

# 创建虚拟环境
conda create -n lensquill python=3.9
conda activate lensquill

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑.env文件，填入讯飞星火API密钥
```

## 运行方式

```bash
# 启动后端服务
python -m api.main

# 前端开发服务器
cd frontend
npm install
npm run dev
```

## 项目结构

```
├── core/              # 核心业务逻辑
├── llm/               # LLM集成
├── api/               # Web服务
├── frontend/          # 前端界面
├── cli/               # CLI工具
├── docs/              # 文档
│   └── yaml_schema.md    # YAML Schema 详细说明
├── examples/          # 示例
│   └── input_novel.txt   # 示例小说
├── tests/             # 测试
└── .env               # 环境变量配置
```

## 使用流程

1. **输入小说** - 在首页粘贴3章以上的小说文本
2. **章节预览** - 查看自动分割的章节列表
3. **生成剧本** - 点击"生成剧本"按钮
4. **编辑剧本** - 在YAML编辑器中微调内容
5. **AI对话** - 与AI助手对话，优化剧本细节

## YAML输出格式

输出为结构化YAML格式，包含元信息、人物列表、按章节组织的场景和分镜。

**主要特点：**

- 按章节组织，每个章节包含完整的场景和分镜
- 分镜是剧本的基本单元，包含动作、对话、特效等要素
- 所有文本使用中文，保持文学性和剧本格式的平衡

详见 `docs/yaml_schema.md`。

## 示例

### 输入

```txt
第1章 塞壬小镇

白柳醒来，他发现自己坐在一个车的后座上...
面板上写着【游戏须知】。
...

第2章 塞壬小镇

白柳从车后座探头出来，这是一辆七人座的面包车...
...
```

### 输出

```yaml
script:
  metadata:
    version: "1.0"
    generated_by: "AI Tool v1.0"
    generated_at: "2026-06-07T12:00:00"
    source_chapters: 2
    llm_model: "astron-code-latest"

  characters:
    - id: "char_001"
      name: "白柳"
      role: "protagonist"
      description: "25岁，失业青年，对金钱有强烈渴望..."

  chapters:
    - chapter_index: 1
      chapter_title: "第1章 塞壬小镇"
      scenes:
        - scene_index: 1
          scene_title: "醒来"
          location: "面包车后座"
          shots:
            - shot_index: 1
              shot_type: "内景"
              action: "白柳皱起眉来，手指轻轻敲击着面板边缘。"
              dialogue:
                - character: "白柳"
                  line: "这是哪里？我为什么在这里？"
```

## 开发计划

详见 `docs/design.md` 和 `CLAUDE.md`。

## 贡献指南

欢迎提交Issue和Pull Request！

## 许可证

MIT License

## 联系方式

如有问题，请联系项目维护者。

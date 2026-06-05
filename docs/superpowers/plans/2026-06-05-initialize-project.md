# 项目初始化实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 初始化 AI 小说转剧本工具项目结构，创建基础文件和目录，配置开发环境

**Architecture:** 采用模块化设计，分为 core（核心逻辑）、llm（AI集成）、api（Web服务）、frontend（前端界面）、tests（测试）等模块

**Tech Stack:** Python 3.9+ + FastAPI + Vue 3 + 讯飞星火API

---
## 项目结构

```
ai-novel-to-script/
├── core/              # 核心业务逻辑层
│   ├── __init__.py
│   ├── chapter_parser.py      # 章节解析器
│   ├── novel_analyzer.py      # 小说分析器
│   ├── script_generator.py    # 剧本生成器
│   └── yaml_exporter.py       # YAML导出器
├── llm/               # LLM集成层
│   ├── __init__.py
│   └── xunfei_api.py          # 讯飞星火API集成
├── api/               # FastAPI Web服务层
│   ├── __init__.py
│   ├── main.py                # FastAPI应用入口
│   ├── models.py              # 数据模型
│   └── routes.py              # API路由
├── frontend/          # Vue 3 前端界面
│   ├── package.json
│   └── src/
│       ├── main.js
│       ├── App.vue
│       └── components/
├── cli/               # CLI工具
│   ├── __init__.py
│   └── main.py
├── docs/              # 文档
│   ├── yaml_schema.md
│   └── design.md
├── examples/          # 示例
│   ├── input_novel.txt
│   └── output_script.yaml
├── tests/             # 单元测试
│   ├── __init__.py
│   ├── test_chapter_parser.py
│   ├── test_yaml_exporter.py
│   └── test_novel_analyzer.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Task 1: 创建目录结构

**Files:**
- Create: `core/__init__.py`
- Create: `llm/__init__.py`
- Create: `api/__init__.py`
- Create: `frontend/src/`
- Create: `cli/__init__.py`
- Create: `docs/yaml_schema.md`
- Create: `examples/input_novel.txt`
- Create: `examples/output_script.yaml`
- Create: `tests/__init__.py`

- [ ] **Step 1: 创建项目目录结构**

```bash
cd /home/wangjian/agent_project_test/LensQuill
mkdir -p core llm api cli tests
mkdir -p frontend/src/components
mkdir -p docs examples
touch core/__init__.py llm/__init__.py api/__init__.py cli/__init__.py tests/__init__.py
```

Expected: 目录和空的 `__init__.py` 文件创建成功

- [ ] **Step 2: 验证目录结构**

```bash
find . -type d -name "core" -o -name "llm" -o -name "api" -o -name "cli" -o -name "tests" -o -name "frontend" | sort
```

Expected:
```
./core
./llm
./api
./cli
./tests
./frontend
```

- [ ] **Step 3: 提交目录结构**

```bash
git add .
git commit -m "feat: add project directory structure"
```

Expected: commit 成功

---

## Task 2: 创建 requirements.txt

**Files:**
- Create: `requirements.txt`

- [ ] **Step 1: 创建 requirements.txt**

```bash
cat > requirements.txt << 'EOF'
# Web Framework
fastapi==0.109.0
uvicorn==0.27.0

# AI API Integration
openai==1.10.0
requests==2.31.0

# YAML Processing
pyyaml==6.0.1

# Validation
pydantic==2.5.6
pydantic-settings==2.2.1

# Utilities
python-dotenv==1.0.0
EOF
```

Expected: requirements.txt 文件创建成功

- [ ] **Step 2: 验证 requirements.txt 内容**

```bash
cat requirements.txt
```

Expected: 显示上述内容

- [ ] **Step 3: 提交 requirements.txt**

```bash
git add requirements.txt
git commit -m "feat: add Python dependencies"
```

Expected: commit 成功

---

## Task 3: 创建基础核心模块文件

**Files:**
- Create: `core/chapter_parser.py`
- Create: `core/novel_analyzer.py`
- Create: `core/script_generator.py`
- Create: `core/yaml_exporter.py`

- [ ] **Step 1: 创建章节解析器骨架**

```python
"""章节解析器 - 解析小说文本中的章节结构"""

from typing import List, Dict, Optional


class ChapterParser:
    """章节解析器类"""
    
    def __init__(self):
        """初始化章节解析器"""
        pass
    
    def parse_chapters(self, text: str) -> List[Dict[str, str]]:
        """
        解析小说文本中的章节
        
        Args:
            text: 小说文本内容
            
        Returns:
            章节列表，每个元素为 dict，包含 title 和 content
        """
        pass
    
    def detect_chapter_titles(self, text: str) -> List[str]:
        """
        检测章节标题
        
        Args:
            text: 小说文本内容
            
        Returns:
            章节标题列表
        """
        pass
    
    def split_chapter_content(self, title: str, content: str) -> List[str]:
        """
        拆分章节内容为段落
        
        Args:
            title: 章节标题
            content: 章节内容
            
        Returns:
            段落列表
        """
        pass

- [ ] **Step 2: 创建小说分析器骨架**

```python
"""小说分析器 - 分析小说内容，提取人物、场景、情节等信息"""

from typing import List, Dict, Optional


class NovelAnalyzer:
    """小说分析器类"""
    
    def __init__(self):
        """初始化小说分析器"""
        pass
    
    def extract_characters(self, chapters: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        提取小说中的人物
        
        Args:
            chapters: 章节列表
            
        Returns:
            人物列表，每个元素为 dict，包含 id, name, description 等
        """
        pass
    
    def extract_scenes(self, chapters: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        提取小说中的场景
        
        Args:
            chapters: 章节列表
            
        Returns:
            场景列表，每个元素为 dict，包含 id, title, location, time 等
        """
        pass
    
    def analyze_relationships(self, characters: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        分析人物关系
        
        Args:
            characters: 人物列表
            
        Returns:
            关系列表，每个元素为 dict，包含人物对和关系类型
        """
        pass
    
    def extract_key_events(self, chapters: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        提取关键事件
        
        Args:
            chapters: 章节列表
            
        Returns:
            事件列表，每个元素为 dict，包含事件描述、相关人物等
        """
        pass

- [ ] **Step 3: 创建剧本生成器骨架**

```python
"""剧本生成器 - 将小说内容转换为剧本结构"""

from typing import List, Dict, Optional


class ScriptGenerator:
    """剧本生成器类"""
    
    def __init__(self):
        """初始化剧本生成器"""
        pass
    
    def generate_scenes(self, chapters: List[Dict[str, str]], analysis: Dict) -> List[Dict[str, str]]:
        """
        生成剧本场景
        
        Args:
            chapters: 章节列表
            analysis: 小说分析结果
            
        Returns:
            场景列表
        """
        pass
    
    def create_beats(self, scene: Dict[str, str]) -> List[Dict[str, str]]:
        """
        创建情节节点
        
        Args:
            scene: 场景信息
            
        Returns:
            情节节点列表
        """
        pass
    
    def convert_to_script_format(self, chapters: List[Dict[str, str]], analysis: Dict) -> Dict[str, str]:
        """
        转换为剧本格式
        
        Args:
            chapters: 章节列表
            analysis: 小说分析结果
            
        Returns:
            完整剧本对象
        """
        pass
```

- [ ] **Step 4: 创建YAML导出器骨架**

```python
"""YAML导出器 - 导出YAML格式的剧本"""

from typing import Dict
import yaml


class YamlExporter:
    """YAML导出器类"""
    
    def __init__(self):
        """初始化YAML导出器"""
        pass
    
    def export_yaml(self, data: Dict) -> str:
        """
        导出为YAML格式
        
        Args:
            data: 数据对象
            
        Returns:
            YAML字符串
        """
        pass
    
    def validate_schema(self, data: Dict) -> bool:
        """
        验证数据结构是否符合Schema
        
        Args:
            data: 数据对象
            
        Returns:
            验证结果
        """
        pass
    
    def format_yaml(self, yaml_str: str) -> str:
        """
        格式化YAML字符串
        
        Args:
            yaml_str: YAML字符串
            
        Returns:
            格式化后的YAML字符串
        """
        pass
```

---

## Task 4: 创建 LLM 集成层

**Files:**
- Create: `llm/xunfei_api.py`

- [ ] **Step 1: 创建讯飞星火API集成**

```python
"""讯飞星火API集成 - 调用Qwen3.6-35B-A3B模型"""

import os
import requests
from typing import Dict, List, Optional
from dotenv import load_dotenv

load_dotenv()


class XunFeiAPI:
    """讯飞星火API类"""
    
    def __init__(self):
        """初始化API客户端"""
        self.api_key = os.getenv("XUNFEI_API_KEY")
        self.api_secret = os.getenv("XUNFEI_API_SECRET")
        self.app_id = os.getenv("XUNFEI_APP_ID")
        self.api_url = "https://spark-api.xf-yun.com/v3.5/chat"
    
    def call_llm(self, prompt: str, temperature: float = 0.7) -> str:
        """
        调用LLM生成文本
        
        Args:
            prompt: 提示词
            temperature: 温度参数
            
        Returns:
            生成的文本
        """
        pass
    
    def analyze_novel(self, chapters: List[Dict[str, str]]) -> Dict:
        """
        分析小说内容
        
        Args:
            chapters: 章节列表
            
        Returns:
            分析结果
        """
        pass
    
    def extract_characters(self, text: str) -> List[Dict[str, str]]:
        """
        从文本中提取人物
        
        Args:
            text: 文本内容
            
        Returns:
            人物列表
        """
        pass
    
    def extract_scenes(self, text: str) -> List[Dict[str, str]]:
        """
        从文本中提取场景
        
        Args:
            text: 文本内容
            
        Returns:
            场景列表
        """
        pass
```

- [ ] **Step 2: 创建 .env.example 示例文件**

```bash
cat > .env.example << 'EOF'
# 讯飞星火API配置
XUNFEI_API_KEY=your_api_key_here
XUNFEI_API_SECRET=your_api_secret_here
XUNFEI_APP_ID=your_app_id_here
EOF
```

Expected: .env.example 文件创建成功

---

## Task 5: 创建 FastAPI Web 服务

**Files:**
- Create: `api/main.py`
- Create: `api/models.py`
- Create: `api/routes.py`

- [ ] **Step 1: 创建FastAPI主应用**

```python
"""FastAPI Web服务主应用"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="AI Novel to Script API",
    description="AI小说转剧本工具API",
    version="1.0.0"
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """根路径"""
    return {"message": "AI Novel to Script API"}


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

- [ ] **Step 2: 创建数据模型**

```python
"""API数据模型"""

from pydantic import BaseModel
from typing import List, Dict, Optional


class TextInput(BaseModel):
    """文本输入模型"""
    content: str
    format: str = "text"


class FileInput(BaseModel):
    """文件输入模型"""
    filename: str
    content: str


class Chapter(BaseModel):
    """章节模型"""
    title: str
    content: str


class AnalysisResult(BaseModel):
    """分析结果模型"""
    characters: List[Dict]
    scenes: List[Dict]
    relationships: List[Dict]


class ScriptOutput(BaseModel):
    """剧本输出模型"""
    script: Dict


class YamlExportRequest(BaseModel):
    """YAML导出请求"""
    script: Dict


class YamlExportResponse(BaseModel):
    """YAML导出响应"""
    yaml: str

- [ ] **Step 1: 验证项目结构**

```bash
tree . -I 'venv|env|.git'
```

Expected: 显示完整的项目结构

- [ ] **Step 2: 检查git状态**

```bash
git status
```

Expected: 显示所有待提交的文件

- [ ] **Step 3: 提交所有更改**

```bash
git add .
git commit -m "feat: initialize project structure

- Add project directory structure
- Add Python dependencies
- Add core module skeletons
- Add LLM integration
- Add FastAPI web service
- Add example files
- Add README documentation"
```

- [ ] **Step 4: 推送到远程仓库**

```bash
git push origin feature/design-phase
```

---

## 执行完成

项目初始化完成！现在可以：

1. 创建PR合并到主分支
2. 开始核心功能开发
3. 配置CI/CD
4. 编写单元测试

---

**计划完成时间:** 约30-45分钟  
**下一个分支:** `feature/core-modules`

# Vue 3 前端开发实现计划

> For agentic workers: REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (- [ ]) syntax for tracking.

**Goal:** 创建 Vue 3 前端界面，实现小说上传、章节预览、YAML 编辑器和剧本导出功能

**Architecture:** 
- Vue 3 + Composition API + TypeScript
- Vue Router 实现页面路由
- Pinia 实现状态管理
- CodeMirror 实现 YAML 代码编辑器
- axios 与后端 FastAPI API 通信

**Tech Stack:**
- Vue 3.3+ (Vite 构建)
- TypeScript
- Vue Router 4+
- Pinia 2+
- CodeMirror 6 (js-yaml for YAML parsing)
- axios

**Current API Endpoints:**
- POST /api/upload - 上传小说文本
- POST /api/analyze - 分析小说内容
- POST /api/generate - 生成剧本
- POST /api/export - 导出 YAML

**Project Structure:**
frontend/src/assets  # 静态资源
frontend/src/components  # 可复用组件
frontend/src/router  # 路由配置
frontend/src/stores  # Pinia 状态管理
frontend/src/views  # 页面组件
frontend/src/api  # API 调用封装
frontend/src/types  # TypeScript 类型定义
frontend/src/main.ts  # 入口文件
frontend/index.html
frontend/package.json
frontend/tsconfig.json
frontend/vite.config.ts

---

### Task 1: 初始化 Vue 3 项目

**Files:**
- Create: `frontend/package.json`
- Create: `frontend/vite.config.ts`
- Create: `frontend/tsconfig.json`
- Create: `frontend/index.html`

- [ ] **Step 1: 创建 package.json**

```bash
cd frontend
npm init -y
```

然后编辑 package.json 添加依赖：
```json
{
  "name": "lensquill-frontend",
  "version": "0.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "vue": "^3.3.0",
    "vue-router": "^4.2.0",
    "pinia": "^2.1.0",
    "axios": "^1.4.0",
    "codemirror": "^6.0.0",
    "js-yaml": "^4.1.0",
    "element-plus": "^2.3.0"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^4.2.0",
    "vite": "^4.4.0",
    "typescript": "^5.0.0",
    "@vue/tsconfig": "^0.4.0",
    "autoprefixer": "^10.4.14",
    "tailwindcss": "^3.3.0"
  }
}
```

- [ ] **Step 2: 创建 vite.config.ts**

```typescript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})
```

- [ ] **Step 3: 创建 tsconfig.json**

```json
{
  "extends": "@vue/tsconfig/tsconfig.web.json",
  "include": ["vite.config.ts", "src/**/*", "src/**/*.vue"],
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "references": [
    {
      "path": "./tsconfig.node.json"
    }
  ]
}
```

- [ ] **Step 4: 创建 index.html**

```html
<!DOCTYPE html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" href="/favicon.ico" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title> LensQuill - AI 小说转剧本工具 </title>
  </head>
  <body>
    <div id="app"></div>
    <script type="module" src="/src/main.ts"></script>
  </body>
</html>
```

- [ ] **Step 5: 安装依赖并验证**

```bash
cd frontend
npm install
npm run dev
```

预期: 浏览器打开 http://localhost:3000 显示空白页面

- [ ] **Step 6: 提交**

```bash
git add frontend/package.json frontend/vite.config.ts frontend/tsconfig.json frontend/index.html
git commit -m "chore: 初始化 Vue 3 项目"
git push origin feature/vue3-frontend

### Task 2: 创建基本目录结构和入口文件

**Files:**
- Create: `frontend/src/main.ts`
- Create: `frontend/src/App.vue`
- Create: `frontend/src/router/index.ts`
- Create: `frontend/src/stores/index.ts`
- Create: `frontend/src/types/index.ts`
- Create: `frontend/src/api/client.ts`

- [ ] **Step 1: 创建 main.ts**

```typescript
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(ElementPlus)

app.mount('#app')
```

- [ ] **Step 2: 创建 App.vue**

```vue
<template>
  <div id="app">
    <el-container>
      <el-header>
        <div class="header-content">
          <h1> LensQuill </h1>
          <el-menu
            :default-active="router.currentRoute.value.path"
            mode="horizontal"
            router
          >
            <el-menu-item index="/"> 首页 </el-menu-item>
            <el-menu-item index="/preview"> 预览 </el-menu-item>
            <el-menu-item index="/editor"> 编辑 </el-menu-item>
          </el-menu>
        </div>
      </el-header>
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { RouterLink, RouterView, useRoute } from 'vue-router'
</script>

<style>
#app {
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB',
    'Microsoft YaHei', Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  height: 100vh;
}

body {
  margin: 0;
  padding: 0;
}

.el-header {
  background-color: #409eff;
  color: white;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.header-content h1 {
  margin: 0;
  font-size: 24px;
}

:deep(.el-menu--horizontal) {
  border-bottom: none;
}
</style>
```

- [ ] **Step 3: 创建 router/index.ts**

```typescript
import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Preview from '../views/Preview.vue'
import Editor from '../views/Editor.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home,
    },
    {
      path: '/preview',
      name: 'preview',
      component: Preview,
    },
    {
      path: '/editor',
      name: 'editor',
      component: Editor,
    },
  ],
})

export default router
```

- [ ] **Step 4: 创建 stores/index.ts**

```typescript
import { createPinia } from 'pinia'

export { createPinia }
```

- [ ] **Step 5: 创建 types/index.ts**

```typescript
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
```

- [ ] **Step 6: 创建 api/client.ts**

```typescript
import axios from 'axios'

const apiClient = axios.create({
  baseURL: '/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 上传文本
export const uploadText = (content: string, format = 'text', filename = '') =>
  apiClient.post('/upload', { content, format, filename })

// 分析小说
export const analyzeNovel = (chapters: Chapter[]) =>
  apiClient.post('/analyze', chapters)

// 生成剧本
export const generateScript = (chapters: Chapter[], analysis?: any) =>
  apiClient.post('/generate', { chapters, analysis })

// 导出 YAML
export const exportToYaml = (script: any) =>
  apiClient.post('/export', { script })

export default apiClient
```

- [ ] **Step 7: 创建 views/Home.vue (占位)**

```vue
<template>
  <div class="home">
    <h2> 欢迎使用 LensQuill </h2>
    <p> 将您的小说转换为剧本 </p>
  </div>
</template>

<script setup lang="ts">
</script>
```

- [ ] **Step 8: 创建 views/Preview.vue (占位)**

```vue
<template>
  <div class="preview">
    <h2> 章节预览 </h2>
  </div>
</template>

<script setup lang="ts">
</script>
```

- [ ] **Step 9: 创建 views/Editor.vue (占位)**

```vue
<template>
  <div class="editor">
    <h2> YAML 编辑器 </h2>
  </div>
</template>

<script setup lang="ts">
</script>
```

- [ ] **Step 10: 提交**

```bash
git add frontend/src frontend/views
git commit -m "feat: 添加基础目录结构和路由"
git push origin feature/vue3-frontend

### Task 3: 实现首页（输入界面）

**Files:**
- Create: `frontend/src/views/Home.vue`

- [ ] **Step 1: 实现 Home.vue**

```vue
<template>
  <div class="home">
    <el-card class="input-card">
      <template #header>
        <div class="card-header">
          <span> 输入小说 </span>
          <el-radio-group v-model="inputMethod" size="small">
            <el-radio-button label="paste"> 粘贴文本 </el-radio-button>
            <el-radio-button label="upload"> 上传文件 </el-radio-button>
          </el-radio-group>
        </div>
      </template>

      <div v-if="inputMethod === 'paste'">
        <el-input
          v-model="textContent"
          type="textarea"
          :rows="20"
          placeholder="粘贴小说文本（至少包含3个章节）"
          style="width: 100%; font-family: monospace"
        />
      </div>

      <div v-if="inputMethod === 'upload'">
        <el-upload
          v-model:file-list="fileList"
          :auto-upload="false"
          :show-file-list="true"
          accept=".txt,.md"
          :on-change="handleFileChange"
        >
          <el-button type="primary"> 点击上传 </el-button>
        </el-upload>
        <div v-if="selectedFile" class="file-info">
          已选择: {{ selectedFile.name }}
        </div>
      </div>

      <div class="actions">
        <el-button
          type="primary"
          :disabled="!canSubmit"
          @click="handleProcess"
          loading="processing"
        >
          开始处理
        </el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'
import { uploadText } from '@/api/client'

const router = useRouter()
const inputMethod = ref<'paste' | 'upload'>('paste')
const textContent = ref('')
const fileList = ref<any[]>([])
const selectedFile = ref<File | null>(null)
const processing = ref(false)

const canSubmit = computed(() => {
  if (inputMethod.value === 'paste') {
    return textContent.value.trim().length > 100
  }
  return selectedFile.value !== null
})

const handleFileChange = (file: any) => {
  selectedFile.value = file.raw
}

const handleProcess = async () => {
  processing.value = true
  try {
    let content = ''
    let filename = ''

    if (inputMethod.value === 'paste') {
      content = textContent.value
      filename = 'novel.txt'
    } else if (selectedFile.value) {
      content = await readFileAsText(selectedFile.value)
      filename = selectedFile.value.name
    }

    // 上传文本
    const uploadResponse = await uploadText(content, 'file', filename)
    
    // 保存到临时状态供预览页使用
    localStorage.setItem('novelContent', content)
    localStorage.setItem('filename', filename)

    ElMessage.success('文本上传成功')
    router.push('/preview')
  } catch (error) {
    ElMessage.error('处理失败，请重试')
    console.error(error)
  } finally {
    processing.value = false
  }
}

const readFileAsText = (file: File): Promise<string> => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onload = (e) => resolve(e.target?.result as string)
    reader.onerror = (e) => reject(e)
    reader.readAsText(file, 'gbk')
  })
}
</script>

<style scoped>
.home {
  max-width: 900px;
  margin: 0 auto;
}

.input-card {
  margin-top: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.actions {
  margin-top: 20px;
  text-align: center;
}

.file-info {
  margin-top: 10px;
  color: #666;
}
</style>
```

- [ ] **Step 2: 提交**

```bash
git add frontend/src/views/Home.vue
git commit -m "feat: 实现首页输入界面"
git push origin feature/vue3-frontend

### Task 4: 实现预览页（章节列表）

**Files:**
- Create: `frontend/src/views/Preview.vue`

- [ ] **Step 1: 实现 Preview.vue**

```vue
<template>
  <div class="preview">
    <el-card>
      <template #header>
        <div class="card-header">
          <span> 章节预览 </span>
          <el-button type="primary" @click="handleGenerate" :loading="generating">
            生成剧本
          </el-button>
        </div>
      </template>

      <div v-if="chapters.length > 0">
        <el-table :data="chapters" style="width: 100%">
          <el-table-column prop="index" label="#" width="80" />
          <el-table-column prop="title" label="章节标题" />
          <el-table-column prop="length" label="字数" width="100" />
        </el-table>

        <div class="summary">
          <p> 总章节数: {{ chapters.length }} </p>
          <p> 总字数: {{ totalLength }} </p>
        </div>
      </div>

      <div v-else-if="loading" class="loading">
        <el-skeleton :rows="5" />
      </div>

      <div v-else class="empty">
        <el-empty description="暂无数据，请从首页上传小说" />
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'
import { uploadText, analyzeNovel, generateScript } from '@/api/client'

const router = useRouter()
const chapters = ref<any[]>([])
const loading = ref(false)
const generating = ref(false)
const novelContent = ref('')

onMounted(() => {
  loadNovelContent()
})

const loadNovelContent = () => {
  novelContent.value = localStorage.getItem('novelContent') || ''
  if (novelContent.value) {
    parseChapters()
  }
}

const parseChapters = () => {
  // 简单的章节解析
  const pattern = /第[零一二三四五六七八九十百千0-9]+[章篇回]/g
  const matches = [...novelContent.value.matchAll(pattern)]
  
  chapters.value = matches.map((match, index) => {
    const start = match.index || 0
    const end = matches[index + 1]?.index || novelContent.value.length
    const content = novelContent.value.substring(start, end)
    return {
      index: index + 1,
      title: match[0],
      length: content.length,
    }
  })
}

const handleGenerate = async () => {
  if (chapters.value.length < 3) {
    ElMessage.warning('至少需要3个章节才能生成剧本')
    return
  }

  generating.value = true
  try {
    // 构建章节对象
    const chapterObjects = chapters.value.map((chap, index) => {
      const pattern = new RegExp(chap.title, 'g')
      const matches = [...novelContent.value.matchAll(pattern)]
      const start = matches[0]?.index || 0
      const end = matches[1]?.index || novelContent.value.length
      const content = novelContent.value.substring(start, end)
      
      return {
        title: chap.title,
        content: content.substring(0, 5000), // 限制长度
      }
    })

    // 生成剧本
    const response = await generateScript(chapterObjects)
    
    // 保存剧本数据
    localStorage.setItem('scriptData', JSON.stringify(response.data.script))

    ElMessage.success('剧本生成成功')
    router.push('/editor')
  } catch (error) {
    ElMessage.error('生成失败，请重试')
    console.error(error)
  } finally {
    generating.value = false
  }
}

const totalLength = computed(() => {
  return chapters.value.reduce((sum, chap) => sum + chap.length, 0)
})
</script>

<style scoped>
.preview {
  max-width: 900px;
  margin: 0 auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.summary {
  margin-top: 20px;
  padding: 15px;
  background: #f5f7fa;
  border-radius: 4px;
}

.summary p {
  margin: 5px 0;
}
</style>
```

- [ ] **Step 2: 提交**

```bash
git add frontend/src/views/Preview.vue
git commit -m "feat: 实现预览页"
git push origin feature/vue3-frontend

### Task 5: 实现编辑页（YAML 编辑器）

**Files:**
- Create: `frontend/src/views/Editor.vue`

- [ ] **Step 1: 实现 Editor.vue**

```vue
<template>
  <div class="editor">
    <el-card>
      <template #header>
        <div class="card-header">
          <span> YAML 编辑器 </span>
          <div>
            <el-button @click="handleDownload"> 下载 YAML </el-button>
            <el-button type="primary" @click="handleSave"> 保存 </el-button>
          </div>
        </div>
      </template>

      <Codemirror
        v-model="yamlContent"
        :options="editorOptions"
        class="editor-container"
      />

      <div class="preview-panel">
        <h3> 预览 </h3>
        <div v-if="scriptData" class="preview-content">
          <el-descriptions :column="2" border>
            <el-descriptions-item label="标题">
              {{ scriptData.source?.title || '未知' }}
            </el-descriptions-item>
            <el-descriptions-item label="章节数">
              {{ scriptData.source?.chapters_count || 0 }}
            </el-descriptions-item>
            <el-descriptions-item label="人物">
              {{ scriptData.characters?.length || 0 }}
            </el-descriptions-item>
            <el-descriptions-item label="场景">
              {{ scriptData.scenes?.length || 0 }}
            </el-descriptions-item>
          </el-descriptions>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { useRoute } from 'vue-router'
import Codemirror from 'vue-codemirror-lite'
import { exportToYaml } from '@/api/client'
import { parse } from 'js-yaml'

const route = useRoute()
const yamlContent = ref('')
const scriptData = ref<any>(null)
const editorOptions = ref({
  lineNumbers: true,
  lineWrapping: true,
  styleActiveLine: true,
  matchBrackets: true,
  indentUnit: 2,
  tabSize: 2,
  mode: 'text/x-yaml',
})

onMounted(() => {
  const storedScript = localStorage.getItem('scriptData')
  if (storedScript) {
    scriptData.value = JSON.parse(storedScript)
    yamlContent.value = scriptData.value
  }
})

const handleDownload = () => {
  const blob = new Blob([yamlContent.value], { type: 'text/yaml' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = 'script.yaml'
  a.click()
  URL.revokeObjectURL(url)
  ElMessage.success('下载成功')
}

const handleSave = async () => {
  try {
    // 验证 YAML 格式
    parse(yamlContent.value)
    
    // 保存到本地存储
    localStorage.setItem('scriptData', yamlContent.value)
    ElMessage.success('保存成功')
  } catch (error) {
    ElMessage.error('YAML 格式无效')
    console.error(error)
  }
}
</script>

<style scoped>
.editor {
  max-width: 1400px;
  margin: 0 auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.editor-container {
  height: 600px;
  margin-bottom: 20px;
}

.preview-panel {
  border-top: 1px solid #eee;
  padding-top: 20px;
}

.preview-content {
  margin-top: 15px;
}
</style>
```

- [ ] **Step 2: 安装 Codemirror 依赖**

```bash
cd frontend
npm install vue-codemirror-lite @codemirror/lang-yaml
```

- [ ] **Step 3: 提交**

```bash
git add frontend/src/views/Editor.vue
git commit -m "feat: 实现 YAML 编辑器页面"
git push origin feature/vue3-frontend

### Task 6: 集成状态管理（Pinia Stores）

**Files:**
- Create: `frontend/src/stores/useInputStore.ts`
- Create: `frontend/src/stores/useScriptStore.ts`

- [ ] **Step 1: 创建 useInputStore.ts**

```typescript
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useInputStore = defineStore('input', () => {
  const novelContent = ref<string>('')
  const filename = ref<string>('')
  const chapters = ref<any[]>([])
  const isProcessing = ref(false)

  function setNovelContent(content: string) {
    novelContent.value = content
  }

  function setFilename(name: string) {
    filename.value = name
  }

  function setChapters(chaptersData: any[]) {
    chapters.value = chaptersData
  }

  function startProcessing() {
    isProcessing.value = true
  }

  function endProcessing() {
    isProcessing.value = false
  }

  function reset() {
    novelContent.value = ''
    filename.value = ''
    chapters.value = []
    isProcessing.value = false
  }

  return {
    novelContent,
    filename,
    chapters,
    isProcessing,
    setNovelContent,
    setFilename,
    setChapters,
    startProcessing,
    endProcessing,
    reset,
  }
})
```

- [ ] **Step 2: 创建 useScriptStore.ts**

```typescript
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { Chapter, Character, Scene, ScriptData } from '@/types'

export const useScriptStore = defineStore('script', () => {
  const scriptData = ref<ScriptData | null>(null)
  const yamlContent = ref<string>('')
  const isGenerating = ref(false)

  function setScriptData(data: ScriptData) {
    scriptData.value = data
  }

  function setYamlContent(content: string) {
    yamlContent.value = content
  }

  function startGenerating() {
    isGenerating.value = true
  }

  function endGenerating() {
    isGenerating.value = false
  }

  function reset() {
    scriptData.value = null
    yamlContent.value = ''
    isGenerating.value = false
  }

  return {
    scriptData,
    yamlContent,
    isGenerating,
    setScriptData,
    setYamlContent,
    startGenerating,
    endGenerating,
    reset,
  }
})
```

- [ ] **Step 3: 更新 main.ts 使用 stores**

```typescript
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import App from './App.vue'
import router from './router'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)
app.use(ElementPlus)

app.mount('#app')
```

- [ ] **Step 4: 提交**

```bash
git add frontend/src/stores/
git commit -m "feat: 添加 Pinia 状态管理 stores"
git push origin feature/vue3-frontend

### Task 7: 集成 impeccable 进行前端界面设计优化

**Files:**
- Review: `frontend/src/App.vue`
- Review: `frontend/src/views/Home.vue`
- Review: `frontend/src/views/Preview.vue`
- Review: `frontend/src/views/Editor.vue`

- [ ] **Step 1: 使用 impeccable 设计首页**

运行 flawless 指令审查和优化首页界面：

```
/impeccable
```

审查点：
- 布局和间距
- 颜色方案
- 输入框样式
- 按钮交互
- 移动端响应式

- [ ] **Step 2: 使用 impeccable 设计预览页**

审查点：
- 表格样式
- 加载状态
- 空状态处理
- 信息层级

- [ ] **Step 3: 使用 impeccable 设计编辑页**

审查点：
- 编辑器对比度
- 面板布局
- 颜色和视觉反馈

- [ ] **Step 4: 应用设计改进**

根据 impeccable 的建议更新 CSS 样式

- [ ] **Step 5: 提交**

```bash
git add frontend/src/views/*.vue frontend/src/App.vue
git commit -m "refactor: 使用 impeccable 优化 UI 设计"
git push origin feature/vue3-frontend

### Task 8: 编写单元测试

**Files:**
- Create: `frontend/src/tests/unit/` (directory)
- Create: `frontend/src/tests/unit/router.spec.ts`
- Create: `frontend/src/tests/unit/stores.spec.ts`

- [ ] **Step 1: 安装测试依赖**

```bash
npm install -D @vue/test-utils @vitejs/plugin-vue vitest jsdom
```

- [ ] **Step 2: 配置 vitest**

在 vite.config.ts 中添加：
```typescript
import { defineConfig } from 'vitest/config'

export default defineConfig({
  // ... 其他配置
  test: {
    environment: 'jsdom',
    globals: true,
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
    },
  },
})
```

- [ ] **Step 3: 编写 router 测试**

```typescript
import { mount } from '@vue/test-utils'
import { createRouter, createWebHistory } from 'vue-router'
import { describe, it, expect } from 'vitest'
import Home from '../views/Home.vue'

describe('Router', () => {
  it('渲染 Home 组件', () => {
    const router = createRouter({
      history: createWebHistory(),
      routes: [{ path: '/', component: Home }],
    })
    const wrapper = mount(Home, {
      global: {
        plugins: [router],
      },
    })
    expect(wrapper.text()).toContain('LensQuill')
  })
})
```

- [ ] **Step 4: 编写 stores 测试**

```typescript
import { setActivePinia, createPinia } from 'pinia'
import { describe, it, expect, beforeEach } from 'vitest'
import { useInputStore } from '../stores/useInputStore'

describe('Input Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('设置 novel content', () => {
    const store = useInputStore()
    store.setNovelContent('test content')
    expect(store.novelContent).toBe('test content')
  })

  it('重置 store', () => {
    const store = useInputStore()
    store.setNovelContent('test')
    store.reset()
    expect(store.novelContent).toBe('')
  })
})
```

- [ ] **Step 5: 运行测试**

```bash
npm run test:unit
```

- [ ] **Step 6: 提交**

```bash
git add frontend/src/tests/
git commit -m "test: 添加单元测试"
git push origin feature/vue3-frontend

### Task 9: 更新文档和 README

**Files:**
- Modify: `frontend/README.md`

- [ ] **Step 1: 创建 frontend/README.md**

```markdown
# LensQuill 前端

AI 小说转剧本工具的 Vue 3 前端界面

## 技术栈

- Vue 3 + TypeScript
- Vite
- Vue Router
- Pinia
- Element Plus
- CodeMirror

## 开发

```bash
cd frontend
npm install
npm run dev
```

## 构建

```bash
npm run build
```

## 预览

```bash
npm run preview
```

## API 配置

默认 API 地址为 `http://localhost:8000/api`，如需修改请编辑 `vite.config.ts`

## 目录结构

```
src/
├── api/          # API 客户端
├── assets/       # 静态资源
├── components/   # 可复用组件
├── router/       # 路由配置
├── stores/       # 状态管理
├── types/        # TypeScript 类型
├── views/        # 页面组件
└── main.ts       # 入口文件
```

- [ ] **Step 2: 更新 docs/design.md**

在设计文档中添加前端开发进度：

```markdown
### 阶段五：前端界面（进行中）
- [x] Vue 3项目搭建
- [x] 页面路由配置
- [x] 组件开发
  - [x] 首页
  - [x] 预览页
  - [x] 编辑页
- [x] YAML编辑器集成
```

- [ ] **Step 3: 提交**

```bash
git add frontend/README.md docs/design.md
git commit -m "docs: 添加前端 README 和更新设计文档"
git push origin feature/vue3-frontend
```

---

- [ ] **Step 2: 更新 docs/design.md**

在设计文档中添加前端开发进度，标记 Vue 3 项目搭建、页面路由配置、组件开发和 YAML 编辑器集成为已完成。

- [ ] **Step 3: 提交**

```bash
git add frontend/README.md docs/design.md
git commit -m "docs: 添加前端 README 和更新设计文档"
git push origin feature/vue3-frontend
```

---

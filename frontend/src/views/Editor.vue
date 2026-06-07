<template>
  <div class="editor">
    <div class="header">
      <h1>YAML 编辑器</h1>
      <div class="actions">
        <el-button @click="handleBack">返回</el-button>
        <el-button @click="handleDownload" icon="Download">
          下载 YAML
        </el-button>
        <el-button type="primary" @click="handleSave" icon="Check">
          保存
        </el-button>
      </div>
    </div>

    <div class="editor-layout">
      <!-- 左侧 YAML 编辑器 -->
      <div class="editor-panel">
        <div class="panel-header">
          <h3>YAML 编辑</h3>
          <span class="panel-hint">实时显示生成进度</span>
        </div>
        <div class="editor-container">
          <textarea
            v-model="yamlContent"
            class="editor-textarea"
            placeholder="YAML 内容将在此处显示..."
            spellcheck="false"
          />
        </div>
      </div>

      <!-- 右侧 AI 对话面板 -->
      <div class="chat-panel">
        <AIChat
          v-model:yaml-content="yamlContent"
          :script-data="scriptData"
          :progress-messages="progressMessages"
          @add-chapter="addChapterToScript"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, watch, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import * as yaml from 'js-yaml'
import { gsap } from 'gsap'
import AIChat from '@/components/AIChat.vue'
import { generateScript } from '@/api/client'

const router = useRouter()
const yamlContent = ref('')
const scriptData = ref<any>(null)
const progressMessages = ref<any[]>([])
const currentChapter = ref(0)

// 加载脚本数据
const loadScriptData = () => {
  const storedScript = localStorage.getItem('scriptData')
  if (storedScript) {
    try {
      const data = JSON.parse(storedScript)
      scriptData.value = data
      yamlContent.value = dumpYaml(data)
    } catch {
      yamlContent.value = storedScript
    }
  }
}

// 转换为 YAML
const dumpYaml = (data: any): string => {
  try {
    return yaml.dump(data)
  } catch {
    return JSON.stringify(data, null, 2)
  }
}

// 追加章节到脚本
const addChapterToScript = (chapter: any) => {
  currentChapter.value++

  // 更新进度消息
  progressMessages.value.push({
    id: Date.now(),
    type: 'chapter_complete',
    chapter: chapter.chapter_title || `第${currentChapter.value}章`,
    timestamp: '刚刚'
  })

  // 如果 scriptData 为空，创建新脚本
  if (!scriptData.value) {
    scriptData.value = {
      metadata: {
        version: "1.0",
        generated_by: "AI Tool v4.0",
        generated_at: new Date().toISOString(),
        source_chapters: 0,
        llm_model: "astron-code-latest"
      },
      characters: [],
      chapters: []
    }
  }

  // 添加章节
  scriptData.value.chapters.push(chapter)
  scriptData.value.metadata.source_chapters = scriptData.value.chapters.length

  // 更新 YAML 内容
  yamlContent.value = dumpYaml(scriptData.value)

  // 保存到 localStorage
  localStorage.setItem('scriptData', yamlContent.value)

  // 滚动编辑器到底部
  const textarea = document.querySelector('.editor-textarea') as HTMLTextAreaElement
  if (textarea) {
    textarea.scrollTop = textarea.scrollHeight
  }
}

// 加载数据
loadScriptData()

// 监听 localStorage 变化（接收其他页面的更新）
const handleStorageChange = (e: StorageEvent) => {
  if (e.key === 'scriptData' && e.newValue) {
    try {
      const data = JSON.parse(e.newValue)
      scriptData.value = data
      yamlContent.value = dumpYaml(data)
    } catch (e) {
      console.error('解析 scriptData 失败:', e)
    }
  }
}

// 连接 SSE 流式生成
const connectSSE = () => {
  console.log('开始连接 SSE...')

  // 从 localStorage 获取 chapters
  const chaptersStr = localStorage.getItem('chapters')
  const chapters = JSON.parse(chaptersStr || '[]')

  console.log('发送 POST 请求触发生成...')

  // 先发送 POST 请求触发生成
  fetch('/api/generate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ chapters, analysis: null })
  }).then(response => {
    if (!response.ok) {
      throw new Error('生成请求失败')
    }
    console.log('生成请求已发送，响应已开始...')

    // 检查内容类型
    const contentType = response.headers.get('content-type')
    console.log('Content-Type:', contentType)

    // 读取流式响应
    const reader = response.body.getReader()
    const decoder = new TextDecoder()

    let buffer = ''

    function readStream(): Promise<void> {
      return reader.read().then(({ done, value }) => {
        if (done) {
          console.log('流式响应完成')
          // 处理剩余缓冲区
          if (buffer.trim()) {
            processSSEBuffer(buffer)
          }
          return
        }

        const chunk = decoder.decode(value, { stream: true })
        console.log('收到原始数据:', chunk.substring(0, 100) + '...')

        buffer += chunk

        // 处理完整的 SSE 消息
        processSSEBuffer(buffer)
        buffer = '' // 简单处理，实际可能需要保留不完整消息

        return readStream()
      })
    }

    function processSSEBuffer(text: string) {
      const lines = text.split('\n')
      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const dataStr = line.substring(6).trim()
          if (dataStr) {
            try {
              const data = JSON.parse(dataStr)
              console.log('解析 SSE 消息:', data.type)

              // 推送到 AI 对话框显示
              progressMessages.value.push(data)

              if (data.type === 'chapter_complete') {
                addChapterToScript(data.chapter)
              }

              if (data.type === 'complete') {
                console.log('剧本生成完成')
              }
            } catch (e) {
              console.error('Parse error:', e, 'data:', dataStr)
            }
          }
        }
      }
    }

    return readStream()
  }).catch(error => {
    console.error('流式生成错误:', error)
  })
}

let sseSource: EventSource | null = null

onMounted(() => {
  window.addEventListener('storage', handleStorageChange)

  // 检查是否有进行中的生成
  const chaptersStr = localStorage.getItem('chapters')
  const scriptStr = localStorage.getItem('scriptData')
  console.log('Editor.vue onMounted:')
  console.log('  chaptersStr:', chaptersStr ? '存在' : '不存在')
  console.log('  scriptStr:', scriptStr ? '存在' : '不存在')

  if (chaptersStr && !scriptStr) {
    console.log('检测到进行中的生成，连接 SSE...')
    // 有章节但没有脚本，说明正在生成，连接 SSE
    connectSSE()
  } else if (scriptStr) {
    console.log('脚本已生成，加载它...')
    // 脚本已生成完毕，加载它
    try {
      scriptData.value = JSON.parse(scriptStr)
      yamlContent.value = dumpYaml(scriptData.value)
    } catch {
      yamlContent.value = scriptStr
      scriptData.value = null
    }
  } else {
    console.log('没有进行中的生成，也没有完成的脚本')
  }

  // 页面进入动画
  gsap.from('.editor .header', {
    y: -30,
    opacity: 0,
    duration: 0.6,
    ease: 'power2.out'
  })
})

onBeforeUnmount(() => {
  window.removeEventListener('storage', handleStorageChange)
  gsap.killTweensOf('.editor .header')
})

const handleBack = () => {
  router.push('/preview')
}

const handleDownload = () => {
  if (!yamlContent.value) {
    ElMessage.warning('没有可下载的内容')
    return
  }
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
  if (!yamlContent.value) {
    ElMessage.warning('YAML 内容不能为空')
    return
  }
  try {
    yaml.load(yamlContent.value)
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
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.header h1 {
  font-size: 28px;
  font-weight: 700;
  color: oklch(95% 0.01 240);
}

.actions {
  display: flex;
  gap: 12px;
}

.editor-layout {
  display: flex;
  gap: 24px;
  min-height: 600px;
}

.editor-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  background-color: oklch(18% 0.01 240);
  border-radius: 12px;
  border: 1px solid oklch(25% 0.01 240);
  overflow: hidden;
}

.panel-header {
  flex-shrink: 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 20px;
  background-color: oklch(15% 0.01 240);
  border-bottom: 1px solid oklch(25% 0.01 240);
}

.panel-header h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: oklch(95% 0.01 240);
}

.panel-hint {
  font-size: 12px;
  color: oklch(70% 0.01 240);
}

.editor-container {
  flex: 1;
  overflow: auto;
}

.editor-textarea {
  width: 100%;
  min-height: 400px;
  background-color: oklch(12% 0.01 240);
  border: none;
  border-radius: 0;
  color: oklch(95% 0.01 240);
  font-family: 'SF Mono', 'Consolas', 'Monaco', monospace;
  font-size: 13px;
  padding: 16px;
  resize: none;
  line-height: 1.6;
}

.editor-textarea:focus {
  outline: none;
}

.chat-panel {
  flex: 1;
  min-width: 350px;
  height: 600px;
  background-color: oklch(18% 0.01 240);
  border-radius: 12px;
  border: 1px solid oklch(25% 0.01 240);
  overflow: hidden;
}

:deep(.el-button) {
  border-radius: 6px;
  font-weight: 600;
}

:deep(.el-button--primary) {
  background: oklch(60% 0.25 250);
  border-color: oklch(60% 0.25 250);
}

:deep(.el-button--primary:hover) {
  background: oklch(65% 0.25 250);
  border-color: oklch(65% 0.25 250);
}
</style>

<template>
  <div class="home">
    <div class="hero">
      <h1>LensQuill</h1>
      <p>AI 小说转剧本工具</p>
      <p class="subtitle">将您的小说文本自动转换为结构化剧本</p>
    </div>

    <div class="input-section">
      <div class="input-card">
        <div class="input-header">
          <span>输入小说</span>
          <el-radio-group v-model="inputMethod" size="small">
            <el-radio-button label="paste">粘贴文本</el-radio-button>
            <el-radio-button label="upload">上传文件</el-radio-button>
          </el-radio-group>
        </div>

        <div v-if="inputMethod === 'paste'" class="paste-input">
          <el-input
            v-model="textContent"
            type="textarea"
            :rows="20"
            placeholder="粘贴小说文本（至少包含3个章节）"
            class="text-area"
          />
          <div class="input-stats">
            <span class="stat-item">
              <span class="stat-label">字数：</span>
              <span class="stat-value">{{ textLength }}</span>
            </span>
            <span class="stat-item">
              <span class="stat-label">章节数：</span>
              <span class="stat-value">{{ estimatedChapters }}</span>
            </span>
          </div>
        </div>

        <div v-if="inputMethod === 'upload'" class="upload-input">
          <el-upload
            v-model:file-list="fileList"
            :auto-upload="false"
            :show-file-list="true"
            accept=".txt,.md"
            :on-change="handleFileChange"
            :limit="1"
          >
            <el-button type="primary" icon="Upload">
              点击上传
            </el-button>
          </el-upload>
          <div v-if="selectedFile" class="file-info">
            <span class="filename">{{ selectedFile.name }}</span>
            <span class="filesize">{{ formatFileSize(selectedFile.size) }}</span>
          </div>
        </div>

        <div class="actions">
          <el-button
            type="primary"
            :disabled="!canSubmit"
            @click="handleProcess"
            :loading="processing"
            size="large"
            icon="Play"
          >
            开始处理
          </el-button>
          <el-button @click="handleExample" size="large">
            使用示例
          </el-button>
        </div>
      </div>
    </div>

    <div class="features">
      <div class="feature-grid">
        <div class="feature-item">
          <div class="feature-icon"> Chapters </div>
          <div class="feature-content">
            <h3>智能章节识别</h3>
            <p>自动检测小说中的章节结构，保持章节顺序一致</p>
          </div>
        </div>
        <div class="feature-item">
          <div class="feature-icon"> Characters </div>
          <div class="feature-content">
            <h3>AI人物分析</h3>
            <p>自动识别人物角色、关系和关键事件</p>
          </div>
        </div>
        <div class="feature-item">
          <div class="feature-icon"> YAML </div>
          <div class="feature-content">
            <h3>结构化输出</h3>
            <p>生成可编辑的 YAML 格式剧本</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { UploadFile } from 'element-plus'
import { useRouter } from 'vue-router'
import { uploadText, generateScript } from '@/api/client'

const router = useRouter()
const inputMethod = ref<'paste' | 'upload'>('paste')
const textContent = ref('')
const fileList = ref<any[]>([])
const selectedFile = ref<File | null>(null)
const processing = ref(false)

const textLength = computed(() => textContent.value.length)
const estimatedChapters = computed(() => {
  const pattern = /第[零一二三四五六七八九十百千0-9]+[章篇回]/g
  const matches = textContent.value.match(pattern)
  return matches ? matches.length : 0
})
const canSubmit = computed(() => {
  if (inputMethod.value === 'paste') {
    return textLength.value > 100
  }
  return selectedFile.value !== null
})

const handleFileChange = (file: UploadFile) => {
  selectedFile.value = file.raw
}

const formatFileSize = (size: number): string => {
  if (size < 1024) return size + ' B'
  if (size < 1024 * 1024) return (size / 1024).toFixed(1) + ' KB'
  return (size / (1024 * 1024)).toFixed(1) + ' MB'
}

const handleExample = () => {
  textContent.value = `第一章 雨夜
林舟撑着伞，快步穿过巷子。
雨点敲打着伞面，发出密集的声响。

第二章 旧书店
转过街角，一家老旧的书店映入眼帘。
招牌上的字迹已经模糊不清。

第三章 真相
推开门，铃铛清脆作响。
柜台后，一个身影缓缓抬起头。
`
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

    const chapters = parseChapters(content)

    if (chapters.length < 3) {
      alert('至少需要3个章节才能生成剧本')
      processing.value = false
      return
    }

    localStorage.setItem('novelContent', content)
    localStorage.setItem('filename', filename)
    localStorage.setItem('chapters', JSON.stringify(chapters))

    router.push('/preview')
  } catch (error) {
    alert('处理失败，请重试')
    console.error(error)
  } finally {
    processing.value = false
  }
}

const parseChapters = (content: string): any[] => {
  const pattern = /第[零一二三四五六七八九十百千0-9]+[章篇回]/g
  const matches = [...content.matchAll(pattern)]

  return matches.map((match, index) => {
    const start = match.index || 0
    const end = matches[index + 1]?.index || content.length
    const chapterContent = content.substring(start, end)

    return {
      title: match[0],
      content: chapterContent,
    }
  })
}

const readFileAsText = (file: File): Promise<string> => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onload = (e) => resolve(e.target?.result as string)
    reader.onerror = (e) => reject(e)
    reader.readAsText(file, 'utf-8')
  })
}
</script>

<style scoped>
.home {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
}

.hero {
  text-align: center;
  margin-bottom: 60px;
}

.hero h1 {
  font-size: 48px;
  font-weight: 800;
  margin-bottom: 16px;
  background: linear-gradient(135deg, oklch(70% 0.25 250) 0%, oklch(75% 0.2 330) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero p {
  font-size: 20px;
  color: oklch(95% 0.01 240);
  margin: 8px 0;
}

.subtitle {
  font-size: 16px;
  color: oklch(70% 0.01 240);
}

.input-section {
  margin-bottom: 60px;
}

.input-card {
  background-color: oklch(18% 0.01 240);
  border: 1px solid oklch(25% 0.01 240);
  border-radius: 16px;
  padding: 32px;
  box-shadow: rgba(0, 0, 0, 0.3) 0px 8px 24px;
}

.input-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid oklch(25% 0.01 240);
}

.input-header span {
  font-size: 20px;
  font-weight: 600;
  color: oklch(95% 0.01 240);
}

.paste-input,
.upload-input {
  margin-bottom: 24px;
}

.text-area {
  font-family: 'SF Mono', 'Consolas', 'Monaco', monospace;
  font-size: 14px;
  background-color: oklch(10% 0.01 240);
  border: 1px solid oklch(25% 0.01 240);
  border-radius: 8px;
  color: oklch(95% 0.01 240);
}

.text-area:deep(textarea) {
  background-color: oklch(10% 0.01 240);
  border-color: oklch(25% 0.01 240);
  color: oklch(95% 0.01 240);
}

.input-stats {
  display: flex;
  gap: 32px;
  margin-top: 16px;
}

.stat-item {
  display: flex;
  flex-direction: column;
}

.stat-label {
  font-size: 12px;
  color: oklch(55% 0.01 240);
  margin-bottom: 4px;
}

.stat-value {
  font-size: 24px;
  font-weight: 700;
  color: oklch(60% 0.25 250);
}

.actions {
  display: flex;
  gap: 16px;
  padding-top: 24px;
  border-top: 1px solid oklch(25% 0.01 240);
}

.action-button {
  flex: 1;
}

.features {
  margin-top: 60px;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.feature-item {
  display: flex;
  gap: 16px;
  padding: 24px;
  background-color: oklch(15% 0.01 240);
  border-radius: 12px;
  border: 1px solid oklch(25% 0.01 240);
  transition: all 0.15s ease-out-quart;
}

.feature-item:hover {
  background-color: oklch(20% 0.01 240);
  transform: translateY(-4px);
}

.feature-icon {
  flex-shrink: 0;
  width: 56px;
  height: 56px;
  background: linear-gradient(135deg, oklch(60% 0.25 250) 0%, oklch(75% 0.2 330) 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 700;
  font-size: 14px;
}

.feature-content h3 {
  font-size: 18px;
  font-weight: 600;
  margin: 0 0 8px 0;
  color: oklch(95% 0.01 240);
}

.feature-content p {
  font-size: 14px;
  color: oklch(70% 0.01 240);
  margin: 0;
  line-height: 1.6;
}

.file-info {
  display: flex;
  gap: 16px;
  align-items: center;
  margin-top: 16px;
  padding: 12px;
  background: oklch(10% 0.01 240);
  border-radius: 8px;
}

.filename {
  color: oklch(60% 0.25 250);
  font-weight: 500;
  flex: 1;
}

.filesize {
  color: oklch(55% 0.01 240);
  font-size: 13px;
}

:deep(.el-button) {
  border-radius: 8px;
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

:deep(.el-radio-button__inner) {
  background-color: oklch(18% 0.01 240);
  border-color: oklch(25% 0.01 240);
  color: oklch(70% 0.01 240);
}

:deep(.el-radio-button__inner:hover) {
  background-color: oklch(22% 0.01 240);
}

:deep(.el-radio-button.is-active .el-radio-button__inner) {
  background-color: oklch(60% 0.25 250);
  border-color: oklch(60% 0.25 250);
  color: white;
}
</style>

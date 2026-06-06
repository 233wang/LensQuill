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

    <el-card class="editor-card" shadow="never">
      <div class="editor-layout">
        <!-- 左侧 YAML 编辑器 -->
        <div class="editor-panel">
          <div class="panel-header">
            <h3>YAML 编辑</h3>
            <span class="panel-hint">可手动编辑 YAML 内容</span>
          </div>
          <div class="editor-container">
            <textarea
              v-model="yamlContent"
              class="editor-textarea"
              placeholder="YAML 内容将在此处显示"
              spellcheck="false"
            />
          </div>
        </div>

        <!-- 右侧 AI 对话面板 -->
        <div class="chat-panel">
          <AIChat v-model:yaml-content="yamlContent" :script-data="scriptData" />
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import * as yaml from 'js-yaml'
import { gsap } from 'gsap'
import AIChat from '@/components/AIChat.vue'

const router = useRouter()
const yamlContent = ref('')
const scriptData = ref<any>(null)

// 页面进入动画
onMounted(() => {
  gsap.from('.editor .header', {
    y: -30,
    opacity: 0,
    duration: 0.6,
    ease: 'power2.out'
  })

  gsap.from('.editor-card', {
    y: 30,
    opacity: 0,
    duration: 0.6,
    delay: 0.2,
    ease: 'power2.out'
  })
})

// 页面离开清理
onBeforeUnmount(() => {
  gsap.killTweensOf('.editor .header')
  gsap.killTweensOf('.editor-card')
})

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

// 加载数据
loadScriptData()

// 监听 YAML 内容变化
watch(yamlContent, (newVal) => {
  localStorage.setItem('scriptData', newVal)
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

.editor-card {
  background-color: oklch(18% 0.01 240);
  border: 1px solid oklch(25% 0.01 240);
  border-radius: 12px;
  overflow: hidden;
}

.editor-layout {
  display: flex;
  gap: 24px;
  height: 600px;
  min-height: 400px;
}

.editor-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  background-color: oklch(15% 0.01 240);
  border-radius: 12px;
  overflow: hidden;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 20px;
  background-color: oklch(18% 0.01 240);
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
  overflow: hidden;
}

.editor-textarea {
  width: 100%;
  height: 100%;
  background-color: oklch(12% 0.01 240);
  border: 1px solid oklch(25% 0.01 240);
  border-radius: 8px;
  color: oklch(95% 0.01 240);
  font-family: 'SF Mono', 'Consolas', 'Monaco', monospace;
  font-size: 13px;
  padding: 16px;
  resize: none;
  line-height: 1.6;
}

.editor-textarea:focus {
  outline: none;
  border-color: oklch(60% 0.25 250);
}

.chat-panel {
  flex: 1;
  min-width: 350px;
  height: 100%;
  background-color: oklch(18% 0.01 240);
  border-radius: 12px;
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

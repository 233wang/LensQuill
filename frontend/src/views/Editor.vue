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

    <el-card class="editor-card">
      <div class="editor-container">
        <YamlEditor v-model="yamlContent" />
      </div>

      <div class="preview-panel">
        <h3>剧本预览</h3>
        <div class="preview-content">
          <el-descriptions v-if="scriptData" :column="2" border>
            <el-descriptions-item label="标题">
              {{ scriptData.source?.title || '未知' }}
            </el-descriptions-item>
            <el-descriptions-item label="章节数">
              {{ scriptData.source?.chapters_count || 0 }}
            </el-descriptions-item>
            <el-descriptions-item label="人物">
              <el-tag v-if="scriptData.characters?.length > 0" type="success" effect="dark">
                {{ scriptData.characters?.length || 0 }}
              </el-tag>
              <span v-else>0</span>
            </el-descriptions-item>
            <el-descriptions-item label="场景">
              <el-tag v-if="scriptData.scenes?.length > 0" type="primary" effect="dark">
                {{ scriptData.scenes?.length || 0 }}
              </el-tag>
              <span v-else>0</span>
            </el-descriptions-item>
          </el-descriptions>

          <div v-if="scriptData?.characters?.length > 0" class="characters-preview">
            <h4>人物列表</h4>
            <div class="characters-list">
              <el-tag
                v-for="char in scriptData.characters.slice(0, 5)"
                :key="char.id"
                class="char-tag"
                effect="dark"
              >
                {{ char.name }}
              </el-tag>
              <el-tag
                v-if="scriptData.characters.length > 5"
                type="info"
                effect="dark"
              >
                +{{ scriptData.characters.length - 5 }} 个
              </el-tag>
            </div>
          </div>

          <div v-if="scriptData?.scenes?.length > 0" class="scenes-preview">
            <h4>场景列表</h4>
            <div class="scenes-list">
              <div
                v-for="scene in scriptData.scenes.slice(0, 3)"
                :key="scene.id"
                class="scene-item"
              >
                <span class="scene-title">{{ scene.title }}</span>
                <span class="scene-location">{{ scene.location }}</span>
              </div>
              <el-link
                v-if="scriptData.scenes.length > 3"
                type="primary"
                @click="handleViewAllScenes"
              >
                查看更多
              </el-link>
            </div>
          </div>
        </div>
      </div>

      <!-- AI 对话面板 -->
      <div class="chat-panel">
        <AIChat />
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import * as yaml from 'js-yaml'
import { gsap } from 'gsap'
import YamlEditor from '@/components/YamlEditor.vue'
import AIChat from '@/components/AIChat.vue'

const router = useRouter()
const yamlContent = ref('')
const scriptData = ref<any>(null)

onMounted(() => {
  // 页面进入动画
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

  // YAML 内容加载动画
  const textarea = document.querySelector('.editor-textarea')
  if (textarea) {
    gsap.from(textarea, {
      opacity: 0,
      duration: 0.5,
      delay: 0.4,
      ease: 'power2.out'
    })
  }

  const storedScript = localStorage.getItem('scriptData')
  if (storedScript) {
    try {
      const data = JSON.parse(storedScript)
      scriptData.value = data
      // 尝试转换为 YAML 格式
      yamlContent.value = dumpYaml(data)
    } catch {
      yamlContent.value = storedScript
    }
  }
})

// 页面离开清理
onBeforeUnmount(() => {
  gsap.killTweensOf('.editor .header')
  gsap.killTweensOf('.editor-card')
  gsap.killTweensOf('.editor-textarea')
})

const dumpYaml = (data: any): string => {
  try {
    return yaml.dump(data)
  } catch {
    // 如果解析失败，使用简单的格式化
    return JSON.stringify(data, null, 2)
  }
}

const handleBack = () => {
  router.push('/preview')
}

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
    yaml.load(yamlContent.value)
    localStorage.setItem('scriptData', yamlContent.value)
    ElMessage.success('保存成功')
  } catch (error) {
    ElMessage.error('YAML 格式无效')
    console.error(error)
  }
}

const handleViewAllScenes = () => {
  ElMessage.info('场景列表预览功能')
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

.editor-container {
  padding: 0;
  height: 600px;
}

.preview-panel {
  border-top: 1px solid oklch(25% 0.01 240);
  padding: 20px;
  background: oklch(15% 0.01 240);
}

.preview-panel h3 {
  font-size: 18px;
  font-weight: 600;
  margin: 0 0 16px 0;
  color: oklch(95% 0.01 240);
}

.characters-list,
.scenes-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 12px;
}

.char-tag {
  border-radius: 4px;
  font-weight: 500;
}

.scene-item {
  display: flex;
  flex-direction: column;
  padding: 8px 12px;
  background: oklch(20% 0.01 240);
  border-radius: 6px;
  font-size: 13px;
  border: 1px solid oklch(25% 0.01 240);
}

.scene-title {
  font-weight: 500;
  color: oklch(70% 0.01 240);
}

.scene-location {
  font-size: 11px;
  color: oklch(55% 0.01 240);
}

h4 {
  font-size: 14px;
  font-weight: 600;
  margin: 16px 0 8px 0;
  color: oklch(95% 0.01 240);
}

:deep(.el-button) {
  border-radius: 6px;
  font-weight: 600;
}

:deep(.el-tag--dark) {
  border-radius: 4px;
}

.chat-panel {
  height: 400px;
  margin-top: 24px;
}
</style>

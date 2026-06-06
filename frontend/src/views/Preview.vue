<template>
  <div class="preview">
    <div class="header">
      <h1>章节预览</h1>
      <div class="actions">
        <el-button @click="handleBack">返回</el-button>
        <el-button type="primary" :disabled="chapters.length < 3" @click="handleGenerate" :loading="generating">
          生成剧本
        </el-button>
      </div>
    </div>

    <div class="summary-card">
      <el-descriptions :column="3" border>
        <el-descriptions-item label="总章节数">
          <el-tag v-if="chapters.length >= 3" type="success" effect="dark">
            {{ chapters.length }}
          </el-tag>
          <el-tag v-else type="warning" effect="dark">
            {{ chapters.length }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="总字数">
          {{ totalLength }}
        </el-descriptions-item>
        <el-descriptions-item label="处理状态">
          <el-tag v-if="chapters.length >= 3" type="success" effect="dark">
            就绪
          </el-tag>
          <el-tag v-else type="warning" effect="dark">
            需至少3章
          </el-tag>
        </el-descriptions-item>
      </el-descriptions>
    </div>

    <el-card class="chapters-card">
      <el-table
        v-if="chapters.length > 0"
        :data="chapters"
        style="width: 100%"
        border
      >
        <el-table-column prop="index" label="序号" width="80" align="center" />
        <el-table-column prop="title" label="章节标题" />
        <el-table-column prop="length" label="字数" width="100" align="center" />
        <el-table-column prop="preview" label="预览" width="200">
          <template #default="{ row }">
            <span class="preview-text">{{ row.preview }}</span>
          </template>
        </el-table-column>
      </el-table>

      <div v-else-if="loading" class="loading">
        <el-skeleton :rows="5" />
      </div>

      <div v-else class="empty">
        <el-empty description="暂无数据，请从首页上传小说">
          <el-button type="primary" @click="handleBack">返回首页</el-button>
        </el-empty>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { generateScript } from '@/api/client'

const router = useRouter()
const chapters = ref<any[]>([])
const loading = ref(false)
const generating = ref(false)
const novelContent = ref('')

const loadChapters = () => {
  const storedContent = localStorage.getItem('novelContent')
  const storedChapters = localStorage.getItem('chapters')

  if (storedChapters) {
    chapters.value = JSON.parse(storedChapters)
    novelContent.value = localStorage.getItem('novelContent') || ''
  } else if (storedContent) {
    novelContent.value = storedContent
    parseChapters(storedContent)
  } else {
    chapters.value = []
    novelContent.value = ''
  }
}

loadChapters()

const parseChapters = (content: string) => {
  const pattern = /第[零一二三四五六七八九十百千0-9]+[章篇回]/g
  const matches = [...content.matchAll(pattern)]

  chapters.value = matches.map((match, index) => {
    const start = match.index || 0
    const end = matches[index + 1]?.index || content.length
    const chapterContent = content.substring(start, end)

    return {
      index: index + 1,
      title: match[0],
      length: chapterContent.length,
      preview: chapterContent.substring(0, 30) + '...',
    }
  })

  localStorage.setItem('chapters', JSON.stringify(chapters.value))
}

const handleBack = () => {
  router.push('/')
}

const handleGenerate = async () => {
  if (chapters.value.length < 3) {
    alert('至少需要3个章节才能生成剧本')
    return
  }

  generating.value = true
  try {
    const chapterObjects = chapters.value.map((chap) => ({
      title: chap.title,
      content: chap.content || '',
    }))

    const response = await generateScript(chapterObjects, null)

    if (response.data && response.data.status === 'success') {
      localStorage.setItem('scriptData', JSON.stringify(response.data.script))
      alert('剧本生成成功')
      router.push('/editor')
    } else {
      alert('生成失败：' + (response.data?.message || '未知错误'))
    }
  } catch (error: any) {
    const errorMessage = error?.response?.data?.message || '生成失败，请重试'
    alert(errorMessage)
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
  max-width: 1000px;
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

.summary-card {
  margin-bottom: 24px;
}

.chapters-card {
  background-color: oklch(18% 0.01 240);
  border: 1px solid oklch(25% 0.01 240);
  border-radius: 12px;
  overflow: hidden;
}

.loading {
  padding: 40px;
}

.empty {
  padding: 60px 20px;
  text-align: center;
}

.preview-text {
  color: oklch(70% 0.01 240);
  font-size: 13px;
}

:deep(.el-tag--dark) {
  border-radius: 6px;
}
</style>

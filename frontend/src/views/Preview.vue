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

    <!-- 统计信息卡片 -->
    <div class="summary-card">
      <el-card shadow="never">
        <div class="summary-grid">
          <div class="summary-item">
            <div class="summary-label">总章节数</div>
            <div class="summary-value">
              <el-tag :type="chapters.length >= 3 ? 'success' : 'warning'" effect="dark">
                {{ chapters.length }}
              </el-tag>
              <span class="summary-subtext" v-if="chapters.length < 3">（需至少3章）</span>
            </div>
          </div>
          <div class="summary-item">
            <div class="summary-label">总字数</div>
            <div class="summary-value">
              <span class="summary-number">{{ totalLength }}</span>
              <span class="summary-unit">字</span>
            </div>
          </div>
          <div class="summary-item">
            <div class="summary-label">平均字数</div>
            <div class="summary-value">
              <span class="summary-number">{{ avgLength }}</span>
              <span class="summary-unit">字/章</span>
            </div>
          </div>
          <div class="summary-item">
            <div class="summary-label">处理状态</div>
            <div class="summary-value">
              <el-tag :type="chapters.length >= 3 ? 'success' : 'warning'" effect="dark">
                {{ chapters.length >= 3 ? '就绪' : '需至少3章' }}
              </el-tag>
            </div>
          </div>
        </div>
      </el-card>
    </div>

    <!-- 章节列表卡片 -->
    <el-card class="chapters-card" shadow="never">
      <!-- 章节列表 -->
      <div class="chapter-list" v-if="chapters.length > 0">
        <div class="chapter-item" v-for="(chapter, index) in chapters" :key="chapter.index">
          <div class="chapter-index">
            <span class="index-number">{{ chapter.index }}</span>
          </div>
          <div class="chapter-content">
            <div class="chapter-title">{{ chapter.title }}</div>
            <div class="chapter-meta">
              <span class="meta-item">{{ chapter.length }} 字</span>
              <span class="meta-item">第 {{ chapter.index }} 章</span>
            </div>
            <div class="chapter-preview">
              {{ chapter.preview }}
            </div>
          </div>
        </div>
      </div>

      <!-- 加载状态 -->
      <div v-else-if="loading" class="loading">
        <el-skeleton :rows="5" />
      </div>

      <!-- 空状态 -->
      <div v-else class="empty">
        <el-empty description="暂无数据，请从首页上传小说">
          <el-button type="primary" @click="handleBack">返回首页</el-button>
        </el-empty>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import { generateScript } from '@/api/client'
import { gsap } from 'gsap'

const router = useRouter()
const chapters = ref<any[]>([])
const loading = ref(false)
const generating = ref(false)
const novelContent = ref('')

// 解析章节
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
      content: chapterContent,
      length: chapterContent.length,
      preview: chapterContent.substring(0, 80) + '...',
    }
  })

  localStorage.setItem('chapters', JSON.stringify(chapters.value))
}

// 加载章节
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

// 初始化加载
onMounted(() => {
  loadChapters()
})

// 页面进入动画
onMounted(() => {
  gsap.from('.preview .header', {
    y: -30,
    opacity: 0,
    duration: 0.6,
    ease: 'power2.out'
  })

  gsap.from('.summary-card', {
    y: 30,
    opacity: 0,
    duration: 0.6,
    delay: 0.2,
    ease: 'power2.out'
  })

  gsap.from('.chapters-card', {
    y: 30,
    opacity: 0,
    duration: 0.6,
    delay: 0.4,
    ease: 'power2.out'
  })
})

// 页面离开清理
onBeforeUnmount(() => {
  gsap.killTweensOf('.preview .header')
  gsap.killTweensOf('.summary-card')
  gsap.killTweensOf('.chapters-card')
})

// 处理生成剧本按钮点击
const handleGenerate = async () => {
  if (chapters.value.length < 3) {
    alert('至少需要3个章节才能生成剧本')
    return
  }

  // 显示加载动画
  generating.value = true

  try {
    const chapterObjects = chapters.value.map((chap) => ({
      title: chap.title,
      content: chap.content || '',
    }))

    // 显示处理动画
    const card = document.querySelector('.chapters-card')
    if (card) {
      gsap.to(card, {
        opacity: 0.5,
        scale: 0.98,
        duration: 0.3,
        ease: 'power2.inOut'
      })
    }

    // 调用后端 API
    const response = await generateScript(chapterObjects, null)

    // 恢复卡片动画
    if (card) {
      gsap.from(card, {
        scale: 0.9,
        opacity: 0,
        duration: 0.5,
        ease: 'back.out(1.7)'
      })
    }

    if (response && response.status === 'success') {
      // 保存剧本数据
      const scriptData = response.script
      localStorage.setItem('scriptData', JSON.stringify(scriptData))

      // 成功动画
      if (card) {
        gsap.to(card, {
          borderColor: 'oklch(50% 0.3 150)',
          duration: 0.3,
          yoyo: true,
          repeat: 1,
          onComplete: () => {
            // 成功动画完成后再跳转
            router.push('/editor')
          }
        })
      } else {
        router.push('/editor')
      }
    } else {
      alert('生成失败：' + (response?.message || '未知错误'))
    }
  } catch (error: any) {
    const errorMessage = error?.message || '生成失败，请重试'
    alert(errorMessage)
    console.error(error)
  } finally {
    generating.value = false
  }
}

// 计算属性
const totalLength = computed(() => {
  return chapters.value.reduce((sum, chap) => sum + chap.length, 0)
})

const avgLength = computed(() => {
  if (chapters.value.length === 0) return 0
  return Math.round(totalLength.value / chapters.value.length)
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
  margin-bottom: 32px;
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

.summary-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
}

.summary-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.summary-label {
  font-size: 14px;
  color: oklch(70% 0.01 240);
  font-weight: 500;
}

.summary-value {
  display: flex;
  align-items: center;
  gap: 12px;
}

.summary-number {
  font-size: 32px;
  font-weight: 700;
  color: oklch(95% 0.01 240);
}

.summary-unit {
  font-size: 14px;
  color: oklch(70% 0.01 240);
}

.summary-subtext {
  font-size: 12px;
  color: oklch(70% 0.01 240);
}

.chapters-card {
  background-color: oklch(18% 0.01 240);
  border: 1px solid oklch(25% 0.01 240);
  border-radius: 12px;
  overflow: hidden;
}

.chapter-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding: 24px;
}

.chapter-item {
  display: flex;
  gap: 20px;
  padding: 20px;
  background-color: oklch(15% 0.01 240);
  border-radius: 12px;
  border: 1px solid oklch(25% 0.01 240);
  transition: all 0.2s ease;
}

.chapter-item:hover {
  background-color: oklch(20% 0.01 240);
  border-color: oklch(35% 0.01 240);
  transform: translateX(4px);
}

.chapter-index {
  flex-shrink: 0;
  width: 56px;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, oklch(60% 0.25 250) 0%, oklch(75% 0.2 330) 100%);
  border-radius: 12px;
}

.index-number {
  font-size: 24px;
  font-weight: 700;
  color: white;
}

.chapter-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.chapter-title {
  font-size: 18px;
  font-weight: 600;
  color: oklch(95% 0.01 240);
}

.chapter-meta {
  display: flex;
  gap: 24px;
}

.meta-item {
  font-size: 13px;
  color: oklch(70% 0.01 240);
}

.chapter-preview {
  font-size: 14px;
  color: oklch(70% 0.01 240);
  line-height: 1.6;
  opacity: 0.8;
}

.loading {
  padding: 40px;
}

.empty {
  padding: 60px 20px;
  text-align: center;
}

:deep(.el-tag--dark) {
  border-radius: 6px;
}

:deep(.el-card) {
  background-color: transparent;
  border: none;
}

:deep(.el-card__body) {
  padding: 0;
}
</style>

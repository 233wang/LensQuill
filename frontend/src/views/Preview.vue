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
      <!-- 章节列表头部 -->
      <div class="chapter-header">
        <div class="select-all-container">
          <el-checkbox
            v-model="selectAll"
            @change="handleSelectAllChange"
            :indeterminate="selectedChapters.length > 0 && selectedChapters.length < chapters.length"
          >
            全选
          </el-checkbox>
        </div>
        <span class="selected-count">
          已选择: {{ selectedChapters.length }} / {{ chapters.length }} 章
        </span>
      </div>

      <!-- 章节列表 -->
      <div class="chapter-list" v-if="chapters.length > 0">
        <div
          class="chapter-item"
          :class="{ 'selected': selectedChapters.includes(chapter.index) }"
          v-for="(chapter, index) in chapters"
          :key="chapter.index"
        >
          <div class="chapter-checkbox">
            <el-checkbox
              v-model="selectedChapters"
              :label="chapter.index"
              @change="handleSelectionChange"
            />
          </div>
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
import { ref, computed, onMounted, onBeforeUnmount, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { generateScript } from '@/api/client'
import { gsap } from 'gsap'
import { ElMessage } from 'element-plus'

const router = useRouter()
const chapters = ref<any[]>([])
const loading = ref(false)
const generating = ref(false)
const novelContent = ref('')
const selectedChapters = ref<number[]>([])  // 已选择的章节索引

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
		console.log('Preview.vue onMounted')
		nextTick(() => {
			loadChapters()
			console.log('加载章节后，chapters数量:', chapters.value.length)

			// 章节数据加载后，执行动画
			nextTick(() => {
				console.log('执行动画')
				// GSAP 动画结束后会自动保留最终状态，无需额外处理
				gsap.from('.preview .header', {
					y: -30,
					opacity: 0,
					duration: 0.8,
					ease: 'power2.out'
				})

				gsap.from('.summary-card', {
					y: 30,
					opacity: 0,
					duration: 0.8,
					delay: 0.3,
					ease: 'power2.out'
				})

				// 章节列表动画 - 先全部隐藏再显示
				const cards = document.querySelectorAll('.chapter-item')
				console.log('找到章节卡片数量:', cards.length)
				gsap.set(cards, { opacity: 0, y: 30 }) // 初始状态
				cards.forEach((card, index) => {
					gsap.to(card, {
						opacity: 1,
						y: 0,
						duration: 0.6,
						delay: 0.5 + index * 0.1,
						ease: 'power2.out'
					})
				})
			})
		})
	})

	// 切换章节选择
	const toggleChapterSelection = (chapterIndex: number) => {
		const index = selectedChapters.value.indexOf(chapterIndex)
		if (index > -1) {
			selectedChapters.value.splice(index, 1)
		} else {
			selectedChapters.value.push(chapterIndex)
		}
		console.log('已选择章节:', selectedChapters.value)
	}

	// 处理全选变化
	const handleSelectAllChange = (val: boolean) => {
		if (val) {
			selectedChapters.value = chapters.value.map(c => c.index)
		} else {
			selectedChapters.value = []
		}
		console.log('全选变化:', val, selectedChapters.value)
	}

	// 处理单个章节选择变化
	const handleSelectionChange = (val: any) => {
		console.log('单个章节选择变化:', val, selectedChapters.value)
	}

	// 页面离开清理
	onBeforeUnmount(() => {
		gsap.killTweensOf('.preview .header')
		gsap.killTweensOf('.summary-card')
		gsap.killTweensOf('.chapter-list .chapter-item')
	})

// 处理返回按钮
const handleBack = () => {
  router.push('/')
}

// 处理生成剧本按钮点击
const handleGenerate = async () => {
  // 如果没有选择章节，使用全部章节
  const chaptersToProcess = selectedChapters.value.length > 0
    ? chapters.value.filter(c => selectedChapters.value.includes(c.index))
    : chapters.value

  if (chaptersToProcess.length < 1) {
    alert('请选择至少1个章节')
    return
  }

  generating.value = true

  try {
    const chapterObjects = chaptersToProcess.map((chap) => ({
      title: chap.title,
      content: chap.content || '',
    }))

    // 清除旧的脚本数据
    localStorage.removeItem('scriptData')
    localStorage.removeItem('progressMessages')

    // 保存 chapters 到 localStorage 供编辑页使用
    localStorage.setItem('chapters', JSON.stringify(chapterObjects))

    // 立即跳转到编辑页
    router.push('/editor')

    // 发送生成请求（SSE 连接由 Editor.vue 处理）
    const chapterArray = JSON.parse(JSON.stringify(chapterObjects))
    fetch('/api/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ chapters: chapterArray, analysis: null })
    }).then(response => {
      if (!response.ok) {
        throw new Error('生成请求失败')
      }
      console.log('生成请求已发送')
    }).catch(error => {
      console.error('请求失败:', error)
      ElMessage.error('生成失败，请重试')
    })
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

// 全选状态计算属性
const selectAll = computed({
  get: () => {
    if (chapters.value.length === 0) return false
    return selectedChapters.value.length === chapters.value.length
  },
  set: toggleSelectAll
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
  padding: 20px;
  background: linear-gradient(135deg, oklch(20% 0.05 250) 0%, oklch(18% 0.01 240) 100%);
  border-radius: 12px;
  border: 1px solid oklch(25% 0.01 240);
}

.header h1 {
  font-size: 28px;
  font-weight: 700;
  background: linear-gradient(135deg, oklch(95% 0.01 240) 0%, oklch(60% 0.25 250) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.actions {
  display: flex;
  gap: 12px;
}

.summary-card {
  margin-bottom: 24px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
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
  background: linear-gradient(180deg, oklch(18% 0.01 240) 0%, oklch(16% 0.01 240) 100%);
  border: 1px solid oklch(25% 0.01 240);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.chapter-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding: 24px;
}

.chapter-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  margin-bottom: 16px;
  border-bottom: 1px solid oklch(25% 0.01 240);
}

.chapter-header :deep(.el-checkbox) {
  font-size: 14px;
  font-weight: 600;
}

.selected-count {
  font-size: 14px;
  color: oklch(70% 0.01 240);
}

.chapter-item {
  display: flex;
  gap: 16px;
  padding: 20px;
  background: linear-gradient(135deg, oklch(15% 0.01 240) 0%, oklch(18% 0.01 240) 100%);
  border-radius: 12px;
  border: 1px solid oklch(25% 0.01 240);
  transition: all 0.3s ease;
  cursor: pointer;
}

.chapter-item.selected {
  border-color: oklch(60% 0.25 250);
  background: linear-gradient(135deg, oklch(18% 0.05 250) 0%, oklch(20% 0.05 250) 100%);
}

.chapter-checkbox {
  display: flex;
  align-items: center;
  justify-content: center;
  padding-top: 4px;
}

.chapter-item:hover {
  background: linear-gradient(135deg, oklch(20% 0.01 240) 0%, oklch(22% 0.01 240) 100%);
  border-color: oklch(60% 0.25 250);
  transform: translateX(4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.chapter-index {
  flex-shrink: 0;
  width: 64px;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, oklch(60% 0.25 250) 0%, oklch(75% 0.2 330) 100%);
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.index-number {
  font-size: 28px;
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
  font-size: 20px;
  font-weight: 700;
  color: oklch(95% 0.01 240);
  background: linear-gradient(135deg, oklch(95% 0.01 240) 0%, oklch(60% 0.25 250) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
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
  opacity: 0.9;
  padding: 12px;
  background: oklch(12% 0.01 240);
  border-radius: 8px;
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

:deep(.el-button) {
  border-radius: 8px;
  font-weight: 600;
}

:deep(.el-button--primary) {
  background: linear-gradient(135deg, oklch(60% 0.25 250) 0%, oklch(55% 0.25 250) 100%);
  border-color: oklch(60% 0.25 250);
}
</style>

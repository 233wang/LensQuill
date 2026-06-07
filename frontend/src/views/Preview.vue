<template>
  <div class="preview">
    <div class="header">
      <h1>章节预览</h1>
      <div class="actions">
        <el-button @click="handleBack">返回</el-button>
        <!-- 粘贴模式：显示生成剧本按钮（只处理选择的章节，最多5章） -->
        <el-button type="primary" v-if="!isUploadMode" :disabled="chapters.length < 3" @click="handleGenerate" :loading="generating">
          生成剧本
        </el-button>
        <!-- 上传模式：如果章节列表为空（大文件），显示处理全部章节按钮 -->
        <el-button type="primary" v-if="isUploadMode && chapters.length === 0" @click="handleGenerateAll" :loading="generating">
          处理全部章节
        </el-button>
        <!-- 上传模式：如果有章节列表（小文件），显示生成剧本按钮 -->
        <el-button type="primary" v-if="isUploadMode && chapters.length > 0" @click="handleGenerate" :loading="generating">
          生成剧本
        </el-button>
      </div>
    </div>

    <!-- 统计信息卡片 -->
    <div class="summary-card" v-if="!isUploadMode || chapters.length > 0">
      <el-card shadow="never">
        <div class="summary-grid">
          <div class="summary-item">
            <div class="summary-label">总章节数</div>
            <div class="summary-value">
              <el-tag effect="dark">
                {{ chapters.length }}
              </el-tag>
            </div>
          </div>
          <div class="summary-item" v-if="!isUploadMode">
            <div class="summary-label">总字数</div>
            <div class="summary-value">
              <span class="summary-number">{{ totalLength }}</span>
              <span class="summary-unit">字</span>
            </div>
          </div>
          <div class="summary-item" v-if="!isUploadMode">
            <div class="summary-label">平均字数</div>
            <div class="summary-value">
              <span class="summary-number">{{ avgLength }}</span>
              <span class="summary-unit">字/章</span>
            </div>
          </div>
          <div class="summary-item">
            <div class="summary-label">处理状态</div>
            <div class="summary-value">
              <el-tag type="success" effect="dark">
                {{ isUploadMode ? '文件已加载' : '就绪' }}
              </el-tag>
            </div>
          </div>
        </div>
      </el-card>
    </div>

    <!-- 上传模式说明卡片 -->
    <div class="upload-info-card" v-if="isUploadMode && chapters.length === 0">
      <el-card shadow="never" type="info">
        <div class="upload-info-content">
          <h3>大文件检测</h3>
          <p>检测到大文件（{{ Math.round(novelContent.length / 1024) }} KB），已加载文件内容。</p>
          <p>由于章节数过多（{{ totalChapterCount }}章），已跳过详细章节列表显示。</p>
          <div class="upload-actions">
            <el-button type="primary" @click="handleGenerateAll" :loading="generating">
              处理全部章节
            </el-button>
            <el-button @click="handleBack">返回</el-button>
          </div>
        </div>
      </el-card>
    </div>

    <!-- 章节列表卡片 -->
    <el-card class="chapters-card" shadow="never" v-if="!isUploadMode || (isUploadMode && chapters.length > 0)">
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
      <div class="chapter-list" v-if="chapters.length > 0 && !isUploadMode">
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

    <!-- 上传模式：处理全部章节按钮 -->
    <div class="upload-process-all" v-if="isUploadMode && chapters.length === 0">
      <el-button type="primary" @click="handleGenerateAll" :loading="generating" size="large">
        处理全部章节
      </el-button>
    </div>
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
const selectedFile = ref<File | null>(null)  // 存储上传的文件对象
const isUploadMode = ref(false)  // 标记是否为上传模式
const totalChapterCount = ref(0)  // 总章节数（用于上传模式显示）

// 从 sessionStorage 恢复上传的文件信息
const savedFileInfo = sessionStorage.getItem('uploadedFileInfo')
if (savedFileInfo) {
  try {
    const fileObj = JSON.parse(savedFileInfo)
    selectedFile.value = {
      name: fileObj.name,
      size: fileObj.size,
      type: fileObj.type,
      lastModified: fileObj.lastModified
    } as File
    console.log('恢复文件信息:', selectedFile.value.name)
  } catch (e) {
    console.error('解析文件信息失败:', e)
  }
}

// 解析章节 - 返回解析后的章节数组，不保存到 localStorage（由调用者决定是否保存）
const parseChapters = (content: string): any[] => {
  const pattern = /第[零一二三四五六七八九十百千0-9]+[章篇回]/g
  const matches = [...content.matchAll(pattern)]

  const chapters = matches.map((match, index) => {
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

  return chapters
}

// 加载章节 - 优先从 sessionStorage 读取文件内容（上传模式），其次从 localStorage 读取（粘贴模式）
const loadChapters = () => {
  console.log('开始加载章节...')

  // 尝试从 sessionStorage 读取文件内容（上传模式）
  const savedContent = sessionStorage.getItem('uploadedFileContent')

  if (savedContent && savedContent.length > 0) {
    console.log('上传模式：检测到文件内容')
    isUploadMode.value = true
    novelContent.value = savedContent

    // 从文件内容解析章节数（不加载具体章节内容，避免空间不足）
    try {
      const pattern = /第[零一二三四五六七八九十百千0-9]+[章篇回]/g
      const matches = savedContent.match(pattern)
      if (matches) {
        totalChapterCount.value = matches.length
        console.log('从文件内容解析章节数:', totalChapterCount.value)
      }
    } catch (e) {
      console.error('解析章节数失败:', e)
    }

    // 上传模式下不加载章节列表（大文件会超出 sessionStorage 配额）
    // 用户直接点击"处理全部章节"按钮，按需解析
    chapters.value = []
  } else {
    // 尝试从 localStorage 加载章节信息（粘贴模式）
    const storedChapters = localStorage.getItem('chapters')
    if (storedChapters) {
      try {
        chapters.value = JSON.parse(storedChapters)
        console.log('从 localStorage 加载章节:', chapters.value.length, '个')
        totalChapterCount.value = chapters.value.length
      } catch (e) {
        console.error('解析 localStorage 数据失败:', e)
        chapters.value = []
      }
    } else {
      console.log('没有找到保存的章节数据')
      chapters.value = []
    }
  }
}

// 从文件读取指定章节的内容
const readFileContent = (): Promise<string> => {
  return new Promise((resolve, reject) => {
    // 从 sessionStorage 读取文件内容
    const savedContent = sessionStorage.getItem('uploadedFileContent')
    if (!savedContent) {
      reject(new Error('未找到上传的文件内容'))
      return
    }
    // 创建一个模拟的 File 对象用于兼容
    const blob = new Blob([savedContent], { type: 'text/plain' })
    const reader = new FileReader()
    reader.onload = (e) => resolve(e.target?.result as string)
    reader.onerror = (e) => reject(e)
    reader.readAsText(blob)
  })
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

// 处理生成剧本按钮点击（用于粘贴模式）
const handleGenerate = async () => {
  // 如果是从 sessionStorage 加载的上传文件，不使用此函数（应使用 handleGenerateAll）
  const savedContent = sessionStorage.getItem('uploadedFileContent')
  if (savedContent && savedContent.length > 0) {
    console.log('上传模式：请使用"处理全部章节"按钮')
    return
  }

  // 粘贴模式：直接使用章节数据
  // 如果没有选择章节，使用全部章节
  let chaptersToProcess = selectedChapters.value.length > 0
    ? chapters.value.filter(c => selectedChapters.value.includes(c.index))
    : chapters.value

  // 限制最多处理5章
  const MAX_CHAPTERS = 5
  if (chaptersToProcess.length > MAX_CHAPTERS) {
    alert(`最多只能选择 ${MAX_CHAPTERS} 章进行处理，请取消选择多余的章节`)
    return
  }

  if (chaptersToProcess.length < 1) {
    alert('请选择至少1个章节')
    return
  }

  // 如果章节没有内容，从文件重新读取
  const chaptersWithoutContent = chaptersToProcess.filter(c => !c.content || c.content.length === 0)
  if (chaptersWithoutContent.length > 0 && selectedFile.value) {
    generating.value = true
    try {
      const content = await readFileContent()
      const allChapters = parseChapters(content)
      // 更新章节内容
      chaptersToProcess = chaptersToProcess.map(chap => {
        const fullChapter = allChapters.find(c => c.index === chap.index)
        return fullChapter ? { ...fullChapter, content: fullChapter.content } : chap
      })
    } catch (error) {
      alert('读取文件内容失败: ' + (error?.message || '未知错误'))
      generating.value = false
      return
    } finally {
      generating.value = false
    }
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

    // 根据模式保存 chapters：
    // 上传模式保存到 sessionStorage，粘贴模式保存到 localStorage
    const savedContent = sessionStorage.getItem('uploadedFileContent')
    if (savedContent && savedContent.length > 0) {
      // 上传模式
      sessionStorage.setItem('chapters_in_session', JSON.stringify(chapterObjects))
      console.log('上传模式：保存 chapters 到 sessionStorage')
    } else {
      // 粘贴模式
      localStorage.setItem('chapters', JSON.stringify(chapterObjects))
      console.log('粘贴模式：保存 chapters 到 localStorage')
    }

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

// 处理生成全部章节（用于上传模式）
const handleGenerateAll = async () => {
  // 从 sessionStorage 读取原始文件内容
  const savedContent = sessionStorage.getItem('uploadedFileContent')
  if (!savedContent) {
    alert('文件内容丢失，请重新上传')
    return
  }

  generating.value = true
  try {
    // 解析所有章节
    const allChapters = parseChapters(savedContent)
    console.log('上传模式：解析所有章节', allChapters.length, '个')

    // 限制最多处理5章
    const MAX_CHAPTERS = 5
    if (allChapters.length > MAX_CHAPTERS) {
      const confirmResult = confirm(`检测到 ${allChapters.length} 章，超过限制（最多5章）。\n\n是否只处理前 ${MAX_CHAPTERS} 章？`)
      if (!confirmResult) {
        generating.value = false
        return
      }
      allChapters.length = MAX_CHAPTERS  // 只保留前5章
    }

    // 清除旧的脚本数据
    localStorage.removeItem('scriptData')
    localStorage.removeItem('progressMessages')

    // 保存章节到 sessionStorage
    sessionStorage.setItem('chapters_in_session', JSON.stringify(allChapters))
    console.log('上传模式：保存 chapters 到 sessionStorage')

    // 立即跳转到编辑页
    router.push('/editor')

    // 发送生成请求（SSE 连接由 Editor.vue 处理）
    const chapterArray = JSON.parse(JSON.stringify(allChapters))
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
  set: (val: boolean) => {
    if (val) {
      selectedChapters.value = chapters.value.map(c => c.index)
    } else {
      selectedChapters.value = []
    }
    console.log('全选设置:', val, selectedChapters.value)
  }
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

/* 上传模式大文件提示卡片 */
.upload-info-card {
  margin-bottom: 24px;
}

.upload-info-content h3 {
  margin: 0 0 8px 0;
  font-size: 18px;
  color: oklch(95% 0.01 240);
}

.upload-info-content p {
  margin: 8px 0;
  color: oklch(70% 0.01 240);
  line-height: 1.6;
}

.upload-actions {
  display: flex;
  gap: 12px;
  margin-top: 16px;
}

/* 上传模式处理全部章节按钮 */
.upload-process-all {
  margin-top: 24px;
  text-align: center;
}
</style>

<template>
  <div class="ai-chat">
    <div class="chat-header">
      <h3>AI 剧本打磨助手</h3>
      <el-button type="danger" plain size="small" @click="clearChat">
        清空对话
      </el-button>
    </div>

    <div class="chat-messages" ref="chatContainer">
      <div v-for="msg in messages" :key="msg.id" :class="['message', msg.role]">
        <div class="message-content">
          <div class="message-header">
            <span class="message-author">{{ msg.author }}</span>
            <span class="message-time">{{ msg.timestamp }}</span>
          </div>
          <div class="message-body" v-html="formatMessage(msg.content)"></div>
        </div>
      </div>
      <div v-if="loading" class="message loading">
        <div class="message-content">
          <div class="message-header">
            <span class="message-author">AI 助手</span>
            <span class="message-time">正在思考...</span>
          </div>
          <div class="message-body">
            <div class="typing-indicator">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="chat-input">
      <div class="input-container">
        <textarea
          v-model="userInput"
          class="chat-textarea"
          placeholder="输入您的修改建议或问题..."
          @keydown="handleKeyDown"
          rows="3"
        />
        <div class="input-actions">
          <el-button type="primary" @click="sendMessage" :loading="loading">
            发送
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, nextTick, defineProps, defineEmits } from 'vue'
import { gsap } from 'gsap'
import { generateScript } from '@/api/client'

interface Props {
  yamlContent: string
  scriptData?: any
}

const props = defineProps<Props>()

const emit = defineEmits<{
  (e: 'update:yamlContent', value: string): void
}>()

const messages = ref<any[]>([
  {
    id: 1,
    role: 'assistant',
    author: 'AI 助手',
    content: '您好！我是您的 AI 剧本打磨助手。您可以告诉我需要修改或优化的地方，我会帮您调整剧本内容。',
    timestamp: '刚刚'
  }
])
const userInput = ref('')
const loading = ref(false)
const chatContainer = ref<HTMLElement | null>(null)

const formatMessage = (content: string): string => {
  // 简单的 Markdown 转换
  return content
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    .replace(/\n/g, '<br>')
}

const sendMessage = async () => {
  const text = userInput.value.trim()
  if (!text || loading.value) return

  const userMsg = {
    id: Date.now(),
    role: 'user',
    author: '您',
    content: text,
    timestamp: '刚刚'
  }

  messages.value.push(userMsg)
  userInput.value = ''
  loading.value = true

  // 滚动到底部
  await nextTick()
  scrollToBottom()

  // 调用后端 API 获取 AI 修改建议
  try {
    const response = await generateScript([], { yaml: props.yamlContent, request: text })

    // 模拟 AI 响应
    setTimeout(() => {
      const aiResponse = {
        id: Date.now() + 1,
        role: 'assistant',
        author: 'AI 助手',
        content: `我理解您的需求。关于"${text.substring(0, 20)}..."，我可以帮您优化。\n\n**修改建议：**\n根据您的要求，我建议对剧本进行以下调整：\n\n1. 增加角色情感描写\n2. 优化场景转换衔接\n3. 增强对话表现力\n\n您觉得这些建议如何？我可以继续调整。`,
        timestamp: '刚刚'
      }
      messages.value.push(aiResponse)
      loading.value = false
      scrollToBottom()

      // 消息进入动画
      gsap.from('.message:last-child', {
        y: 20,
        opacity: 0,
        duration: 0.4,
        ease: 'power2.out'
      })
    }, 1000)
  } catch (error) {
    const aiResponse = {
      id: Date.now() + 1,
      role: 'assistant',
      author: 'AI 助手',
      content: `抱歉，暂时无法处理您的请求。错误信息：${error}`,
      timestamp: '刚刚'
    }
    messages.value.push(aiResponse)
    loading.value = false
    scrollToBottom()
  }
}

const scrollToBottom = () => {
  if (chatContainer.value) {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight
  }
}

// 处理键盘事件：回车发送，shift+回车换行
const handleKeyDown = (e: KeyboardEvent) => {
  if (e.key === 'Enter') {
    if (e.shiftKey) {
      // shift+回车：换行
      return
    } else {
      // 回车：发送消息
      e.preventDefault()
      sendMessage()
    }
  }
}

const clearChat = () => {
  messages.value = [
    {
      id: Date.now(),
      role: 'assistant',
      author: 'AI 助手',
      content: '对话已清空。欢迎重新开始打磨剧本！',
      timestamp: '刚刚'
    }
  ]
}

onMounted(() => {
  scrollToBottom()

  // 首条消息动画
  gsap.from('.message:first-child .message-content', {
    y: 20,
    opacity: 0,
    duration: 0.5,
    delay: 0.2,
    ease: 'power2.out'
  })
})
</script>

<style scoped>
.ai-chat {
  display: flex;
  flex-direction: column;
  height: 100%;
  background-color: oklch(18% 0.01 240);
  border: 1px solid oklch(25% 0.01 240);
  border-radius: 12px;
  overflow: hidden;
}

.chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  background-color: oklch(15% 0.01 240);
  border-bottom: 1px solid oklch(25% 0.01 240);
}

.chat-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: oklch(95% 0.01 240);
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  scroll-behavior: smooth;
}

.message {
  display: flex;
  flex-direction: column;
  max-width: 80%;
}

.message.user {
  align-self: flex-end;
  align-items: flex-end;
}

.message.assistant {
  align-self: flex-start;
  align-items: flex-start;
}

.message.loading {
  align-self: flex-start;
}

.message-content {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.message-header {
  display: flex;
  gap: 12px;
  font-size: 12px;
  color: oklch(55% 0.01 240);
}

.message-author {
  font-weight: 600;
  color: oklch(60% 0.25 250);
}

.message-time {
  color: oklch(55% 0.01 240);
}

.message-body {
  padding: 12px 16px;
  border-radius: 12px;
  font-size: 14px;
  line-height: 1.6;
  word-wrap: break-word;
}

.message.user .message-body {
  background-color: oklch(60% 0.25 250);
  color: oklch(98% 0 0);
  border-bottom-right-radius: 4px;
}

.message.assistant .message-body {
  background-color: oklch(25% 0.01 240);
  color: oklch(95% 0.01 240);
  border-bottom-left-radius: 4px;
}

.message.assistant strong {
  color: oklch(70% 0.25 250);
}

.typing-indicator {
  display: flex;
  gap: 4px;
  padding: 4px 0;
}

.typing-indicator span {
  width: 6px;
  height: 6px;
  background-color: oklch(70% 0.01 240);
  border-radius: 50%;
  animation: typing 1.4s infinite ease-in-out both;
}

.typing-indicator span:nth-child(1) {
  animation-delay: -0.32s;
}

.typing-indicator span:nth-child(2) {
  animation-delay: -0.16s;
}

@keyframes typing {
  0%, 80%, 100% {
    transform: scale(0);
  }
  40% {
    transform: scale(1);
  }
}

.chat-input {
  padding: 16px 24px;
  background-color: oklch(15% 0.01 240);
  border-top: 1px solid oklch(25% 0.01 240);
}

.input-container {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.input-actions {
  display: flex;
  justify-content: flex-end;
}

.chat-textarea {
  width: 100%;
  min-height: 80px;
  max-height: 120px;
  background-color: oklch(12% 0.01 240);
  border: 1px solid oklch(25% 0.01 240);
  border-radius: 8px;
  color: oklch(95% 0.01 240);
  font-family: 'SF Mono', 'Consolas', 'Monaco', monospace;
  font-size: 14px;
  padding: 12px;
  resize: none;
  line-height: 1.6;
}

.chat-textarea:focus {
  outline: none;
  border-color: oklch(60% 0.25 250);
}

:deep(.el-button) {
  border-radius: 8px;
  font-weight: 600;
}

:deep(.el-button--primary) {
  background-color: oklch(60% 0.25 250);
  border-color: oklch(60% 0.25 250);
}

:deep(.el-button--primary:hover) {
  background-color: oklch(65% 0.25 250);
  border-color: oklch(65% 0.25 250);
}

:deep(.el-button--danger) {
  color: oklch(70% 0.4 25);
  border-color: oklch(70% 0.4 25);
}

:deep(.el-button--danger:hover) {
  background-color: oklch(70% 0.4 25);
  color: white;
  border-color: oklch(70% 0.4 25);
}
</style>

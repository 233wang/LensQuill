import axios from 'axios'
import { ElMessage } from 'element-plus'

const apiClient = axios.create({
  baseURL: '/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
apiClient.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    const message = error.response?.data?.message || error.message || '请求失败'
    ElMessage.error(message)
    return Promise.reject(error)
  }
)

// 上传文本
export const uploadText = (content: string, format = 'text', filename = '') =>
  apiClient.post('/upload', { content, format, filename })

// 分析小说
export const analyzeNovel = (chapters: any[]) =>
  apiClient.post('/analyze', chapters)

// 生成剧本（流式）
export const generateScriptStream = (
  chapters: any[],
  analysis?: any,
  onMessage?: (event: any) => void,
  onError?: (error: Error) => void
) => {
  return new Promise((resolve, reject) => {
    // 使用 POST 请求发送数据，SSE 接收
    const body = { chapters, analysis }

    fetch('/api/generate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body)
    })
      .then(response => {
        if (!response.ok) {
          throw new Error('请求失败')
        }

        // 检查是否是 SSE 响应
        const contentType = response.headers.get('content-type')
        if (!contentType?.includes('text/event-stream')) {
          throw new Error('不是流式响应')
        }

        // 使用 EventSource 接收流式数据
        const eventSource = new EventSource(response.url)

        const results: any[] = []
        let fullScript: any = null

        eventSource.onmessage = (event) => {
          try {
            const data = JSON.parse(event.data)
            results.push(data)

            if (data.type === 'complete' && data.script) {
              fullScript = data.script
              eventSource.close()
              resolve({ status: 'success', script: fullScript, events: results })
            }

            if (onMessage) {
              onMessage(data)
            }
          } catch (e) {
            console.error('Event source parse error:', e)
          }
        }

        eventSource.onerror = (error) => {
          console.error('Event source error:', error)
          eventSource.close()
          reject(new Error('连接错误或超时'))
        }

        // 设置超时
        setTimeout(() => {
          eventSource.close()
          reject(new Error('请求超时'))
        }, 120000) // 2分钟超时
      })
      .catch(error => {
        reject(error)
      })
  })
}

// 导出 YAML
export const exportToYaml = (script: any) =>
  apiClient.post('/export', { script })

export default apiClient

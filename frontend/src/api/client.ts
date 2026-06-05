import axios from 'axios'

const apiClient = axios.create({
  baseURL: '/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 上传文本
export const uploadText = (content: string, format = 'text', filename = '') =>
  apiClient.post('/upload', { content, format, filename })

// 分析小说
export const analyzeNovel = (chapters: any[]) =>
  apiClient.post('/analyze', chapters)

// 生成剧本
export const generateScript = (chapters: any[], analysis?: any) =>
  apiClient.post('/generate', { chapters, analysis })

// 导出 YAML
export const exportToYaml = (script: any) =>
  apiClient.post('/export', { script })

export default apiClient

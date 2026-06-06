import axios from 'axios';
import { ElMessage } from 'element-plus';
const apiClient = axios.create({
    baseURL: '/api',
    timeout: 30000,
    headers: {
        'Content-Type': 'application/json',
    },
});
// Request interceptor
apiClient.interceptors.request.use((config) => {
    return config;
}, (error) => {
    return Promise.reject(error);
});
// Response interceptor
apiClient.interceptors.response.use((response) => {
    return response;
}, (error) => {
    const message = error.response?.data?.message || error.message || '请求失败';
    ElMessage.error(message);
    return Promise.reject(error);
});
// 上传文本
export const uploadText = (content, format = 'text', filename = '') => apiClient.post('/upload', { content, format, filename });
// 分析小说
export const analyzeNovel = (chapters) => apiClient.post('/analyze', chapters);
// 生成剧本
export const generateScript = (chapters, analysis) => apiClient.post('/generate', { chapters, analysis });
// 导出 YAML
export const exportToYaml = (script) => apiClient.post('/export', { script });
export default apiClient;
//# sourceMappingURL=client.js.map
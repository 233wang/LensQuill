declare const apiClient: import("axios").AxiosInstance;
export declare const uploadText: (content: string, format?: string, filename?: string) => Promise<import("axios").AxiosResponse<any, any, {}>>;
export declare const analyzeNovel: (chapters: any[]) => Promise<import("axios").AxiosResponse<any, any, {}>>;
export declare const generateScript: (chapters: any[], analysis?: any) => Promise<import("axios").AxiosResponse<any, any, {}>>;
export declare const exportToYaml: (script: any) => Promise<import("axios").AxiosResponse<any, any, {}>>;
export default apiClient;
//# sourceMappingURL=client.d.ts.map
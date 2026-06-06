export interface Chapter {
    index: number;
    title: string;
    content: string;
    length: number;
    preview?: string;
}
export interface NovelState {
    content: string;
    filename: string;
    chapters: Chapter[];
    characters: any[];
    scenes: any[];
    relationships: any[];
    script: any;
    processing: boolean;
    error: string | null;
}
export declare const useNovelStore: import("pinia").StoreDefinition<"novel", Pick<{
    content: import("vue").Ref<string, string>;
    filename: import("vue").Ref<string, string>;
    chapters: import("vue").Ref<{
        index: number;
        title: string;
        content: string;
        length: number;
        preview?: string | undefined;
    }[], Chapter[] | {
        index: number;
        title: string;
        content: string;
        length: number;
        preview?: string | undefined;
    }[]>;
    characters: import("vue").Ref<any[], any[]>;
    scenes: import("vue").Ref<any[], any[]>;
    relationships: import("vue").Ref<any[], any[]>;
    script: import("vue").Ref<any, any>;
    processing: import("vue").Ref<boolean, boolean>;
    error: import("vue").Ref<string | null, string | null>;
    chapterCount: import("vue").ComputedRef<number>;
    totalLength: import("vue").ComputedRef<number>;
    hasEnoughChapters: import("vue").ComputedRef<boolean>;
    isReadyToGenerate: import("vue").ComputedRef<boolean>;
    setNovelContent: (text: string, fileName?: string) => void;
    setChapters: (chapterList: Chapter[]) => void;
    setAnalysis: (data: any) => void;
    setScript: (data: any) => void;
    startProcessing: () => void;
    stopProcessing: () => void;
    setError: (msg: string) => void;
    clearAll: () => void;
    loadFromLocalStorage: () => void;
    saveToLocalStorage: () => void;
    clearLocalStorage: () => void;
}, "error" | "content" | "filename" | "chapters" | "script" | "characters" | "scenes" | "relationships" | "processing">, Pick<{
    content: import("vue").Ref<string, string>;
    filename: import("vue").Ref<string, string>;
    chapters: import("vue").Ref<{
        index: number;
        title: string;
        content: string;
        length: number;
        preview?: string | undefined;
    }[], Chapter[] | {
        index: number;
        title: string;
        content: string;
        length: number;
        preview?: string | undefined;
    }[]>;
    characters: import("vue").Ref<any[], any[]>;
    scenes: import("vue").Ref<any[], any[]>;
    relationships: import("vue").Ref<any[], any[]>;
    script: import("vue").Ref<any, any>;
    processing: import("vue").Ref<boolean, boolean>;
    error: import("vue").Ref<string | null, string | null>;
    chapterCount: import("vue").ComputedRef<number>;
    totalLength: import("vue").ComputedRef<number>;
    hasEnoughChapters: import("vue").ComputedRef<boolean>;
    isReadyToGenerate: import("vue").ComputedRef<boolean>;
    setNovelContent: (text: string, fileName?: string) => void;
    setChapters: (chapterList: Chapter[]) => void;
    setAnalysis: (data: any) => void;
    setScript: (data: any) => void;
    startProcessing: () => void;
    stopProcessing: () => void;
    setError: (msg: string) => void;
    clearAll: () => void;
    loadFromLocalStorage: () => void;
    saveToLocalStorage: () => void;
    clearLocalStorage: () => void;
}, "chapterCount" | "totalLength" | "hasEnoughChapters" | "isReadyToGenerate">, Pick<{
    content: import("vue").Ref<string, string>;
    filename: import("vue").Ref<string, string>;
    chapters: import("vue").Ref<{
        index: number;
        title: string;
        content: string;
        length: number;
        preview?: string | undefined;
    }[], Chapter[] | {
        index: number;
        title: string;
        content: string;
        length: number;
        preview?: string | undefined;
    }[]>;
    characters: import("vue").Ref<any[], any[]>;
    scenes: import("vue").Ref<any[], any[]>;
    relationships: import("vue").Ref<any[], any[]>;
    script: import("vue").Ref<any, any>;
    processing: import("vue").Ref<boolean, boolean>;
    error: import("vue").Ref<string | null, string | null>;
    chapterCount: import("vue").ComputedRef<number>;
    totalLength: import("vue").ComputedRef<number>;
    hasEnoughChapters: import("vue").ComputedRef<boolean>;
    isReadyToGenerate: import("vue").ComputedRef<boolean>;
    setNovelContent: (text: string, fileName?: string) => void;
    setChapters: (chapterList: Chapter[]) => void;
    setAnalysis: (data: any) => void;
    setScript: (data: any) => void;
    startProcessing: () => void;
    stopProcessing: () => void;
    setError: (msg: string) => void;
    clearAll: () => void;
    loadFromLocalStorage: () => void;
    saveToLocalStorage: () => void;
    clearLocalStorage: () => void;
}, "setNovelContent" | "setChapters" | "setAnalysis" | "setScript" | "startProcessing" | "stopProcessing" | "setError" | "clearAll" | "loadFromLocalStorage" | "saveToLocalStorage" | "clearLocalStorage">>;
//# sourceMappingURL=novel.d.ts.map
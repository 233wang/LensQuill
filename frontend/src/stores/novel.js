import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
export const useNovelStore = defineStore('novel', () => {
    // State
    const content = ref('');
    const filename = ref('');
    const chapters = ref([]);
    const characters = ref([]);
    const scenes = ref([]);
    const relationships = ref([]);
    const script = ref(null);
    const processing = ref(false);
    const error = ref(null);
    // Computed
    const chapterCount = computed(() => chapters.value.length);
    const totalLength = computed(() => content.value.length);
    const hasEnoughChapters = computed(() => chapterCount.value >= 3);
    const isReadyToGenerate = computed(() => hasEnoughChapters.value && content.value.length > 0);
    // Actions
    function setNovelContent(text, fileName = 'novel.txt') {
        content.value = text;
        filename.value = fileName;
    }
    function setChapters(chapterList) {
        chapters.value = chapterList;
    }
    function setAnalysis(data) {
        characters.value = data.characters || [];
        scenes.value = data.scenes || [];
        relationships.value = data.relationships || [];
    }
    function setScript(data) {
        script.value = data;
    }
    function startProcessing() {
        processing.value = true;
        error.value = null;
    }
    function stopProcessing() {
        processing.value = false;
    }
    function setError(msg) {
        error.value = msg;
        stopProcessing();
    }
    function clearAll() {
        content.value = '';
        filename.value = '';
        chapters.value = [];
        characters.value = [];
        scenes.value = [];
        relationships.value = [];
        script.value = null;
        error.value = null;
    }
    function loadFromLocalStorage() {
        const storedContent = localStorage.getItem('novelContent');
        const storedChapters = localStorage.getItem('chapters');
        const storedScript = localStorage.getItem('scriptData');
        if (storedContent)
            content.value = storedContent;
        if (storedChapters)
            chapters.value = JSON.parse(storedChapters);
        if (storedScript)
            script.value = JSON.parse(storedScript);
    }
    function saveToLocalStorage() {
        localStorage.setItem('novelContent', content.value);
        localStorage.setItem('filename', filename.value);
        localStorage.setItem('chapters', JSON.stringify(chapters.value));
        if (script.value) {
            localStorage.setItem('scriptData', JSON.stringify(script.value));
        }
    }
    function clearLocalStorage() {
        localStorage.removeItem('novelContent');
        localStorage.removeItem('filename');
        localStorage.removeItem('chapters');
        localStorage.removeItem('scriptData');
    }
    return {
        // State
        content,
        filename,
        chapters,
        characters,
        scenes,
        relationships,
        script,
        processing,
        error,
        // Computed
        chapterCount,
        totalLength,
        hasEnoughChapters,
        isReadyToGenerate,
        // Actions
        setNovelContent,
        setChapters,
        setAnalysis,
        setScript,
        startProcessing,
        stopProcessing,
        setError,
        clearAll,
        loadFromLocalStorage,
        saveToLocalStorage,
        clearLocalStorage,
    };
});
//# sourceMappingURL=novel.js.map
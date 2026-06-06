import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import Preview from '../views/Preview.vue';
import Editor from '../views/Editor.vue';
const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            name: 'home',
            component: Home,
        },
        {
            path: '/preview',
            name: 'preview',
            component: Preview,
        },
        {
            path: '/editor',
            name: 'editor',
            component: Editor,
        },
    ],
});
export default router;
//# sourceMappingURL=index.js.map
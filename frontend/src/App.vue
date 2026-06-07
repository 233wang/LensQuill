<template>
  <div id="app">
    <el-container>
      <el-header>
        <div class="header-content">
          <h1>LensQuill</h1>
          <el-menu
            :default-active="route.path"
            mode="horizontal"
            router
            class="header-menu"
          >
            <el-menu-item index="/">首页</el-menu-item>
            <el-menu-item index="/preview">预览</el-menu-item>
            <el-menu-item index="/editor">编辑</el-menu-item>
          </el-menu>
        </div>
      </el-header>
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router'

const route = useRoute()
</script>

<style>
#app {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  height: 100vh;
}

body {
  margin: 0;
  padding: 0;
  background-color: oklch(15% 0.01 240);
  color: oklch(95% 0.01 240);
}

.el-header {
  background: linear-gradient(180deg, oklch(18% 0.01 240) 0%, oklch(16% 0.01 240) 100%);
  color: oklch(95% 0.01 240);
  border-bottom: 1px solid oklch(25% 0.01 240);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 100%;
  padding: 0 24px;
}

.header-content h1 {
  margin: 0;
  font-size: 24px;
  font-weight: 700;
  background: linear-gradient(135deg, oklch(95% 0.01 240) 0%, oklch(60% 0.25 250) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.header-menu {
  border-bottom: none;
  background: transparent;
}

:deep(.el-menu-item) {
  color: oklch(70% 0.01 240);
  border-radius: 8px;
  margin: 4px 0;
  transition: all 0.3s ease;
}

:deep(.el-menu-item.is-active) {
  color: oklch(95% 0.01 240);
  background: linear-gradient(135deg, oklch(60% 0.25 250) 0%, oklch(55% 0.25 250) 100%);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

:deep(.el-menu-item:hover) {
  color: oklch(95% 0.01 240);
  background: oklch(22% 0.01 240);
  transform: translateX(4px);
}
</style>

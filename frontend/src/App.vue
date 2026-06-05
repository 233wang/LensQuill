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
  background-color: oklch(18% 0.01 240);
  color: oklch(95% 0.01 240);
  border-bottom: 1px solid oklch(25% 0.01 240);
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 100%;
}

.header-content h1 {
  margin: 0;
  font-size: 24px;
  font-weight: 700;
  color: oklch(95% 0.01 240);
}

.header-menu {
  border-bottom: none;
}

:deep(.el-menu-item) {
  color: oklch(70% 0.01 240);
}

:deep(.el-menu-item.is-active) {
  color: oklch(60% 0.25 250);
  background-color: oklch(20% 0.05 250);
}

:deep(.el-menu-item:hover) {
  background-color: oklch(22% 0.01 240);
}
</style>

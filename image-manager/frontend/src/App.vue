<template>
  <el-container style="height: 100vh;">
    <el-header style="display: flex; align-items: center; background: #fff; border-bottom: 1px solid #eee;">
      <h2 style="margin: 0;">🖼️ Image Manager</h2>
    </el-header>
    <el-main>
      <ImageManager />
    </el-main>
  </el-container>
</template>

<script setup>
import ImageManager from './views/ImageManager.vue'
</script>
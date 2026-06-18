<script setup>
import { RouterView } from 'vue-router'
import AppHeader from '@/components/layout/AppHeader.vue'
</script>

<template>
  <div class="public-layout">
    <header class="public-header">
      <AppHeader />
    </header>

    <main class="public-main">
      <RouterView />
    </main>
  </div>
</template>

<style scoped>
.public-layout {
  min-height: 100vh;
  background-color: var(--color-bg);
}
.public-header {
  width: 100%;
}

.public-main {
  width: 100%;
}
</style>

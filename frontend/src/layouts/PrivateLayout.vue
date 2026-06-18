<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { RouterView } from 'vue-router'
import AppSideBar from '@/components/layout/AppSideBar.vue'
import AppPrivateTop from '@/components/layout/AppPrivateTop.vue'

const sidebarOpen = ref(false)

const isDarkMode = ref(localStorage.getItem('chronic_theme') === 'dark')

const handleThemeChange = (event) => {
  isDarkMode.value = event.detail === 'dark'
}

onMounted(() => {
  window.addEventListener('chronic-theme-change', handleThemeChange)
})

onUnmounted(() => {
  window.removeEventListener('chronic-theme-change', handleThemeChange)
})
</script>

<template>
  <div class="private-layout" :class="{ 'dark-mode': isDarkMode }">
    <aside class="private-sidebar" :class="{ 'is-open': sidebarOpen }">
      <AppSideBar @close-sidebar="sidebarOpen = false" />
    </aside>

    <div class="private-content">
      <AppPrivateTop :is-sidebar-open="sidebarOpen" @toggle-sidebar="sidebarOpen = !sidebarOpen" />

      <main class="private-main">
        <div class="private-main-inner">
          <RouterView />
        </div>
      </main>
    </div>
  </div>
</template>

<style scoped>
.private-layout {
  height: 100vh;
  min-height: 100vh;
  overflow: hidden;
  display: grid;
  grid-template-columns: 240px 1fr;
  background-color: var(--color-bg);
}

.private-sidebar {
  height: 100vh;
  box-sizing: border-box;
  border-right: 2px solid var(--color-border);
  background-color: var(--color-surface);
  padding: 8px;
  overflow: hidden;
}

.private-content {
  min-width: 0;
  min-height: 0;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.private-main {
  flex: 1;
  min-width: 0;
  min-height: 0;
  padding: 32px;
  overflow-y: auto;
}

.private-main-inner {
  width: 100%;
}

@media (min-width: 1600px) {
  .private-main-inner {
    max-width: 1200px;
    margin: 0 auto;
  }
}

@media (min-width: 820px) and (max-width: 1025px) and (orientation: portrait) {
  .private-layout {
    grid-template-columns: 1fr;
    position: relative;
  }

  .private-sidebar {
    position: fixed;
    top: 84px;
    left: 0;

    display: block;
    width: min(340px, 42vw);
    height: calc(100vh - 84px);
    max-height: none;

    border-right: 2px solid var(--color-border);
    border-left: none;

    z-index: 40;

    transform: translateX(-100%);
    transition: transform 0.5s ease;

    background-color: color-mix(in srgb, var(--color-surface) 78%, transparent);
    backdrop-filter: blur(12px);
  }

  .private-sidebar.is-open {
    transform: translateX(0);
  }

  .private-main {
    padding: 28px;
  }
}

@media (max-width: 1369px) and (orientation: landscape) {
  .private-layout {
    grid-template-columns: 280px 1fr;
  }
}
@media (max-width: 769px) {
  .private-layout {
    grid-template-columns: 1fr;
    position: relative;
  }

  .private-sidebar {
    position: fixed;
    top: 80px;
    left: 0;
    right: auto;
    padding-left: 0;

    display: block;
    width: 70%;
    height: calc(100vh - 80px);
    max-height: none;

    border-right: 2px solid var(--color-border);
    border-left: none;

    z-index: 40;

    transform: translateX(-100%);
    transition: transform 0.5s ease;

    background-color: color-mix(in srgb, var(--color-surface) 78%, transparent);
    backdrop-filter: blur(12px);
  }

  .private-sidebar.is-open {
    transform: translateX(0);
  }
}

@media (max-width: 950px) and (max-height: 520px) and (orientation: landscape) {
  .private-layout {
    grid-template-columns: 1fr;
    position: relative;
  }

  .private-sidebar {
    position: fixed;
    top: 58px;
    left: 0;
    right: auto;

    display: block;
    width: min(310px, 54vw);
    height: calc(100vh - 58px);
    max-height: none;
    padding-left: 0;

    border-right: 2px solid var(--color-border);
    border-left: none;

    z-index: 40;

    transform: translateX(-100%);
    transition: transform 0.5s ease;

    background-color: color-mix(in srgb, var(--color-surface) 78%, transparent);
    backdrop-filter: blur(12px);
  }

  .private-sidebar.is-open {
    transform: translateX(0);
  }

  .private-main {
    padding: 1rem 1.25rem;
  }
}
</style>

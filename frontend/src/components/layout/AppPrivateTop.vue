<script setup>
import { onMounted, ref } from 'vue'

import OpenMenuIcon from '../Icons/OpenMenuIcon.vue'
import CloseMenuIcon from '../Icons/CloseMenuIcon.vue'
import LogoIcon from '../brand/LogoIcon.vue'
import { getCurrentUser } from '@/services/userService'

const emit = defineEmits(['toggle-sidebar'])

defineProps({
  isSidebarOpen: {
    type: Boolean,
    default: false,
  },
})

const currentUser = ref(null)
const errorMessage = ref('')

async function loadCurrentUser() {
  try {
    currentUser.value = await getCurrentUser()
  } catch (error) {
    errorMessage.value = error.message
  }
}

onMounted(() => {
  loadCurrentUser()
})
</script>

<template>
  <header class="top">
    <section class="top-member">
      <div class="top-logo">
        <LogoIcon />
      </div>

      <strong v-if="currentUser">{{ currentUser.name }}</strong>
      <strong v-else>Área privada</strong>
    </section>

    <button
      class="top-toggle"
      type="button"
      :aria-label="isSidebarOpen ? 'Cerrar menu lateral' : 'Abrir menu lateral'"
      :aria-expanded="isSidebarOpen"
      @click="emit('toggle-sidebar')"
    >
      <CloseMenuIcon v-if="isSidebarOpen" />
      <OpenMenuIcon v-else />
    </button>
  </header>
</template>

<style scoped>
.top {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 1rem;

  min-height: 90px;
  width: 100%;
  padding: 0 32px;

  position: relative;
  z-index: 30;

  background-color: var(--color-bg);
  color: var(--color-text);
}

.top::after {
  content: '';
  position: absolute;
  left: 32px;
  right: 32px;
  bottom: 0;
  height: 2px;
  background-color: var(--color-border);
}

.top-member {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  min-width: 0;
}

.top-logo {
  display: none;
  align-items: center;
  justify-content: center;
  color: var(--color-primary);
}

.top-logo svg {
  width: 2rem;
  height: 2rem;
}

.top-member strong {
  color: var(--color-text);
  font-size: 1.15rem;
  font-weight: 800;
  white-space: nowrap;
}

.top-toggle {
  display: none;
  align-items: center;
  justify-content: center;

  width: 2.7rem;
  height: 2.7rem;

  border: 1px solid var(--color-border);
  border-radius: 0.45rem;
  background-color: var(--color-surface);
  color: var(--color-text);

  font-size: 1.35rem;
  line-height: 1;
  cursor: pointer;
}

.top-toggle svg {
  width: 1.2rem;
  height: 1.2rem;
}

@media (max-width: 769px) {
  .top {
    justify-content: flex-start;
    min-height: 80px;
    padding: 0 1.5rem;
  }

  .top::after {
    left: 0;
    right: 0;
  }

  .top-member {
    order: 2;
    margin-left: auto;
  }

  .top-logo {
    display: flex;
  }

  .top-member strong {
    font-size: 1rem;
    text-align: right;
  }

  .top-toggle {
    display: flex;
    order: 1;
    margin-right: 0.85rem;

    transition:
      transform 0.2s ease,
      background-color 0.2s ease,
      border-color 0.2s ease,
      color 0.2s ease;
  }

  .top-toggle:hover {
    background-color: var(--color-primary-muted);
    color: var(--color-primary);
    transform: translateY(-1px);
  }

  .top-toggle:active {
    transform: scale(0.94);
  }

  .top-toggle svg {
    transition: transform 0.25s ease;
  }

  .top-toggle:hover svg {
    transform: scale(1.08);
  }
}

@media (min-width: 820px) and (max-width: 1025px) and (orientation: portrait) {
  .top {
    justify-content: flex-start;
    min-height: 84px;
    padding: 0 1.75rem;
  }

  .top::after {
    left: 0;
    right: 0;
  }

  .top-member {
    order: 2;
    margin-left: auto;
  }

  .top-logo {
    display: flex;
  }

  .top-member strong {
    font-size: 1.05rem;
    text-align: right;
  }

  .top-toggle {
    display: flex;
    order: 1;
    margin-right: 1rem;

    width: 2.9rem;
    height: 2.9rem;

    transition:
      transform 0.2s ease,
      background-color 0.2s ease,
      border-color 0.2s ease,
      color 0.2s ease;
  }

  .top-toggle:hover {
    background-color: var(--color-primary-muted);
    color: var(--color-primary);
    transform: translateY(-1px);
  }

  .top-toggle:active {
    transform: scale(0.94);
  }

  .top-toggle svg {
    transition: transform 0.25s ease;
  }

  .top-toggle:hover svg {
    transform: scale(1.08);
  }
}

@media (max-width: 950px) and (max-height: 520px) and (orientation: landscape) {
  .top {
    justify-content: flex-start;
    min-height: 58px;
    padding: 0 1rem;
  }

  .top::after {
    left: 0;
    right: 0;
    height: 1px;
  }

  .top-member {
    order: 2;
    margin-left: auto;
  }

  .top-logo {
    display: flex;
  }

  .top-logo svg {
    width: 1.55rem;
    height: 1.55rem;
  }

  .top-member strong {
    font-size: 0.95rem;
    text-align: right;
  }

  .top-toggle {
    display: flex;
    order: 1;
    width: 2.35rem;
    height: 2.35rem;
    margin-right: 0.75rem;
  }

  .top-toggle svg {
    width: 1.05rem;
    height: 1.05rem;
  }
}
</style>

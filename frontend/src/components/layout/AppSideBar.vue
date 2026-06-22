<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

import LogoIcon from '../brand/LogoIcon.vue'
import ConfigIcon from '../Icons/ConfigIcon.vue'
import DashIcon from '../Icons/DashIcon.vue'
import DropIcon from '../Icons/DropIcon.vue'
import LogInIcon from '../Icons/LogInIcon.vue'
import LogOutIcon from '../Icons/LogOutIcon.vue'
import { useCurrentUser } from '@/composables/useCurrentUser'

const router = useRouter()
const { clearCurrentUser } = useCurrentUser()
const showLogoutModal = ref(false)
const emit = defineEmits(['close-sidebar'])

function openLogoutModal() {
  showLogoutModal.value = true
}

function cancelLogout() {
  showLogoutModal.value = false
}

function confirmLogout() {
  localStorage.removeItem('access_token')
  clearCurrentUser()
  router.push('/login')
}
</script>
<template>
  <section class="side-bar-container">
    <div class="side-logo">
      <div class="side-logo-icon"><LogoIcon /></div>
      <div class="side-logo-text">Chronic Project</div>
    </div>
    <nav class="side-nav">
      <RouterLink class="side-nav-comp" to="/dashboard" @click="emit('close-sidebar')">
        <DashIcon />
        <span>Inicio</span>
      </RouterLink>

      <RouterLink class="side-nav-comp" to="/glucemias" @click="emit('close-sidebar')">
        <DropIcon />
        <span>Mis glucemias</span>
      </RouterLink>

      <RouterLink class="side-nav-comp" to="/profile" @click="emit('close-sidebar')">
        <LogInIcon />
        <span>Perfil</span>
      </RouterLink>

      <RouterLink class="side-nav-comp" to="/settings" @click="emit('close-sidebar')">
        <ConfigIcon />
        <span>Configuración</span>
      </RouterLink>
    </nav>
    <nav class="log-out">
      <button class="log-out-comp" type="button" @click="openLogoutModal">
        <LogOutIcon />
        <span>Salir</span>
      </button>
    </nav>
  </section>
  <div v-if="showLogoutModal" class="logout-modal-backdrop">
    <div class="logout-modal" role="dialog" aria-modal="true" aria-labelledby="logout-modal-title">
      <h2 id="logout-modal-title">¿De verdad deseas cerrar sesión?</h2>

      <div class="logout-modal-actions">
        <button type="button" @click="cancelLogout">Cancelar</button>

        <button type="button" @click="confirmLogout">Cerrar sesión</button>
      </div>
    </div>
  </div>
</template>
<style scoped>
.side-nav-comp svg *,
.log-out-comp svg * {
  width: 18px;
  height: 18px;
  stroke-width: 1.8;
}
.side-bar-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  min-height: 0;
  overflow: hidden;
}
.side-logo {
  display: flex;

  align-items: center;
  color: var(--color-primary);
  font-size: 18px;
  font-weight: 600;
  gap: 0.4rem;
  padding: 1rem;
  margin: 8px;
  margin-bottom: 2px;
}
.side-logo-icon svg {
  width: 32px;
  height: 32px;
}
.side-nav {
  display: flex;
  flex-direction: column;
  justify-items: center;

  justify-content: center;
  border-bottom: 2px solid var(--color-border);
  padding: 1rem;
}
.side-nav-comp {
  display: flex;

  justify-content: start;
  gap: 8px;
  border-radius: 0.25rem;
  width: 80%;
  padding: 0.6rem;
  margin: 0.2rem;
  cursor: pointer;
  color: var(--color-text-muted);
  text-decoration: none;
  font-size: 16px;
  align-items: center;
}
.side-nav-comp svg {
  height: 16px;
  width: 16px;
  color: inherit;
}

.side-nav-comp:hover,
.side-nav-comp.router-link-exact-active,
.side-nav-comp.router-link-active {
  background-color: var(--color-primary-muted);
  color: var(--color-primary);
}

.log-out {
  display: flex;
  flex-direction: column;
  justify-items: center;
  gap: 0.5rem;
  justify-content: center;
  margin-top: auto;
  border-top: 2px solid var(--color-border);
  padding: 1rem;
}
.log-out-comp {
  display: flex;

  justify-content: start;
  gap: 8px;
  border-radius: 0.25rem;
  width: 70%;
  padding: 0.4rem;
  margin: 0.2rem;

  color: var(--color-text-muted);
  border: none;
  appearance: none;
  font: inherit;

  cursor: pointer;
  background: transparent;
  align-items: center;
}
.log-out-comp svg {
  height: 16px;
  width: 16px;
  color: inherit;
}
.log-out-comp p {
  text-decoration: none;
  font-size: 12px;
  color: inherit;
}
.log-out-comp:hover {
  background-color: var(--color-primary-muted);
  color: var(--color-primary);
}

.logout-modal-backdrop {
  position: fixed;
  inset: 0;
  z-index: 1000;
  background-color: color-mix(in srgb, var(--color-bg) 80%, transparent);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
}

.logout-modal {
  width: min(420px, 100%);
  background-color: var(--color-bg);
  border: 1px solid var(--color-border);
  border-radius: 1rem;
  padding: 1.5rem;
  color: var(--color-text);
}

.logout-modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  margin-top: 1.5rem;
}
.logout-modal-actions button {
  background-color: var(--color-primary);
  color: var(--color-bg);
  border: none;
  border-radius: 0.15rem;
  padding: 0.3rem 0.4rem;
}
@media (min-width: 820px) and (max-width: 1025px) and (orientation: portrait) {
  .side-nav-comp svg *,
  .log-out-comp svg * {
    width: 28px;
    height: 28px;
    stroke-width: 1.8;
  }
  .side-bar-container {
    gap: 1.2rem;
  }
  .side-logo {
    font-size: 2rem;

    gap: 0.95rem;
    padding: 1rem 1.05rem;
    margin: 1.75rem 0 0.75rem;
  }
  .side-logo-icon svg {
    width: 46px;
    height: 46px;
  }
  .side-nav {
    padding: 1rem 1.05rem;
    gap: 1.9rem;
  }
  .side-nav-comp {
    width: 100%;
    min-height: 4.65rem;
    padding: 1.1rem 1.15rem;
    margin: 0;
    gap: 1.1rem;
    border-radius: 0.7rem;
    font-size: 1.42rem;
  }
  .side-nav-comp svg {
    height: 31px;
    width: 31px;
    color: inherit;
  }
  .side-nav-comp:hover,
  .side-nav-comp:has(.router-link-exact-active),
  .side-nav-comp:has(.router-link-active) {
    background-color: var(--color-primary-muted);
    color: var(--color-primary);
  }
  .log-out {
    gap: 1.35rem;
    padding: 1rem 1.05rem;
  }
  .log-out-comp {
    width: 100%;
    min-height: 4.2rem;
    padding: 1rem 1.15rem;
    margin: 0;
    gap: 1.1rem;
    border-radius: 0.7rem;
    font-size: 1.32rem;
  }
  .log-out-comp svg {
    height: 30px;
    width: 30px;
    color: inherit;
  }

}
@media (max-width: 1369px) and (orientation: landscape) {
  .side-logo {
    font-size: 22px;

    gap: 0.6rem;
    padding: 1rem;
    margin: 2rem 0;
    margin-bottom: 2px;
    font-size: 26px;
  }
  .side-logo-icon svg {
    width: 40px;
    height: 40px;
  }
  .side-nav-comp {
    width: 100%;
    min-height: 52px;
    margin: 0;
    padding: 0.75rem 1rem;
    gap: 0.75rem;
    border-radius: 0.5rem;
    box-sizing: border-box;
    font-size: 18px;
  }

  .side-nav-comp svg {
    width: 22px;
    height: 22px;
    flex-shrink: 0;
  }

  .side-nav {
    gap: 2.5rem;
  }

  .log-out {
    gap: 0.75rem;
  }
  .log-out-comp {
    width: 100%;
    min-height: 52px;
    margin: 0;
    padding: 0.75rem 1rem;
    gap: 0.75rem;
    border-radius: 0.5rem;
    box-sizing: border-box;
    font-size: 18px;
  }

  .log-out-comp svg {
    width: 22px;
    height: 22px;
    flex-shrink: 0;
  }

}
@media (max-width: 769px) {
  .side-bar-container {
    height: 100%;
  }
}

@media (max-width: 950px) and (max-height: 520px) and (orientation: landscape) {
  .side-bar-container {
    height: 100%;
    gap: 0;
    overflow-y: auto;
  }

  .side-logo {
    gap: 0.6rem;
    margin: 0.25rem 0 0.15rem;
    padding: 0.4rem 0.75rem;
    font-size: 1rem;
    line-height: 1;
  }

  .side-logo-icon svg {
    width: 24px;
    height: 24px;
  }

  .side-nav {
    gap: 0.6rem;
    padding: 0.75rem 1rem;
  }

  .side-nav-comp {
    width: 100%;
    min-height: 2.35rem;
    gap: 0.6rem;
    margin: 0;
    padding: 0.4rem 0.65rem;
    border-radius: 0.45rem;
    font-size: 1rem;
  }

  .side-nav-comp svg {
    width: 20px;
    height: 20px;
  }

  .log-out {
    gap: 0.5rem;
    padding: 0.75rem 1rem;
  }

  .log-out-comp {
    width: 100%;
    min-height: 2.6rem;
    gap: 0.75rem;
    margin: 0;
    padding: 0.5rem 0.75rem;
    border-radius: 0.45rem;
    font-size: 1rem;
  }

  .log-out-comp svg {
    width: 20px;
    height: 20px;
  }

  .log-out-comp p {
    font-size: 1rem;
  }

}
</style>

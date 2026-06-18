<script setup>
import LogoIcon from '../brand/LogoIcon.vue'
import LogInIcon from '../Icons/LogInIcon.vue'
import RegisterUserIcon from '../Icons/RegisterUserIcon.vue'
import { ref } from 'vue'

import ToggleDownIcon from '../Icons/ToggleDownIcon.vue'
import ToggleUpIcon from '../Icons/ToggleUpIcon.vue'

const menuOpen = ref(false)
</script>
<template>
  <section class="header-container">
    <div class="header-content">
      <div class="logo">
        <LogoIcon class="logo-icon" />
        Chronic Project
      </div>
      <div class="header-menu" :class="{ 'is-open': menuOpen }">
        <nav class="header-nav">
          <RouterLink @click="menuOpen = false" to="/">Inicio</RouterLink>
          <RouterLink @click="menuOpen = false" to="/diabetes">Diabetes</RouterLink>
          <RouterLink @click="menuOpen = false" to="/about">Sobre el proyecto</RouterLink>
          <RouterLink @click="menuOpen = false" to="/contact">Contacto</RouterLink>
        </nav>
        <nav class="log-user">
          <RouterLink @click="menuOpen = false" class="login" to="/login"
            ><LogInIcon class="logicon" /> Iniciar sesión</RouterLink
          >
          <RouterLink @click="menuOpen = false" class="register" to="/register"
            ><RegisterUserIcon class="logicon" /> Crear cuenta</RouterLink
          >
        </nav>
      </div>
      <button
        class="menu-toggle"
        type="button"
        :aria-label="menuOpen ? 'Cerrar menu principal' : 'Abrir menu principal'"
        :aria-expanded="menuOpen"
        @click="menuOpen = !menuOpen"
      >
        <ToggleUpIcon v-if="menuOpen" class="menu-toggle-icon" />
        <ToggleDownIcon v-else class="menu-toggle-icon" />
      </button>
    </div>
  </section>
</template>
<style>
.menu-toggle {
  display: none;
  border: none;
  background: transparent;
  cursor: pointer;
  padding: 0.4rem;
}

.menu-toggle-icon {
  width: 32px;
  height: 32px;
  color: var(--color-primary);
}
.header-container {
  height: 4.5rem;
  width: 100%;
}
.header-content {
  max-width: 1200px;
  height: 100%;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 18px;
}
.header-menu {
  display: flex;
  align-items: center;
  gap: 2rem;
}
.logo {
  display: flex;
  align-items: center;
  color: var(--color-primary);
  font-size: 20px;
  font-weight: 600;
  gap: 0.4rem;
}
.logo-icon {
  width: 30px;
  height: 30px;
}
.header-nav {
  display: flex;

  gap: 2rem;
  font-weight: 500;
}
.header-nav a {
  position: relative;
  color: var(--color-text);
  text-decoration: none;
  padding-bottom: 0.25rem;
}
.header-nav a::after {
  content: '';
  position: absolute;
  left: 0;
  bottom: 0;
  width: 0;
  height: 2px;
  background-color: var(--color-primary);
  transition: width 0.2s ease;
}
.header-nav a:hover {
  color: var(--color-primary);
}
.header-nav a:hover::after,
.header-nav a.router-link-exact-active::after {
  width: 100%;
}
.header-nav a.router-link-exact-active {
  color: var(--color-primary);
}
.log-user {
  display: flex;
  gap: 0.5rem;
}
.log-user a {
  text-decoration: none;
  border-radius: 0.5rem;
  border-style: solid;
  border-width: 1px;
  border-color: var(--color-border);
  padding: 0.5rem 0.7rem;
}
.log-user .register {
  display: flex;
  gap: 0.4rem;
  align-items: center;
  background-color: var(--color-primary);
  color: var(--color-surface);
  border-color: var(--color-primary);
}
.log-user .login {
  display: flex;
  gap: 0.4rem;
  align-items: center;
  color: var(--color-primary);
  background-color: var(--color-bg);
}

@media (max-width: 769px),
  (min-width: 820px) and (max-width: 1025px) and (orientation: portrait),
  (max-width: 1180px) and (orientation: landscape) {
  .header-container {
    border-bottom: 2px solid var(--color-border);
    position: relative;
  }
  .menu-toggle {
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .header-menu {
    position: absolute;
    top: 100%;
    right: 0;
    left: 0;
    z-index: 20;

    display: flex;
    flex-direction: column;
    gap: 1rem;

    background-color: color-mix(in srgb, var(--color-bg) 70%, transparent);
    box-shadow: var(--shadow-soft);
    backdrop-filter: blur(10px);

    max-height: 0;
    opacity: 0;
    overflow: hidden;
    pointer-events: none;
    transform: translateY(-0.75rem);

    transition:
      max-height 0.5s ease,
      opacity 0.5s ease,
      transform 0.5s ease;
  }
  .header-menu.is-open {
    max-height: 500px;
    opacity: 1;
    pointer-events: auto;
    transform: translateY(0);

    border-bottom: 2px solid var(--color-border);
    border-left: 2px solid var(--color-border);
    padding-bottom: 1rem;
  }

  .header-nav {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    margin-top: 1rem;
  }

  .header-nav a::after {
    display: none;
  }
  .log-user {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }
}
@media (max-width: 1025px) and (orientation: portrait) {
  .header-container {
    height: 5rem;
  }

  .header-content {
    padding: 0 1.5rem;
    font-size: 20px;
  }

  .logo {
    font-size: 22px;
    gap: 0.4rem;
  }

  .logo-icon {
    width: 30px;
    height: 30px;
  }

  .header-menu {
    gap: 1.4rem;
  }

  .header-nav {
    gap: 1.4rem;
    font-size: 20px;
  }

  .log-user {
    gap: 0.45rem;
  }

  .log-user a {
    padding: 0.45rem 0.6rem;
    font-size: 18px;
  }

  .log-user .login,
  .log-user .register {
    gap: 0.4rem;
  }
}
</style>

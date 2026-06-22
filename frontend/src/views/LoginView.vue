<script setup>
import { ref } from 'vue'
import { API_BASE_URL } from '@/config/api'
import { useRouter } from 'vue-router'

import { useCurrentUser } from '@/composables/useCurrentUser'

import MailIcon from '@/components/Icons/MailIcon.vue'
import LockerIcon from '@/components/Icons/LockerIcon.vue'
import EyeDownIcon from '@/components/Icons/EyeDownIcon.vue'
import EyeUpIcon from '@/components/Icons/EyeUpIcon.vue'

const router = useRouter()

const email = ref('')
const password = ref('')
const showPassword = ref(false)
const isLoading = ref(false)
const { currentUser, loadCurrentUser, clearCurrentUser } = useCurrentUser()

const errorMessage = ref('')

async function handleLogin() {
  if (isLoading.value) return

  errorMessage.value = ''
  clearCurrentUser()
  isLoading.value = true

  try {
    const formData = new URLSearchParams()
    formData.append('username', email.value)
    formData.append('password', password.value)

    const respuesta = await fetch(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: formData,
    })

    const data = await respuesta.json()

    if (!respuesta.ok) {
      errorMessage.value = data.detail || 'No se ha podido iniciar sesión'
      return
    }

    localStorage.setItem('access_token', data.access_token)
    try {
      await loadCurrentUser({ force: true })

      setTimeout(() => {
        router.push('/dashboard')
      }, 2000)
    } catch (error) {
      localStorage.removeItem('access_token')
      clearCurrentUser()
      errorMessage.value = error.message
    }
  } catch (error) {
    errorMessage.value = error.message || 'No se ha podido conectar con el servidor'
  } finally {
    isLoading.value = false
  }
}
</script>
<template>
  <section class="login">
    <section class="login-grid">
      <div v-if="!currentUser" class="login-grid-content">
        <h1>Iniciar Sesión</h1>
        <h2>Accede a tu cuenta para continuar</h2>
        <form @submit.prevent="handleLogin" :aria-busy="isLoading">
          <label class="label" for="email">Correo electrónico</label>
          <div class="placing">
            <MailIcon class="placing-icon" /><input
              v-model="email"
              id="email"
              type="email"
              :disabled="isLoading"
              placeholder="tu@email.com"
            />
          </div>
          <label class="label" for="password">Contraseña</label>
          <div class="placing">
            <LockerIcon class="placing-icon" /><input
              v-model="password"
              id="password"
              :type="showPassword ? 'text' : 'password'"
              :disabled="isLoading"
              placeholder="Tu contraseña"
            />
            <button
              class="password-toggle"
              type="button"
              :aria-label="showPassword ? 'Ocultar contrasena' : 'Mostrar contrasena'"
              :disabled="isLoading"
              @click="showPassword = !showPassword"
            >
              <EyeUpIcon v-if="showPassword" />
              <EyeDownIcon v-else />
            </button>
          </div>

          <div class="error-login" v-if="errorMessage">
            <p>{{ errorMessage }}</p>
          </div>
          <p class="forgot"></p>
          <button class="login-button" type="submit" :disabled="isLoading">
            <span v-if="isLoading" class="login-spinner" aria-hidden="true"></span>
            <span>{{ isLoading ? 'Iniciando sesión...' : 'Iniciar sesión' }}</span>
          </button>
        </form>

        <div class="hook-user">
          <p>¿Aun no tienes cuenta?</p>
          <RouterLink to="/register">Registrate aquí</RouterLink>
        </div>
      </div>
      <div class="success-login" v-if="currentUser">
        <h2 class="success-title">Sesión iniciada correctamente</h2>
        <p>Bienvenido, {{ currentUser.name }}</p>
        <p>Te redirigimos al dashboard...</p>

        <RouterLink to="/dashboard"> Ir al dashboard ahora </RouterLink>
      </div>
    </section>
  </section>
</template>
<style scoped>
.password-toggle {
  display: inline-flex;
  align-items: center;
  align-self: stretch;
  justify-content: center;
  width: 3rem;
  border: none;
  border-left: 1px solid var(--color-border);
  background: var(--color-bg);
  color: var(--color-text-muted);
  cursor: pointer;
  flex-shrink: 0;
}
.password-toggle svg {
  width: 1.1rem;
  height: 1.1rem;
}
.login {
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: var(--color-bg);
  min-height: calc(100vh - 80px);
  padding: 2rem 1rem;
}
.login-grid {
  width: 100%;
  max-width: 520px;
}
.login-grid-content {
  display: flex;
  flex-direction: column;
  background-color: var(--color-surface);
  border-radius: 1rem;
  padding: 1rem;
}
.login-grid-content h1,
.login-grid-content h2 {
  margin: 8px;
  color: var(--color-primary-dark);
}
.login-grid-content form {
  display: flex;
  flex-direction: column;
  justify-items: center;
  gap: 0.5rem;
  width: 100%;
  margin: 8px 0;
}

.label {
  font-weight: 600;
}
.placing {
  display: flex;
  align-items: center;
  border: 1px solid var(--color-border);
  border-radius: 0.4rem;
  background-color: var(--color-bg);
}
.placing .placing-icon {
  width: 1.2rem;
  height: 1.2rem;
  margin: 0 0.8rem;
  background-color: var(--color-bg);
  color: var(--color-primary);
}
.placing input {
  flex: 1;
  min-width: 0;
  border: none;
  outline: none;
  padding: 0.8rem;
  border-left: 1px solid var(--color-border);
  background-color: var(--color-bg);
}
.forgot {
  text-align: center;
  font-weight: 600;
  color: var(--color-primary);
  font-size: 14px;
}
.error-login {
  margin: 1rem 8px 0;
  padding: 0.8rem 1rem;
  border: 1px solid var(--color-danger);
  border-radius: 0.6rem;
  background-color: var(--color-bg);
}
.error-login p {
  margin: 0;
  color: var(--color-danger);
  font-weight: 600;
  text-align: center;
}
.login-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  text-align: center;
  border: none;
  border-style: none;
  border-radius: 0.4rem;
  background-color: var(--color-primary);
  color: var(--color-bg);
  padding: 0.8rem;
  cursor: pointer;
}
.login-grid-content form[aria-busy='true'] .login-button,
.login-grid-content form[aria-busy='true'] .password-toggle {
  opacity: 0.7;
  pointer-events: none;
}
.login-grid-content form[aria-busy='true'] input {
  opacity: 0.75;
  cursor: wait;
}
.login-spinner {
  width: 1rem;
  height: 1rem;
  border: 2px solid rgba(255, 255, 255, 0.45);
  border-top-color: var(--color-bg);
  border-radius: 50%;
  animation: login-spin 0.8s linear infinite;
}
@keyframes login-spin {
  to {
    transform: rotate(360deg);
  }
}
.hook-user {
  display: flex;
  justify-content: center;
  gap: 16px;
  margin: 16px;
}
.hook-user p {
  margin: 0;
}
.hook-user a {
  text-decoration: none;
  color: var(--color-primary);
}
.success-login {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  margin: 1rem 8px 0;
  padding: 1rem;
  border: 1px solid var(--color-primary);
  border-radius: 0.8rem;
  background-color: var(--color-surface);
}

.success-login p {
  margin: 0;
  color: var(--color-text);
}

.success-login .success-title {
  font-weight: 700;
  color: var(--color-primary-dark);
}

.success-login a {
  display: inline-flex;
  justify-content: center;
  align-items: center;
  margin-top: 0.5rem;
  padding: 0.7rem 1rem;
  border-radius: 0.4rem;
  background-color: var(--color-primary);
  color: var(--color-bg);
  text-decoration: none;
  font-weight: 600;
}
@media (max-width: 1025px) and (orientation: portrait) {
  .login-grid {
    width: 100%;
    max-width: 720px;
  }
  .login-grid-content h1 {
    font-size: 32px;
  }

  .login-grid-content h2 {
    font-size: 28px;
  }

  .label {
    font-size: 24px;
  }

  .placing input {
    font-size: 24px;
  }

  .forgot {
    font-size: 20px;
  }

  .error-login {
    font-size: 22px;
  }

  .login-button {
    font-size: 24px;
  }

  .hook-user p {
    font-size: 24px;
  }

  .hook-user a {
    font-size: 24px;
  }
  .success-login {
    font-size: 22px;
  }

  .success-login a {
    font-size: 22px;
  }
}
@media (max-width: 768px) {
  .login-grid {
    width: 100%;
    max-width: 720px;
  }
  .hook-user {
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  .placing {
    display: flex;
    align-items: center;
    border: 1px solid var(--color-border);
    border-radius: 0.4rem;
    background-color: var(--color-bg);
    overflow: hidden;
  }
  .placing .placing-icon {
    width: 1.5rem;
    height: 1.5rem;
    margin: 0 0.7rem;
    color: var(--color-primary);
    flex-shrink: 0;
  }
  .placing input {
    flex: 1;
    min-width: 0;
    border: none;
    outline: none;
    padding: 0.5rem;
    border-left: 1px solid var(--color-border);
  }

  .error-login {
    margin: 1rem 0 0;
    padding: 0.8rem;
  }
  .success-login {
    margin: 1rem 0 0;
    padding: 0.9rem;
  }

  .success-login a {
    width: 100%;
    padding: 0.7rem;
  }
}
</style>

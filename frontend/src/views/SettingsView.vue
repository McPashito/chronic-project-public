<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'

import AppPrivateStart from '@/components/layout/AppPrivateStart.vue'

import EyeDownIcon from '@/components/Icons/EyeDownIcon.vue'
import EyeUpIcon from '@/components/Icons/EyeUpIcon.vue'
import InfoIcon from '@/components/Icons/InfoIcon.vue'
import LockerIcon from '@/components/Icons/LockerIcon.vue'
import MailIcon from '@/components/Icons/MailIcon.vue'
import MoonIcon from '@/components/Icons/MoonIcon.vue'
import SecurityIcon from '@/components/Icons/SecurityIcon.vue'

import { getCurrentUser } from '@/services/userService'
import { changePassword } from '@/services/securityService'
import { handleAuthError } from '@/utils/handleAuthError'

const router = useRouter()

const currentUser = ref(null)
const isLoadingSettings = ref(false)
const settingsError = ref('')

const isDarkMode = ref(false)

const oldPassword = ref('')
const newPassword = ref('')
const confirmPassword = ref('')
const passwordError = ref('')
const passwordSuccess = ref('')
const isSubmittingPassword = ref(false)

const newEmail = ref('')
const confirmEmail = ref('')
const emailError = ref('')
const emailSuccess = ref('')
const isSubmittingEmail = ref(false)

const showOldPassword = ref(false)
const showNewPassword = ref(false)
const showConfirmPassword = ref(false)

const currentEmail = computed(() => {
  return currentUser.value?.email || 'No disponible'
})

onMounted(() => {
  const savedTheme = localStorage.getItem('chronic_theme')
  isDarkMode.value = savedTheme === 'dark'

  loadSettingsData()
})

async function loadSettingsData() {
  isLoadingSettings.value = true
  settingsError.value = ''

  try {
    currentUser.value = await getCurrentUser()
  } catch (error) {
    if (handleAuthError(error, router)) {
      settingsError.value = 'Tu sesión ha caducado. Te redirigimos al inicio de sesión.'
      return
    }

    settingsError.value = error.message || 'No se pudo cargar la configuración.'
  } finally {
    isLoadingSettings.value = false
  }
}

function toggleDarkMode() {
  isDarkMode.value = !isDarkMode.value

  const newTheme = isDarkMode.value ? 'dark' : 'light'

  localStorage.setItem('chronic_theme', newTheme)

  window.dispatchEvent(
    new CustomEvent('chronic-theme-change', {
      detail: newTheme,
    }),
  )
}

function resetPasswordMessages() {
  passwordError.value = ''
  passwordSuccess.value = ''
}

function resetEmailMessages() {
  emailError.value = ''
  emailSuccess.value = ''
}

async function handlePasswordSubmit() {
  resetPasswordMessages()

  if (!oldPassword.value || !newPassword.value || !confirmPassword.value) {
    passwordError.value = 'Completa todos los campos de contraseña.'
    return
  }

  if (newPassword.value !== confirmPassword.value) {
    passwordError.value = 'La nueva contraseña y su confirmación no coinciden.'
    return
  }

  isSubmittingPassword.value = true

  try {
    await changePassword({
      old_password: oldPassword.value,
      new_password: newPassword.value,
    })

    oldPassword.value = ''
    newPassword.value = ''
    confirmPassword.value = ''
    passwordSuccess.value = 'Contraseña actualizada correctamente.'
  } catch (error) {
    if (handleAuthError(error, router)) {
      passwordError.value = 'Tu sesión ha caducado. Te redirigimos al inicio de sesión.'
      return
    }

    passwordError.value = error.message || 'No se pudo cambiar la contraseña.'
  } finally {
    isSubmittingPassword.value = false
  }
}

async function handleEmailSubmit() {
  resetEmailMessages()

  emailSuccess.value = ''
  emailError.value =
    'Función no disponible en este momento. Estamos trabajando para habilitar el cambio de correo electrónico.'
}
</script>

<template>
  <AppPrivateStart
    title=", gestiona la seguridad y preferencias principales de tu cuenta"
    main="Configuración y cuenta"
    variant="inactive"
  />

  <section class="settings-main-flex">
    <div v-if="isLoadingSettings" class="settings-state">Cargando configuración...</div>

    <div v-else-if="settingsError" class="settings-state settings-state-error">
      {{ settingsError }}
    </div>

    <template v-else>
      <section class="settings-card-flex">
        <div class="settings-card-head">
          <div class="settings-head-text">
            <h3>Apariencia</h3>
            <p>Personaliza cómo se ve la aplicación.</p>
          </div>
        </div>

        <article class="settings-option-row">
          <div class="settings-option-info">
            <div class="settings-option-icon">
              <MoonIcon />
            </div>

            <div class="settings-option-text">
              <strong>Modo oscuro</strong>
              <span>Activa el modo oscuro para reducir la fatiga visual.</span>
            </div>
          </div>

          <div class="settings-switch-wrap">
            <button
              type="button"
              class="settings-switch"
              :class="{ 'is-active': isDarkMode }"
              role="switch"
              :aria-checked="isDarkMode"
              :aria-label="isDarkMode ? 'Desactivar modo oscuro' : 'Activar modo oscuro'"
              @click="toggleDarkMode"
            >
              <span></span>
            </button>

            <strong>{{ isDarkMode ? 'Activado' : 'Desactivado' }}</strong>
          </div>
        </article>
      </section>

      <section class="settings-card-flex">
        <div class="settings-card-head">
          <div class="settings-head-icon">
            <SecurityIcon />
          </div>

          <div class="settings-head-text">
            <h3>Seguridad de la cuenta</h3>
            <p>Mantén tu cuenta protegida actualizando tu contraseña.</p>
          </div>
        </div>

        <form class="settings-form-flex" @submit.prevent="handlePasswordSubmit">
          <label class="settings-form-row" for="old-password">
            <strong>Contraseña actual</strong>

            <div class="settings-input-wrap">
              <LockerIcon />
              <input
                id="old-password"
                v-model="oldPassword"
                :type="showOldPassword ? 'text' : 'password'"
                placeholder="Introduce tu contraseña actual"
                @input="resetPasswordMessages"
              />

              <button
                type="button"
                :aria-label="showOldPassword ? 'Ocultar contrasena actual' : 'Mostrar contrasena actual'"
                @click="showOldPassword = !showOldPassword"
              >
                <EyeUpIcon v-if="showOldPassword" />
                <EyeDownIcon v-else />
              </button>
            </div>
          </label>

          <label class="settings-form-row" for="new-password">
            <strong>Nueva contraseña</strong>

            <div class="settings-input-wrap">
              <LockerIcon />
              <input
                id="new-password"
                v-model="newPassword"
                :type="showNewPassword ? 'text' : 'password'"
                placeholder="Introduce tu nueva contraseña"
                @input="resetPasswordMessages"
              />

              <button
                type="button"
                :aria-label="showNewPassword ? 'Ocultar nueva contrasena' : 'Mostrar nueva contrasena'"
                @click="showNewPassword = !showNewPassword"
              >
                <EyeUpIcon v-if="showNewPassword" />
                <EyeDownIcon v-else />
              </button>
            </div>
          </label>

          <label class="settings-form-row" for="confirm-password">
            <strong>Confirmar nueva contraseña</strong>

            <div class="settings-input-wrap">
              <LockerIcon />
              <input
                id="confirm-password"
                v-model="confirmPassword"
                :type="showConfirmPassword ? 'text' : 'password'"
                placeholder="Confirma tu nueva contraseña"
                @input="resetPasswordMessages"
              />

              <button
                type="button"
                :aria-label="
                  showConfirmPassword
                    ? 'Ocultar confirmacion de contrasena'
                    : 'Mostrar confirmacion de contrasena'
                "
                @click="showConfirmPassword = !showConfirmPassword"
              >
                <EyeUpIcon v-if="showConfirmPassword" />
                <EyeDownIcon v-else />
              </button>
            </div>
          </label>

          <div class="settings-info-box">
            <InfoIcon />
            <span>
              La contraseña debe tener al menos 8 caracteres e incluir mayúsculas, minúsculas,
              números y símbolos.
            </span>
          </div>

          <p v-if="passwordError" class="settings-form-message settings-form-error">
            {{ passwordError }}
          </p>

          <p v-if="passwordSuccess" class="settings-form-message settings-form-success">
            {{ passwordSuccess }}
          </p>

          <div class="settings-form-actions">
            <button type="submit" class="settings-submit-button" :disabled="isSubmittingPassword">
              <LockerIcon />
              {{ isSubmittingPassword ? 'Actualizando...' : 'Actualizar contraseña' }}
            </button>
          </div>
        </form>
      </section>

      <section class="settings-card-flex">
        <div class="settings-card-head">
          <div class="settings-head-icon">
            <MailIcon />
          </div>

          <div class="settings-head-text">
            <h3>Correo electrónico</h3>
            <p>Actualiza tu dirección de correo electrónico.</p>
          </div>
        </div>

        <div class="settings-current-email">
          <span>Correo actual</span>
          <strong>{{ currentEmail }}</strong>
        </div>

        <form class="settings-form-flex" @submit.prevent="handleEmailSubmit">
          <label class="settings-form-row" for="new-email">
            <strong>Nuevo correo electrónico</strong>

            <div class="settings-input-wrap">
              <MailIcon />
              <input
                id="new-email"
                v-model="newEmail"
                type="email"
                placeholder="Introduce tu nuevo correo electrónico"
                @input="resetEmailMessages"
              />
            </div>
          </label>

          <label class="settings-form-row" for="confirm-email">
            <strong>Confirma tu nuevo correo</strong>

            <div class="settings-input-wrap">
              <MailIcon />
              <input
                id="confirm-email"
                v-model="confirmEmail"
                type="email"
                placeholder="Confirma tu nuevo correo electrónico"
                @input="resetEmailMessages"
              />
            </div>
          </label>

          <div class="settings-info-box">
            <InfoIcon />
            <span>
              Al cambiar tu correo electrónico, será necesario verificar la nueva dirección.
            </span>
          </div>

          <p v-if="emailError" class="settings-form-message settings-form-error">
            {{ emailError }}
          </p>

          <p v-if="emailSuccess" class="settings-form-message settings-form-success">
            {{ emailSuccess }}
          </p>

          <div class="settings-form-actions">
            <button type="submit" class="settings-submit-button" :disabled="isSubmittingEmail">
              <MailIcon />
              {{ isSubmittingEmail ? 'Comprobando...' : 'Actualizar correo' }}
            </button>
          </div>
        </form>
      </section>
    </template>
  </section>
</template>

<style scoped>
.settings-main-flex {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.settings-state {
  padding: 2rem;
  border: 1px solid var(--color-border);
  border-radius: 1rem;
  background-color: var(--color-bg);
  color: var(--color-text-muted);
  text-align: center;
}

.settings-state-error {
  color: var(--color-danger);
}

.settings-card-flex {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  padding: 1.6rem;
  border: 1px solid var(--color-border);
  border-radius: 1rem;
  background-color: var(--color-bg);
  box-shadow: var(--shadow-soft);
}

.settings-card-head {
  display: flex;
  align-items: center;
  gap: 0.9rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--color-border);
}

.settings-head-icon,
.settings-option-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 3rem;
  height: 3rem;
  flex-shrink: 0;
  border-radius: 50%;
  background-color: var(--color-surface);
  color: var(--color-primary);
}

.settings-head-icon svg,
.settings-option-icon svg {
  width: 1.45rem;
  height: 1.45rem;
}

.settings-head-text {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.settings-head-text h3,
.settings-head-text p {
  margin: 0;
}

.settings-head-text h3 {
  color: var(--color-text);
  font-size: 1.35rem;
  font-weight: 800;
}

.settings-head-text p {
  color: var(--color-text-muted);
  font-size: 0.95rem;
}

.settings-option-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1.5rem;
  padding: 1rem;
  border: 1px solid var(--color-border);
  border-radius: 0.85rem;
  background-color: var(--color-bg);
}

.settings-option-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.settings-option-text {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.settings-option-text strong {
  color: var(--color-text);
  font-size: 1rem;
}

.settings-option-text span {
  color: var(--color-text-muted);
  font-size: 0.9rem;
}

.settings-switch-wrap {
  display: flex;
  align-items: center;
  gap: 0.8rem;
}

.settings-switch-wrap strong {
  color: var(--color-text-muted);
  font-size: 0.95rem;
}

.settings-switch {
  position: relative;
  width: 4rem;
  height: 2rem;
  padding: 0.2rem;
  border: none;
  border-radius: 999px;
  background-color: var(--color-border);
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.settings-switch span {
  display: block;
  width: 1.6rem;
  height: 1.6rem;
  border-radius: 50%;
  background-color: var(--color-bg);
  box-shadow: var(--shadow-soft);
  transition: transform 0.2s ease;
}

.settings-switch.is-active {
  background-color: var(--color-primary);
}

.settings-switch.is-active span {
  transform: translateX(2rem);
}

.settings-form-flex {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.settings-form-row {
  display: grid;
  grid-template-columns: 14rem 1fr;
  align-items: center;
  gap: 1.2rem;
}

.settings-form-row strong {
  color: var(--color-text);
  font-size: 0.95rem;
}

.settings-input-wrap {
  display: flex;
  align-items: center;
  min-height: 3.3rem;
  overflow: hidden;
  border: 1px solid var(--color-border);
  border-radius: 0.65rem;
  background-color: var(--color-bg);
}

.settings-input-wrap > svg {
  width: 1.35rem;
  height: 1.35rem;
  margin: 0 1rem;
  flex-shrink: 0;
  color: var(--color-text-muted);
}

.settings-input-wrap input {
  width: 100%;
  min-width: 0;
  padding: 0.9rem 1rem;
  border: none;
  border-left: 1px solid var(--color-border);
  outline: none;
  background: transparent;
  color: var(--color-text);
  font: inherit;
}

.settings-input-wrap input::placeholder {
  color: var(--color-text-muted);
}

.settings-input-wrap button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 3.2rem;
  height: 100%;
  flex-shrink: 0;
  border: none;
  background: transparent;
  color: var(--color-text-muted);
  cursor: pointer;
}

.settings-input-wrap button svg {
  width: 1.35rem;
  height: 1.35rem;
}

.settings-info-box {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.85rem 1rem;
  border: 1px solid var(--dashboard-blue-border);
  border-radius: 0.65rem;
  background-color: var(--dashboard-blue-bg);
  color: var(--color-text-muted);
  font-size: 0.92rem;
  line-height: 1.4;
}

.settings-info-box svg {
  width: 1.35rem;
  height: 1.35rem;
  flex-shrink: 0;
  color: var(--color-primary);
}

.settings-form-message {
  margin: 0;
  padding: 0.85rem 1rem;
  border-radius: 0.65rem;
  font-size: 0.95rem;
  font-weight: 700;
}

.settings-form-error {
  background-color: #fee2e2;
  color: var(--color-danger);
}

.settings-form-success {
  background-color: #dcfce7;
  color: var(--color-success);
}

.settings-form-actions {
  display: flex;
  justify-content: flex-end;
}

.settings-submit-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.55rem;
  padding: 0.9rem 1.4rem;
  border: none;
  border-radius: 0.65rem;
  background-color: var(--color-primary);
  color: var(--color-bg);
  font-weight: 800;
  cursor: pointer;
}

.settings-submit-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.settings-submit-button svg {
  width: 1.35rem;
  height: 1.35rem;
}

.settings-current-email {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 1rem;
  border: 1px solid var(--color-border);
  border-radius: 0.85rem;
  background-color: var(--color-surface);
}

.settings-current-email span {
  color: var(--color-text-muted);
  font-size: 0.9rem;
}

.settings-current-email strong {
  color: var(--color-text);
  font-size: 1rem;
}

@media (max-width: 1025px) and (orientation: portrait) {
  .settings-card-flex {
    padding: 1.8rem;
  }

  .settings-head-text h3 {
    font-size: 1.7rem;
  }

  .settings-head-text p,
  .settings-option-text span,
  .settings-switch-wrap strong,
  .settings-form-row strong,
  .settings-info-box,
  .settings-current-email span,
  .settings-current-email strong {
    font-size: 1.3rem;
  }

  .settings-option-text strong {
    font-size: 1.4rem;
  }

  .settings-form-row {
    grid-template-columns: 1fr;
    gap: 0.6rem;
  }

  .settings-input-wrap {
    min-height: 4rem;
  }

  .settings-input-wrap input {
    font-size: 1.25rem;
  }

  .settings-submit-button {
    width: 100%;
    padding: 1.1rem 1.5rem;
    font-size: 1.25rem;
  }
}

@media (max-width: 768px) {
  .settings-card-flex {
    padding: 1.25rem;
  }

  .settings-option-row,
  .settings-current-email {
    align-items: flex-start;
    flex-direction: column;
  }

  .settings-switch-wrap,
  .settings-form-actions {
    width: 100%;
  }

  .settings-form-actions {
    justify-content: stretch;
  }

  .settings-submit-button {
    width: 100%;
  }
}
</style>

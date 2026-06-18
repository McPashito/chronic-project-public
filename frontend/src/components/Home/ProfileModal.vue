<script setup>
import { computed, ref, watch } from 'vue'

import EyeUpIcon from '../Icons/EyeUpIcon.vue'
import EyeDownIcon from '../Icons/EyeDownIcon.vue'

const props = defineProps({
  mode: {
    type: String,
    required: true,
  },
  currentUser: {
    type: Object,
    default: null,
  },
  errorMessage: {
    type: String,
    default: '',
  },
  successMessage: {
    type: String,
    default: '',
  },
  isSubmitting: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['submit', 'cancel'])

const profileForm = ref({
  name: '',
  surname: '',
  date_of_birth: '',
  subscription_type: 'standard',
})

const passwordForm = ref({
  old_password: '',
  new_password: '',
  repeat_password: '',
})

const localError = ref('')
const showOldPassword = ref(false)
const showNewPassword = ref(false)
const showRepeatPassword = ref(false)

const isEditProfileMode = computed(() => props.mode === 'edit-profile')
const isChangePasswordMode = computed(() => props.mode === 'change-password')

const modalTitle = computed(() => {
  if (isEditProfileMode.value) return 'Editar perfil'

  return 'Cambiar contraseña'
})

const modalDescription = computed(() => {
  if (isEditProfileMode.value) {
    return 'Actualiza tus datos personales. El correo electrónico no se puede modificar desde esta pantalla.'
  }

  return 'Introduce tu contraseña actual y escribe la nueva contraseña dos veces.'
})

const submitButtonText = computed(() => {
  if (props.isSubmitting) return 'Guardando...'

  if (isEditProfileMode.value) return 'Editar perfil'

  return 'Cambiar contraseña'
})

watch(
  () => props.currentUser,
  (user) => {
    if (!user) return

    profileForm.value = {
      name: user.name || '',
      surname: user.surname || '',
      date_of_birth: user.date_of_birth || '',
      subscription_type: user.subscription_type || 'standard',
    }
  },
  { immediate: true },
)

watch(
  () => props.mode,
  () => {
    localError.value = ''

    passwordForm.value = {
      old_password: '',
      new_password: '',
      repeat_password: '',
    }
  },
)

function handleSubmit() {
  localError.value = ''

  if (isEditProfileMode.value) {
    emit('submit', {
      name: profileForm.value.name,
      surname: profileForm.value.surname,
      date_of_birth: profileForm.value.date_of_birth,
      subscription_type: profileForm.value.subscription_type,
    })

    return
  }

  if (passwordForm.value.new_password !== passwordForm.value.repeat_password) {
    localError.value = 'Las nuevas contraseñas no coinciden.'
    return
  }

  emit('submit', {
    old_password: passwordForm.value.old_password,
    new_password: passwordForm.value.new_password,
  })
}
</script>

<template>
  <div class="profile-modal-overlay">
    <section class="profile-modal" role="dialog" aria-modal="true" aria-labelledby="profile-modal-title">
      <header class="profile-modal-header">
        <div>
          <h2 id="profile-modal-title">{{ modalTitle }}</h2>
          <p>{{ modalDescription }}</p>
        </div>

        <button type="button" class="profile-modal-close" @click="emit('cancel')">×</button>
      </header>

      <form class="profile-modal-form" @submit.prevent="handleSubmit">
        <template v-if="isEditProfileMode">
          <div class="profile-modal-group">
            <label for="profile-name">Nombre</label>
            <input id="profile-name" v-model="profileForm.name" type="text" />
          </div>

          <div class="profile-modal-group">
            <label for="profile-surname">Apellidos</label>
            <input id="profile-surname" v-model="profileForm.surname" type="text" />
          </div>

          <div class="profile-modal-group">
            <label for="profile-birthdate">Fecha de nacimiento</label>
            <input id="profile-birthdate" v-model="profileForm.date_of_birth" type="date" />
          </div>

          <div class="profile-modal-group">
            <label for="profile-subscription">Tipo de cuenta</label>

            <select id="profile-subscription" v-model="profileForm.subscription_type">
              <option value="standard">Standard</option>
              <option value="premium">Premium</option>
            </select>
          </div>

          <div class="profile-modal-readonly">
            <span>Correo electrónico</span>
            <strong>{{ currentUser?.email }}</strong>
          </div>
        </template>

        <template v-if="isChangePasswordMode">
          <div class="profile-modal-group">
            <label for="old-password">Contraseña actual</label>

            <div class="password-input-wrapper">
              <input
                id="old-password"
                v-model="passwordForm.old_password"
                :type="showOldPassword ? 'text' : 'password'"
              />

              <button
                type="button"
                class="password-toggle-button"
                :aria-label="
                  showOldPassword ? 'Ocultar contrasena actual' : 'Mostrar contrasena actual'
                "
                @click="showOldPassword = !showOldPassword"
              >
                <EyeDownIcon v-if="showOldPassword" />
                <EyeUpIcon v-else />
              </button>
            </div>
          </div>

          <div class="profile-modal-group">
            <label for="new-password">Nueva contraseña</label>

            <div class="password-input-wrapper">
              <input
                id="new-password"
                v-model="passwordForm.new_password"
                :type="showNewPassword ? 'text' : 'password'"
              />

              <button
                type="button"
                class="password-toggle-button"
                :aria-label="
                  showNewPassword ? 'Ocultar nueva contrasena' : 'Mostrar nueva contrasena'
                "
                @click="showNewPassword = !showNewPassword"
              >
                <EyeDownIcon v-if="showNewPassword" />
                <EyeUpIcon v-else />
              </button>
            </div>
          </div>

          <div class="profile-modal-group">
            <label for="repeat-password">Repite la nueva contraseña</label>

            <div class="password-input-wrapper">
              <input
                id="repeat-password"
                v-model="passwordForm.repeat_password"
                :type="showRepeatPassword ? 'text' : 'password'"
              />

              <button
                type="button"
                class="password-toggle-button"
                :aria-label="
                  showRepeatPassword
                    ? 'Ocultar confirmacion de contrasena'
                    : 'Mostrar confirmacion de contrasena'
                "
                @click="showRepeatPassword = !showRepeatPassword"
              >
                <EyeDownIcon v-if="showRepeatPassword" />
                <EyeUpIcon v-else />
              </button>
            </div>
          </div>
        </template>

        <p v-if="localError" class="profile-modal-message profile-modal-message-error">
          {{ localError }}
        </p>

        <p v-if="errorMessage" class="profile-modal-message profile-modal-message-error">
          {{ errorMessage }}
        </p>

        <p v-if="successMessage" class="profile-modal-message profile-modal-message-success">
          {{ successMessage }}
        </p>

        <footer class="profile-modal-actions">
          <button type="button" class="profile-modal-cancel" @click="emit('cancel')">
            Cancelar
          </button>

          <button type="submit" class="profile-modal-submit" :disabled="isSubmitting">
            {{ submitButtonText }}
          </button>
        </footer>
      </form>
    </section>
  </div>
</template>

<style scoped>
.profile-modal-overlay {
  position: fixed;
  inset: 0;
  z-index: 50;
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding: 2rem 1.5rem;
  overflow-y: auto;
  background-color: rgba(15, 23, 42, 0.45);
}

.profile-modal {
  width: 100%;
  max-width: 34rem;
  padding: 1.7rem;

  max-height: none;
  overflow-y: visible;

  border: 1px solid var(--color-border);
  border-radius: 1rem;
  background-color: var(--color-bg);
  box-shadow: var(--shadow-soft);
}

.profile-modal-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 1rem;
  padding-bottom: 1.2rem;
  border-bottom: 1px solid var(--color-border);
}

.profile-modal-header h2 {
  margin: 0;
  color: var(--color-text);
  font-size: 1.4rem;
  font-weight: 800;
}

.profile-modal-header p {
  margin: 0.4rem 0 0;
  color: var(--color-text-muted);
  font-size: 0.95rem;
  line-height: 1.5;
}

.profile-modal-close {
  border: none;
  background: transparent;
  color: var(--color-text-muted);
  font-size: 2rem;
  line-height: 1;
  cursor: pointer;
}

.profile-modal-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding-top: 1.2rem;
}

.profile-modal-group {
  display: flex;
  flex-direction: column;
  gap: 0.45rem;
}

.profile-modal-group label {
  color: var(--color-text);
  font-size: 0.95rem;
  font-weight: 700;
}

.profile-modal-group input,
.profile-modal-group select {
  width: 100%;
  padding: 0.85rem 0.95rem;
  border: 1px solid var(--color-border);
  border-radius: 0.7rem;
  background-color: var(--color-bg);
  color: var(--color-text);
  font-size: 1rem;
}
.password-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.password-input-wrapper input {
  padding-right: 3rem;
}

.password-toggle-button {
  position: absolute;
  right: 0.85rem;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 1.8rem;
  height: 1.8rem;
  border: none;
  background: transparent;
  color: var(--color-text-muted);
  cursor: pointer;
}

.password-toggle-button svg {
  width: 1.25rem;
  height: 1.25rem;
}

.profile-modal-group input:focus,
.profile-modal-group select:focus {
  outline: 2px solid var(--color-text-muted);
  border-color: var(--color-primary);
}

.profile-modal-readonly {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
  padding: 0.9rem;
  border: 1px solid var(--color-border);
  border-radius: 0.7rem;
  background-color: var(--color-bg);
}

.profile-modal-readonly span {
  color: var(--color-text-muted);
  font-size: 0.85rem;
}

.profile-modal-readonly strong {
  color: var(--color-text);
  font-size: 0.95rem;
}

.profile-modal-message {
  margin: 0;
  padding: 0.85rem 1rem;
  border-radius: 0.7rem;
  font-size: 0.95rem;
  font-weight: 700;
}

.profile-modal-message-error {
  border: 1px solid var(--color-danger);
  color: var(--color-danger);
}

.profile-modal-message-success {
  border: 1px solid var(--color-primary);
  color: var(--color-primary);
}

.profile-modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.8rem;
  padding-top: 0.5rem;
}

.profile-modal-cancel,
.profile-modal-submit {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.85rem 1.2rem;
  border-radius: 0.7rem;
  font-weight: 700;
  cursor: pointer;
}

.profile-modal-cancel {
  border: 1px solid var(--color-border);
  background-color: var(--color-bg);
  color: var(--color-text);
}

.profile-modal-submit {
  border: none;
  background-color: var(--color-primary);
  color: var(--color-bg);
}

.profile-modal-submit:disabled {
  cursor: not-allowed;
  opacity: 0.7;
}

@media (max-width: 1025px) and (orientation: portrait) {
  .profile-modal {
    max-width: 42rem;
  }

  .profile-modal-header h2 {
    font-size: 2rem;
  }

  .profile-modal-header p {
    font-size: 1.5rem;
  }

  .profile-modal-group label {
    font-size: 1.5rem;
  }

  .profile-modal-group input,
  .profile-modal-group select {
    font-size: 1.5rem;
  }
  .password-input-wrapper input {
    padding-right: 4rem;
  }

  .password-toggle-button {
    right: 1rem;
    width: 2.4rem;
    height: 2.4rem;
  }

  .password-toggle-button svg {
    width: 1.7rem;
    height: 1.7rem;
  }

  .profile-modal-readonly span,
  .profile-modal-readonly strong {
    font-size: 1.5rem;
  }

  .profile-modal-message {
    font-size: 1.5rem;
  }

  .profile-modal-cancel,
  .profile-modal-submit {
    font-size: 1.5rem;
  }
}

@media (max-width: 768px) {
  .profile-modal {
    padding: 1.3rem;
  }

  .profile-modal-actions {
    flex-direction: column-reverse;
  }

  .profile-modal-cancel,
  .profile-modal-submit {
    width: 100%;
  }
}

@media (max-width: 950px) and (max-height: 520px) and (orientation: landscape) {
  .profile-modal-overlay {
    align-items: center;
    padding: 0.75rem 1rem;
  }

  .profile-modal {
    max-width: min(42rem, calc(100vw - 2rem));
    max-height: calc(100vh - 1.5rem);
    overflow-y: auto;
    padding: 1rem;
    border-radius: 0.9rem;
  }

  .profile-modal-header {
    gap: 0.75rem;
    padding-bottom: 0.75rem;
  }

  .profile-modal-header h2 {
    font-size: 1.25rem;
    line-height: 1.15;
  }

  .profile-modal-header p {
    margin-top: 0.25rem;
    font-size: 0.86rem;
    line-height: 1.3;
  }

  .profile-modal-close {
    font-size: 1.7rem;
  }

  .profile-modal-form {
    gap: 0.7rem;
    padding-top: 0.8rem;
  }

  .profile-modal-group {
    gap: 0.3rem;
  }

  .profile-modal-group label {
    font-size: 0.86rem;
  }

  .profile-modal-group input,
  .profile-modal-group select {
    min-height: 2.45rem;
    padding: 0 0.75rem;
    font-size: 0.95rem;
  }

  .password-input-wrapper input {
    padding-right: 2.75rem;
  }

  .password-toggle-button {
    right: 0.65rem;
    width: 1.7rem;
    height: 1.7rem;
  }

  .password-toggle-button svg {
    width: 1.1rem;
    height: 1.1rem;
  }

  .profile-modal-readonly {
    gap: 0.2rem;
    padding: 0.7rem 0.75rem;
  }

  .profile-modal-readonly span {
    font-size: 0.78rem;
  }

  .profile-modal-readonly strong {
    font-size: 0.9rem;
  }

  .profile-modal-message {
    padding: 0.65rem 0.8rem;
    font-size: 0.86rem;
  }

  .profile-modal-actions {
    flex-direction: row;
    justify-content: flex-end;
    gap: 0.6rem;
    padding-top: 0.2rem;
  }

  .profile-modal-cancel,
  .profile-modal-submit {
    width: auto;
    min-height: 2.45rem;
    padding: 0 1rem;
    font-size: 0.9rem;
  }
}
</style>

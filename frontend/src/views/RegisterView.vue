<script setup>
import { ref } from 'vue'
import { API_BASE_URL } from '@/config/api'

import MailIcon from '@/components/Icons/MailIcon.vue'
import LockerIcon from '@/components/Icons/LockerIcon.vue'
import PeopleIcon from '@/components/Icons/PeopleIcon.vue'
import ScheduleIcon from '@/components/Icons/ScheduleIcon.vue'

import AtentionIcon from '@/components/Icons/AtentionIcon.vue'

const email = ref('')
const password = ref('')
const passwordConfirm = ref('')
const showPassword = ref(false)
const showPasswordConfirm = ref(false)
const fecha = ref('')
const name = ref('')
const apellidos = ref('')

const successMessage = ref('')
const errorMessage = ref('')
const currentUser = ref(null)

const acceptedTerms = ref(false)
const wantsPremium = ref(false)

async function handleRegister() {
  if (!acceptedTerms.value) {
    errorMessage.value = 'Debes aceptar los términos y condiciones para registrarte'
    successMessage.value = ''
    currentUser.value = null
    return
  }

  if (password.value !== passwordConfirm.value) {
    errorMessage.value = 'Las contraseñas no coinciden'
    successMessage.value = ''
    currentUser.value = null
    return
  }

  const newUser = {
    email: email.value,
    password: password.value,
    name: name.value,
    surname: apellidos.value,
    date_of_birth: fecha.value,
  }
}
</script>

<template>
  <section class="register">
    <section class="register-grid">
      <div class="register-grid-content">
        <h1>Crea tu cuenta</h1>
        <h2>Crea tu cuenta para acceder a los servicios</h2>
        <form v-if="!currentUser" @submit.prevent="handleRegister">
          <label class="label" for="name">Nombre</label>
          <div class="placing">
            <PeopleIcon class="placing-icon" /><input
              v-model="name"
              id="name"
              type="text"
              placeholder="Tu nombre"
            />
          </div>
          <label class="label" for="apellidos">Apellidos</label>
          <div class="placing">
            <PeopleIcon class="placing-icon" /><input
              v-model="apellidos"
              id="apellidos"
              type="text"
              placeholder="Tus apellidos"
            />
          </div>
          <label class="label" for="fecha">Fecha de nacimiento</label>
          <div class="placing">
            <ScheduleIcon class="placing-icon" /><input
              v-model="fecha"
              id="fecha"
              type="date"
              placeholder="Tu fecha de nacimiento"
            />
          </div>
          <label class="label" for="email">Correo electrónico</label>
          <div class="placing">
            <MailIcon class="placing-icon" /><input
              v-model="email"
              id="email"
              type="email"
              placeholder="tu@email.com"
            />
          </div>
          <label class="label" for="password">Contraseña</label>
          <div class="placing">
            <LockerIcon class="placing-icon" />
            <input
              v-model="password"
              id="password"
              :type="showPassword ? 'text' : 'password'"
              placeholder="Tu contraseña"
            />
            <button
              class="password-toggle"
              type="button"
              :aria-label="showPassword ? 'Ocultar contrasena' : 'Mostrar contrasena'"
              @click="showPassword = !showPassword"
            >
              {{ showPassword ? '🙈' : '👁️' }}
            </button>
          </div>

          <label class="label" for="password-confirm">Confirmar contraseña</label>
          <div class="placing">
            <LockerIcon class="placing-icon" />
            <input
              v-model="passwordConfirm"
              id="password-confirm"
              :type="showPasswordConfirm ? 'text' : 'password'"
              placeholder="Repite tu contraseña"
            />
            <button
              class="password-toggle"
              type="button"
              :aria-label="
                showPasswordConfirm ? 'Ocultar confirmacion de contrasena' : 'Mostrar confirmacion de contrasena'
              "
              @click="showPasswordConfirm = !showPasswordConfirm"
            >
              {{ showPasswordConfirm ? '🙈' : '👁️' }}
            </button>
          </div>

          <div class="conditions">
            <label class="checkbox-row">
              <input v-model="wantsPremium" type="checkbox" />
              <span>
                Quiero registrarme como usuario premium y recibir la newsletter de Chronic Project.
              </span>
            </label>

            <label class="checkbox-row">
              <input v-model="acceptedTerms" type="checkbox" />
              <span>Acepto los términos y condiciones (ver al final de página).</span>
            </label>
          </div>

          <div class="error-registration" v-if="errorMessage">
            <p>{{ errorMessage }}</p>
          </div>

          <button class="register-button" type="submit">Registrar</button>
        </form>

        <div class="success-registration" v-if="successMessage && currentUser">
          <h2 class="success-title">{{ successMessage }}</h2>
          <p>Usuario {{ currentUser.name }} registrado</p>
          <p>Tu usuario: {{ currentUser.email }}</p>
          <p>Tu tipo de cuenta: {{ currentUser.subscription_type }}</p>
          <RouterLink to="/login">Inicia sesión</RouterLink>
        </div>

        <div v-if="!currentUser" class="hook-user">
          <p>¿Ya estas registrado?</p>
          <RouterLink to="/login">Accede aquí</RouterLink>
        </div>
      </div>
    </section>
    <div v-if="!currentUser" class="registration-terms">
      <div class="registration-terms-logo">
        <AtentionIcon />
      </div>
      <div class="registration-terms-text">
        <h3>Términos y condiciones</h3>
        <p>
          * Chronic Project es una aplicación académica orientada al registro y consulta de
          mediciones de glucemia. No sustituye el criterio médico ni debe utilizarse como
          herramienta diagnóstica.
        </p>

        <p>
          * Al registrarte como usuario premium aceptas suscribirte a la newsletter de Chronic
          Project, que puede incluir novedades, información relacionada con la aplicación y
          contenido publicitario.
        </p>
      </div>
    </div>
  </section>
</template>
<style scoped>
.conditions {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin: 8px;
}

.register {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-color: var(--color-bg);
  min-height: calc(100vh - 80px);
  padding: 2rem 1rem;
}
.register-grid {
  width: 100%;
  max-width: 520px;
}
.register-grid-content {
  display: flex;
  flex-direction: column;
  background-color: var(--color-surface);
  border-radius: 1rem;
  padding: 1rem;
}
.register-grid-content h1,
.register-grid-content h2 {
  margin: 8px;
  color: var(--color-primary-dark);
}
.register-grid-content form {
  display: flex;
  flex-direction: column;
  justify-items: center;
  gap: 0.5rem;
  width: 90%;
  margin: 8px;
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
}
.placing .placing-icon {
  flex-shrink: 0;
}

.password-toggle {
  border: none;
  background: transparent;
  cursor: pointer;
  padding: 0 0.8rem;
  font-size: 1rem;
  flex-shrink: 0;
}
.forgot {
  text-align: center;
  font-weight: 600;
  color: var(--color-primary);
  font-size: 14px;
}
.register-button {
  text-align: center;
  border: none;
  border-style: none;
  border-radius: 0.4rem;
  background-color: var(--color-primary);
  color: var(--color-bg);
  padding: 0.8rem;
  cursor: pointer;
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
.success-registration {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  margin: 1rem 8px 0;
  padding: 1rem;
  border: 1px solid var(--color-primary);
  border-radius: 0.8rem;
  background-color: var(--color-bg);
}

.success-registration p {
  margin: 0;
  color: var(--color-text);
}

.success-registration .success-title {
  font-weight: 700;
  color: var(--color-primary-dark);
}

.success-registration a {
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

.error-registration {
  margin: 1rem 8px 0;
  padding: 0.8rem 1rem;
  border: 1px solid var(--color-danger);
  border-radius: 0.6rem;
  background-color: var(--color-bg);
}

.error-registration p {
  margin: 0;
  color: var(--color-danger);
  font-weight: 600;
  text-align: center;
}
.registration-terms {
  display: flex;
  justify-content: start;
  align-items: center;
  width: 100%;
  max-width: 520px;
  background-color: var(--color-success-soft);
  border: 1px solid var(--color-success-border);
  border-radius: 1rem;
  margin-top: 2rem;
  padding: 1rem;
}
.registration-terms-logo {
  display: flex;
  justify-content: center;
  color: var(--color-success);
  width: 90px;
}
.registration-terms-text {
  display: flex;
  flex-direction: column;
  gap: 8px;
  color: var(--color-success);
}
.registration-terms-text p,
.registration-terms-text h3 {
  margin: 0;
}
.registration-terms-text h3 {
  font-size: 12px;
  font-weight: bolder;
}
.registration-terms-text p {
  font-size: 12px;

  max-width: 500px;
}

@media (max-width: 1025px) and (orientation: portrait) {
  .register-grid {
    width: 100%;
    max-width: 720px;
  }
  .register-grid-content h1 {
    font-size: 32px;
  }

  .register-grid-content h2 {
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

  .register-button {
    font-size: 24px;
  }

  .hook-user p {
    font-size: 24px;
  }

  .hook-user a {
    font-size: 24px;
  }
  .success-registration {
    font-size: 22px;
  }

  .success-registration a {
    font-size: 22px;
  }

  .error-registration {
    font-size: 22px;
  }
  .registration-terms-logo {
    width: 70px;
    flex-shrink: 0;
  }
  .registration-terms-text {
    gap: 4px;
  }
  .registration-terms-text h3 {
    font-size: 20px;
  }

  .registration-terms-text p {
    font-size: 18px;
  }

  .registration-terms-logo svg {
    width: 42px;
    height: 42px;
  }
}
@media (max-width: 768px) {
  .register-grid {
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

  .success-registration {
    margin: 1rem 0 0;
    padding: 0.9rem;
  }

  .success-registration a {
    width: 100%;
    padding: 0.7rem;
  }

  .error-registration {
    margin: 1rem 0 0;
    padding: 0.8rem;
  }

  .registration-terms-text h3 {
    font-size: 16px;
  }

  .registration-terms-text p {
    font-size: 14px;
  }

  .registration-terms-logo {
    width: 50px;
    flex-shrink: 0;
  }

  .registration-terms-logo svg {
    width: 32px;
    height: 32px;
  }
}
</style>

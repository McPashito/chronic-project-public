<script setup>
import { ref } from 'vue'

import MailIcon from '@/components/Icons/MailIcon.vue'
import LockerIcon from '@/components/Icons/LockerIcon.vue'
import EyeDownIcon from '@/components/Icons/EyeDownIcon.vue'
import EyeUpIcon from '@/components/Icons/EyeUpIcon.vue'
import PeopleIcon from '@/components/Icons/PeopleIcon.vue'
import ScheduleIcon from '@/components/Icons/ScheduleIcon.vue'

import AtentionIcon from '@/components/Icons/AtentionIcon.vue'

const showPassword = ref(false)
const showPasswordConfirm = ref(false)

</script>

<template>
  <section class="register">
    <section class="register-grid">
      <div class="register-grid-content">
        <h1>Crea tu cuenta</h1>
        <h2>Crea tu cuenta para acceder a los servicios</h2>

        <div class="register-demo-notice" role="note">
          <strong>Registro deshabilitado en la demo pública</strong>
          <p>
            Chronic Project trabaja con datos de salud. Para evitar que se introduzcan datos
            médicos reales en una demo de portfolio, el registro público está desactivado.
          </p>
          <p>Puedes probar la aplicación con las cuentas demo preparadas.</p>
        </div>

        <form class="register-preview" aria-disabled="true">
          <label class="label" for="name">Nombre</label>
          <div class="placing">
            <PeopleIcon class="placing-icon" /><input
              id="name"
              type="text"
              disabled
              placeholder="Tu nombre"
            />
          </div>
          <label class="label" for="apellidos">Apellidos</label>
          <div class="placing">
            <PeopleIcon class="placing-icon" /><input
              id="apellidos"
              type="text"
              disabled
              placeholder="Tus apellidos"
            />
          </div>
          <label class="label" for="fecha">Fecha de nacimiento</label>
          <div class="placing">
            <ScheduleIcon class="placing-icon" /><input
              id="fecha"
              type="date"
              disabled
              placeholder="Tu fecha de nacimiento"
            />
          </div>
          <label class="label" for="email">Correo electrónico</label>
          <div class="placing">
            <MailIcon class="placing-icon" /><input
              id="email"
              type="email"
              disabled
              placeholder="tu@email.com"
            />
          </div>
          <label class="label" for="password">Contraseña</label>
          <div class="placing">
            <LockerIcon class="placing-icon" />
            <input
              id="password"
              :type="showPassword ? 'text' : 'password'"
              disabled
              placeholder="Tu contraseña"
            />
            <button
              class="password-toggle"
              type="button"
              :aria-label="showPassword ? 'Ocultar contrasena' : 'Mostrar contrasena'"
              @click="showPassword = !showPassword"
            >
              <EyeUpIcon v-if="showPassword" />
              <EyeDownIcon v-else />
            </button>
          </div>

          <label class="label" for="password-confirm">Confirmar contraseña</label>
          <div class="placing">
            <LockerIcon class="placing-icon" />
            <input
              id="password-confirm"
              :type="showPasswordConfirm ? 'text' : 'password'"
              disabled
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
              <EyeUpIcon v-if="showPasswordConfirm" />
              <EyeDownIcon v-else />
            </button>
          </div>

          <div class="conditions">
            <label class="checkbox-row">
              <input type="checkbox" disabled />
              <span>
                Quiero registrarme como usuario premium y recibir la newsletter de Chronic Project.
              </span>
            </label>

            <label class="checkbox-row">
              <input type="checkbox" disabled />
              <span>Acepto los términos y condiciones (ver al final de página).</span>
            </label>
          </div>

          <button class="register-button" type="button" disabled>
            Registro no disponible en la demo
          </button>
        </form>

        <div class="demo-access">
          <p>
            Para probar la demo pública, utiliza las cuentas demo indicadas en la documentación
            del proyecto.
          </p>
          <RouterLink class="demo-login-link" to="/login">Ir al login</RouterLink>
        </div>
      </div>
    </section>
    <div class="registration-terms">
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

.register-demo-notice {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin: 1rem 8px;
  padding: 1rem;
  border: 1px solid var(--color-success-border);
  border-radius: 0.8rem;
  background-color: var(--color-success-soft);
  color: var(--color-text);
}

.register-demo-notice strong {
  color: var(--color-primary-dark);
}

.register-demo-notice p {
  margin: 0;
}

.register-preview {
  opacity: 0.78;
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

.placing input:disabled,
.conditions input:disabled {
  cursor: not-allowed;
}

.placing input:disabled {
  color: var(--color-text-muted);
  background-color: var(--color-bg);
}
.placing .placing-icon {
  flex-shrink: 0;
}

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

.register-button:disabled {
  opacity: 0.75;
  cursor: not-allowed;
}

.demo-access {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
  margin: 1rem 8px 0;
  padding: 0.8rem;
  border: 1px solid var(--color-border);
  border-radius: 0.6rem;
  background-color: var(--color-bg);
}

.demo-access p {
  margin: 0;
  color: var(--color-text);
}

.demo-access a {
  display: inline-flex;
  justify-content: center;
  align-items: center;
  padding: 0.75rem 1rem;
  border-radius: 0.4rem;
  background-color: var(--color-primary);
  color: var(--color-bg);
  text-decoration: none;
  font-weight: 600;
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

  .register-button {
    font-size: 24px;
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

  .demo-access {
    margin: 1rem 0 0;
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

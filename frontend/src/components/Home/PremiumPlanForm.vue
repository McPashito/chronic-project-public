<script setup>
import { computed } from 'vue'

import SecurityIcon from '@/components/Icons/SecurityIcon.vue'
import StarIcon from '@/components/Icons/StarIcon.vue'

const props = defineProps({
  currentUser: {
    type: Object,
    default: null,
  },
  isSubmitting: {
    type: Boolean,
    default: false,
  },
  errorMessage: {
    type: String,
    default: '',
  },
  successMessage: {
    type: String,
    default: '',
  },
})

const emit = defineEmits(['confirm-plan-change', 'cancel'])

const currentPlan = computed(() => {
  return props.currentUser?.subscription_type === 'premium' ? 'premium' : 'standard'
})

const isPremium = computed(() => currentPlan.value === 'premium')

const currentPlanLabel = computed(() => {
  return isPremium.value ? 'Premium' : 'Standard'
})

const targetPlan = computed(() => {
  return isPremium.value ? 'standard' : 'premium'
})

const submitButtonText = computed(() => {
  if (props.isSubmitting) return 'Actualizando...'

  return isPremium.value ? 'Volver a Standard' : 'Activar Premium'
})

const modalTitle = computed(() => {
  return isPremium.value ? 'Gestionar plan Premium' : 'Actualiza a Premium'
})

const modalDescription = computed(() => {
  if (isPremium.value) {
    return 'Actualmente tienes acceso completo a tu historial de glucemias.'
  }

  return 'Obten acceso completo a tus registros anteriores a 30 días'
})

function handleConfirm() {
  emit('confirm-plan-change', targetPlan.value)
}
</script>

<template>
  <div class="premium-plan-overlay">
    <section
      class="premium-plan-modal"
      role="dialog"
      aria-modal="true"
      aria-labelledby="premium-plan-title"
    >
      <header class="premium-plan-header">
        <div>
          <span class="premium-plan-kicker">Plan de cuenta</span>
          <h2 id="premium-plan-title">{{ modalTitle }}</h2>
          <p>{{ modalDescription }}</p>
        </div>

        <button
          type="button"
          class="premium-plan-close"
          :disabled="isSubmitting"
          aria-label="Cerrar modal"
          @click="emit('cancel')"
        >
          ×
        </button>
      </header>

      <div class="premium-plan-current">
        <div class="premium-plan-current-icon">
          <StarIcon />
        </div>

        <div>
          <span>Plan actual</span>
          <strong>{{ currentPlanLabel }}</strong>
        </div>
      </div>

      <div class="premium-plan-benefits">
        <article class="premium-plan-benefit">
          <div class="premium-plan-benefit-icon">
            <SecurityIcon />
          </div>

          <div>
            <strong>Historial completo</strong>
            <p>Consulta tus registros antiguos sin limitación de 30 días.</p>
          </div>
        </article>
      </div>

      <div class="premium-plan-notice">
        <strong>Condiciones premium</strong>
        <p>
          El plan Premium incluye newsletter con novedades, consejos de salud y
          promociones/publicidad.
        </p>
      </div>

      <p v-if="errorMessage" class="premium-plan-message premium-plan-message-error">
        {{ errorMessage }}
      </p>

      <p v-if="successMessage" class="premium-plan-message premium-plan-message-success">
        {{ successMessage }}
      </p>

      <footer class="premium-plan-actions">
        <button
          type="button"
          class="premium-plan-cancel"
          :disabled="isSubmitting"
          @click="emit('cancel')"
        >
          Cancelar
        </button>

        <button
          type="button"
          class="premium-plan-submit"
          :disabled="isSubmitting"
          @click="handleConfirm"
        >
          {{ submitButtonText }}
        </button>
      </footer>
    </section>
  </div>
</template>

<style scoped>
.premium-plan-overlay {
  position: fixed;
  inset: 0;
  z-index: 60;

  display: flex;
  align-items: flex-start;
  justify-content: center;

  padding: 2rem 1.5rem;
  overflow-y: auto;

  background-color: rgba(15, 23, 42, 0.45);
}

.premium-plan-modal {
  width: 100%;
  max-width: 42rem;
  padding: 1.7rem;

  border: 1px solid var(--color-border);
  border-radius: 1rem;
  background-color: var(--color-bg);
  box-shadow: var(--shadow-soft);
}

.premium-plan-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 1rem;

  padding-bottom: 1.2rem;
  border-bottom: 1px solid var(--color-border);
}

.premium-plan-kicker {
  display: inline-flex;
  margin-bottom: 0.45rem;

  color: var(--color-primary);
  font-size: 0.85rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.premium-plan-header h2 {
  margin: 0;

  color: var(--color-text);
  font-size: 1.45rem;
  font-weight: 800;
}

.premium-plan-header p {
  margin: 0.45rem 0 0;

  color: var(--color-text-muted);
  font-size: 0.95rem;
  line-height: 1.5;
}

.premium-plan-close {
  border: none;
  background: transparent;
  color: var(--color-text-muted);
  font-size: 2rem;
  line-height: 1;
  cursor: pointer;
}

.premium-plan-close:disabled {
  cursor: not-allowed;
  opacity: 0.6;
}

.premium-plan-current {
  display: flex;
  align-items: center;
  gap: 1rem;

  margin-top: 1.2rem;
  padding: 1rem;

  border: 1px solid var(--color-border);
  border-radius: 0.9rem;
  background-color: var(--color-surface);
}

.premium-plan-current-icon,
.premium-plan-benefit-icon {
  display: flex;
  align-items: center;
  justify-content: center;

  width: 3rem;
  height: 3rem;
  flex-shrink: 0;

  border-radius: 50%;
  background-color: var(--dashboard-blue-bg);
  color: var(--dashboard-blue-icon);
}

.premium-plan-current-icon svg,
.premium-plan-benefit-icon svg {
  width: 1.55rem;
  height: 1.55rem;
}

.premium-plan-current span {
  display: block;

  color: var(--color-text-muted);
  font-size: 0.85rem;
  font-weight: 700;
}

.premium-plan-current strong {
  display: block;

  margin-top: 0.15rem;

  color: var(--color-text);
  font-size: 1.15rem;
  font-weight: 800;
}

.premium-plan-benefits {
  display: flex;
  flex-direction: column;
  gap: 0.9rem;

  margin-top: 1rem;
}

.premium-plan-benefit {
  display: flex;
  gap: 1rem;

  padding: 1rem;

  border: 1px solid var(--color-border);
  border-radius: 0.9rem;
  background-color: var(--color-bg);
}

.premium-plan-benefit strong {
  display: block;

  color: var(--color-text);
  font-size: 1rem;
}

.premium-plan-benefit p {
  margin: 0.3rem 0 0;

  color: var(--color-text-muted);
  font-size: 0.92rem;
  line-height: 1.45;
}

.premium-plan-notice {
  margin-top: 1rem;
  padding: 1rem;

  border: 1px solid var(--color-warning);
  border-radius: 0.9rem;
  background-color: var(--dashboard-yellow-bg);
}

.premium-plan-notice strong {
  color: var(--color-text);
  font-size: 0.95rem;
}

.premium-plan-notice p {
  margin: 0.35rem 0 0;

  color: var(--color-text-muted);
  font-size: 0.9rem;
  line-height: 1.5;
}

.premium-plan-message {
  margin: 1rem 0 0;
  padding: 0.85rem 1rem;

  border-radius: 0.7rem;
  font-size: 0.95rem;
  font-weight: 700;
}

.premium-plan-message-error {
  border: 1px solid var(--color-danger);
  color: var(--color-danger);
}

.premium-plan-message-success {
  border: 1px solid var(--color-primary);
  color: var(--color-primary);
}

.premium-plan-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.8rem;

  padding-top: 1.2rem;
}

.premium-plan-cancel,
.premium-plan-submit {
  display: inline-flex;
  align-items: center;
  justify-content: center;

  padding: 0.85rem 1.2rem;

  border-radius: 0.7rem;
  font: inherit;
  font-weight: 800;
  cursor: pointer;
}

.premium-plan-cancel {
  border: 1px solid var(--color-border);
  background-color: var(--color-bg);
  color: var(--color-text);
}

.premium-plan-submit {
  border: 1px solid var(--color-primary);
  background-color: var(--color-primary);
  color: var(--color-bg);
}

.premium-plan-cancel:disabled,
.premium-plan-submit:disabled {
  cursor: not-allowed;
  opacity: 0.7;
}

@media (max-width: 1025px) and (orientation: portrait) {
  .premium-plan-modal {
    max-width: 44rem;
  }

  .premium-plan-kicker {
    font-size: 1.1rem;
  }

  .premium-plan-header h2 {
    font-size: 2rem;
  }

  .premium-plan-header p {
    font-size: 1.45rem;
  }

  .premium-plan-current span,
  .premium-plan-current strong {
    font-size: 1.45rem;
  }

  .premium-plan-benefit strong,
  .premium-plan-notice strong {
    font-size: 1.45rem;
  }

  .premium-plan-benefit p,
  .premium-plan-notice p,
  .premium-plan-message,
  .premium-plan-cancel,
  .premium-plan-submit {
    font-size: 1.35rem;
  }
}

@media (max-width: 769px) {
  .premium-plan-overlay {
    padding: 1rem;
  }

  .premium-plan-modal {
    padding: 1.3rem;
  }

  .premium-plan-header {
    gap: 0.75rem;
  }

  .premium-plan-benefit {
    flex-direction: column;
  }

  .premium-plan-actions {
    flex-direction: column-reverse;
  }

  .premium-plan-cancel,
  .premium-plan-submit {
    width: 100%;
  }
}

@media (max-width: 950px) and (max-height: 520px) and (orientation: landscape) {
  .premium-plan-overlay {
    align-items: center;
    padding: 0.75rem 1rem;
  }

  .premium-plan-modal {
    display: grid;
    grid-template-columns: minmax(0, 0.9fr) minmax(0, 1.1fr);
    column-gap: 0.85rem;
    row-gap: 0.85rem;
    max-width: min(48rem, calc(100vw - 2rem));
    max-height: calc(100vh - 1.5rem);
    overflow-y: auto;
    padding: 1rem;
    border-radius: 0.85rem;
  }

  .premium-plan-header,
  .premium-plan-notice,
  .premium-plan-message,
  .premium-plan-actions {
    grid-column: 1 / -1;
  }

  .premium-plan-header {
    padding-bottom: 0.75rem;
  }

  .premium-plan-kicker {
    margin-bottom: 0.25rem;
    font-size: 0.78rem;
  }

  .premium-plan-header h2 {
    font-size: 1.25rem;
    line-height: 1.15;
  }

  .premium-plan-header p {
    margin-top: 0.3rem;
    font-size: 0.86rem;
    line-height: 1.3;
  }

  .premium-plan-close {
    font-size: 1.7rem;
  }

  .premium-plan-current,
  .premium-plan-benefits,
  .premium-plan-notice {
    margin-top: 0;
  }

  .premium-plan-current,
  .premium-plan-benefit {
    min-height: 5rem;
    padding: 0.85rem;
  }

  .premium-plan-benefits {
    gap: 0;
  }

  .premium-plan-benefit {
    flex-direction: row;
    align-items: center;
  }

  .premium-plan-current-icon,
  .premium-plan-benefit-icon {
    width: 2.45rem;
    height: 2.45rem;
  }

  .premium-plan-current-icon svg,
  .premium-plan-benefit-icon svg {
    width: 1.25rem;
    height: 1.25rem;
  }

  .premium-plan-current span {
    font-size: 0.78rem;
  }

  .premium-plan-current strong {
    font-size: 1rem;
  }

  .premium-plan-benefit strong,
  .premium-plan-notice strong {
    font-size: 0.9rem;
  }

  .premium-plan-benefit p,
  .premium-plan-notice p {
    font-size: 0.82rem;
    line-height: 1.3;
  }

  .premium-plan-notice {
    padding: 0.85rem;
  }

  .premium-plan-actions {
    flex-direction: row;
    justify-content: flex-end;
    padding-top: 0;
  }

  .premium-plan-cancel,
  .premium-plan-submit {
    width: auto;
    min-height: 2.55rem;
    padding: 0 1rem;
    font-size: 0.9rem;
  }
}
</style>

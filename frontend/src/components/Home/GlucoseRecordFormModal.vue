<script setup>
import { computed, reactive, watch } from 'vue'

const props = defineProps({
  mode: {
    type: String,
    default: 'create',
    validator: (value) => ['create', 'edit'].includes(value),
  },
  initialRecord: {
    type: Object,
    default: null,
  },
  errorMessage: {
    type: String,
    default: '',
  },
  isSubmitting: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['submit', 'cancel'])

const form = reactive({
  date: '',
  time: '',
  glucose_value: '',
  moment_of_day: '',
  notes: '',
})

const localError = reactive({
  message: '',
})

const modalTitle = computed(() => {
  return props.mode === 'edit' ? 'Editar glucemia' : 'Añadir nueva glucemia'
})

const submitButtonText = computed(() => {
  if (props.isSubmitting) {
    return props.mode === 'edit' ? 'Guardando...' : 'Creando...'
  }

  return props.mode === 'edit' ? 'Guardar cambios' : 'Crear glucemia'
})

function getTodayDate() {
  return new Date().toISOString().split('T')[0]
}

function getCurrentTime() {
  const now = new Date()
  const hours = String(now.getHours()).padStart(2, '0')
  const minutes = String(now.getMinutes()).padStart(2, '0')

  return `${hours}:${minutes}`
}

function fillForm() {
  localError.message = ''

  if (props.mode === 'edit' && props.initialRecord) {
    form.date = props.initialRecord.date || ''
    form.time = props.initialRecord.time?.slice(0, 5) || ''
    form.glucose_value = props.initialRecord.glucose_value || ''
    form.moment_of_day = props.initialRecord.moment_of_day || ''
    form.notes = props.initialRecord.notes || ''
    return
  }

  form.date = getTodayDate()
  form.time = getCurrentTime()
  form.glucose_value = ''
  form.moment_of_day = ''
  form.notes = ''
}

watch(
  () => [props.mode, props.initialRecord],
  () => {
    fillForm()
  },
  { immediate: true },
)

function validateForm() {
  localError.message = ''

  if (!form.date) {
    localError.message = 'Debes indicar una fecha.'
    return false
  }

  if (!form.time) {
    localError.message = 'Debes indicar una hora.'
    return false
  }

  if (form.glucose_value === '' || form.glucose_value === null) {
    localError.message = 'Debes indicar el valor de glucemia.'
    return false
  }

  const glucoseValue = Number(form.glucose_value)

  if (Number.isNaN(glucoseValue)) {
    localError.message = 'El valor de glucemia debe ser numérico.'
    return false
  }

  if (glucoseValue < 20 || glucoseValue > 600) {
    localError.message = 'El valor de glucemia debe estar entre 20 y 600 mg/dL.'
    return false
  }

  if (!form.moment_of_day) {
    localError.message = 'Debes seleccionar el momento del día.'
    return false
  }

  if (form.notes && form.notes.length > 255) {
    localError.message = 'Las notas no pueden superar los 255 caracteres.'
    return false
  }

  return true
}

function handleSubmit() {
  if (!validateForm()) {
    return
  }

  emit('submit', {
    date: form.date,
    time: form.time.length === 5 ? `${form.time}:00` : form.time,
    glucose_value: Number(form.glucose_value),
    moment_of_day: form.moment_of_day,
    notes: form.notes.trim() || null,
  })
}

function handleCancel() {
  localError.message = ''
  emit('cancel')
}
</script>

<template>
  <div class="glucose-record-modal">
    <div
      class="glucose-record-modal-box"
      role="dialog"
      aria-modal="true"
      aria-labelledby="glucose-record-modal-title"
    >
      <header class="glucose-record-modal-header">
        <div>
          <span class="glucose-record-modal-kicker">
            {{ mode === 'edit' ? 'Modificar registro' : 'Nuevo registro' }}
          </span>

          <h3 id="glucose-record-modal-title">{{ modalTitle }}</h3>
        </div>

        <button
          type="button"
          class="glucose-record-modal-close"
          :disabled="isSubmitting"
          aria-label="Cerrar formulario"
          @click="handleCancel"
        >
          ×
        </button>
      </header>

      <div v-if="localError.message || errorMessage" class="glucose-record-error">
        {{ localError.message || errorMessage }}
      </div>

      <form class="glucose-record-form" @submit.prevent="handleSubmit">
        <div class="form-row">
          <div class="form-group">
            <label for="glucose-date">Fecha</label>
            <input id="glucose-date" v-model="form.date" type="date" :disabled="isSubmitting" />
          </div>

          <div class="form-group">
            <label for="glucose-time">Hora</label>
            <input id="glucose-time" v-model="form.time" type="time" :disabled="isSubmitting" />
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label for="glucose-value">Valor de glucemia</label>
            <div class="glucose-value-control">
              <input
                id="glucose-value"
                v-model="form.glucose_value"
                type="number"
                min="20"
                max="600"
                step="1"
                placeholder="Ej. 110"
                :disabled="isSubmitting"
              />
              <span>mg/dL</span>
            </div>
          </div>

          <div class="form-group">
            <label for="moment-of-day">Momento del día</label>
            <select id="moment-of-day" v-model="form.moment_of_day" :disabled="isSubmitting">
              <option value="">Selecciona una opción</option>
              <option value="fasting">Ayunas</option>
              <option value="before_meal">Antes de comer</option>
              <option value="after_meal">Después de comer</option>
              <option value="night">Noche</option>
              <option value="other">Otro</option>
            </select>
          </div>
        </div>

        <div class="form-group">
          <label for="glucose-notes">Notas</label>
          <textarea
            id="glucose-notes"
            v-model="form.notes"
            rows="4"
            maxlength="255"
            placeholder="Añade una observación opcional"
            :disabled="isSubmitting"
          ></textarea>

          <span class="notes-counter">{{ form.notes.length }}/255</span>
        </div>

        <div class="glucose-record-modal-actions">
          <button
            type="button"
            class="modal-button modal-button-secondary"
            :disabled="isSubmitting"
            @click="handleCancel"
          >
            Cancelar
          </button>

          <button type="submit" class="modal-button modal-button-primary" :disabled="isSubmitting">
            {{ submitButtonText }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<style scoped>
.glucose-record-modal {
  position: fixed;
  inset: 0;
  z-index: 1100;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1.5rem;
  background-color: rgba(15, 23, 42, 0.5);
}

.glucose-record-modal-box {
  width: 100%;
  max-width: 620px;
  max-height: calc(100vh - 3rem);
  overflow-y: auto;
  background-color: var(--color-bg);
  border: 1px solid var(--color-border);
  border-radius: 1.25rem;
  box-shadow: 0 24px 60px rgba(15, 23, 42, 0.28);
}

.glucose-record-modal-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 1rem;
  padding: 1.5rem 1.5rem 1rem;
  border-bottom: 1px solid var(--color-border);
}

.glucose-record-modal-kicker {
  display: block;
  margin-bottom: 0.25rem;
  color: var(--color-primary);
  font-size: 0.8rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.glucose-record-modal-header h3 {
  margin: 0;
  color: var(--color-text);
  font-size: 1.35rem;
}

.glucose-record-modal-close {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 2.25rem;
  height: 2.25rem;
  border: 1px solid var(--color-border);
  border-radius: 999px;
  background-color: var(--color-bg);
  color: var(--color-text-muted);
  font-size: 1.5rem;
  line-height: 1;
  cursor: pointer;
}

.glucose-record-modal-close:hover {
  color: var(--color-text);
  border-color: var(--color-primary);
}

.glucose-record-modal-close:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.glucose-record-error {
  margin: 1rem 1.5rem 0;
  padding: 0.85rem 1rem;
  border: 1px solid rgba(220, 38, 38, 0.25);
  border-radius: 0.9rem;
  background-color: rgba(220, 38, 38, 0.08);
  color: var(--color-danger);
  font-size: 0.95rem;
  font-weight: 600;
  line-height: 1.4;
}

.glucose-record-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding: 1.5rem;
}

.form-row {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.45rem;
}

.form-group label {
  color: var(--color-text);
  font-size: 0.95rem;
  font-weight: 700;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  border: 1px solid var(--color-border);
  border-radius: 0.85rem;
  background-color: var(--color-bg);
  color: var(--color-text);
  font: inherit;
  outline: none;
}

.form-group input,
.form-group select {
  min-height: 2.75rem;
  padding: 0 0.85rem;
}

.form-group textarea {
  resize: vertical;
  min-height: 6rem;
  padding: 0.85rem;
  line-height: 1.45;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.12);
}

.form-group input:disabled,
.form-group select:disabled,
.form-group textarea:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.glucose-value-control {
  display: flex;
  align-items: center;
  overflow: hidden;
  border: 1px solid var(--color-border);
  border-radius: 0.85rem;
  background-color: var(--color-bg);
}

.glucose-value-control:focus-within {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.12);
}

.glucose-value-control input {
  border: none;
  border-radius: 0;
  box-shadow: none;
}

.glucose-value-control input:focus {
  border: none;
  box-shadow: none;
}

.glucose-value-control span {
  padding: 0 0.85rem;
  color: var(--color-text-muted);
  font-size: 0.9rem;
  white-space: nowrap;
  border-left: 1px solid var(--color-border);
}

.notes-counter {
  align-self: flex-end;
  color: var(--color-text-muted);
  font-size: 0.8rem;
}

.glucose-record-modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  margin-top: 0.5rem;
}

.modal-button {
  border: none;
  border-radius: 999px;
  padding: 0.75rem 1.1rem;
  font-weight: 700;
  cursor: pointer;
}

.modal-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.modal-button-secondary {
  border: 1px solid var(--color-border);
  background-color: var(--color-bg);
  color: var(--color-text);
}

.modal-button-secondary:hover:not(:disabled) {
  border-color: var(--color-primary);
  color: var(--color-primary);
}

.modal-button-primary {
  background-color: var(--color-primary);
  color: white;
}

.modal-button-primary:hover:not(:disabled) {
  background-color: var(--color-primary-dark);
}

/* Tablet */
@media (max-width: 768px) {
  .glucose-record-modal {
    padding: 1rem;
    align-items: flex-start;
  }

  .glucose-record-modal-box {
    max-width: 560px;
    margin-top: 2rem;
    max-height: calc(100vh - 4rem);
    border-radius: 1rem;
  }

  .glucose-record-modal-header {
    padding: 1.25rem 1.25rem 0.9rem;
  }

  .glucose-record-modal-header h3 {
    font-size: 1.2rem;
  }

  .glucose-record-form {
    padding: 1.25rem;
  }

  .form-row {
    gap: 0.85rem;
  }
}

/* Móvil */
@media (max-width: 560px) {
  .glucose-record-modal {
    padding: 0.75rem;
    align-items: flex-start;
  }

  .glucose-record-modal-box {
    margin-top: 1rem;
    max-height: calc(100vh - 2rem);
    border-radius: 0.9rem;
  }

  .glucose-record-modal-header {
    padding: 1rem;
  }

  .glucose-record-modal-kicker {
    font-size: 0.72rem;
  }

  .glucose-record-modal-header h3 {
    font-size: 1.1rem;
  }

  .glucose-record-modal-close {
    width: 2rem;
    height: 2rem;
    font-size: 1.3rem;
  }

  .glucose-record-error {
    margin: 0.85rem 1rem 0;
    font-size: 0.9rem;
  }

  .glucose-record-form {
    padding: 1rem;
  }

  .form-row {
    grid-template-columns: 1fr;
  }

  .glucose-record-modal-actions {
    flex-direction: column-reverse;
  }

  .modal-button {
    width: 100%;
  }
}

@media (max-width: 950px) and (max-height: 520px) and (orientation: landscape) {
  .glucose-record-modal {
    padding: 0.75rem 1rem;
  }

  .glucose-record-modal-box {
    max-width: min(42rem, calc(100vw - 2rem));
    max-height: calc(100vh - 1.5rem);
    border-radius: 0.95rem;
  }

  .glucose-record-modal-header {
    padding: 1rem 1rem 0.7rem;
  }

  .glucose-record-modal-kicker {
    margin-bottom: 0.18rem;
    font-size: 0.72rem;
  }

  .glucose-record-modal-header h3 {
    font-size: 1.18rem;
    line-height: 1.15;
  }

  .glucose-record-modal-close {
    width: 2rem;
    height: 2rem;
    font-size: 1.3rem;
  }

  .glucose-record-error {
    margin: 0.75rem 1rem 0;
    padding: 0.65rem 0.8rem;
    font-size: 0.86rem;
  }

  .glucose-record-form {
    gap: 0.7rem;
    padding: 1rem;
  }

  .form-row {
    gap: 0.75rem;
  }

  .form-group {
    gap: 0.3rem;
  }

  .form-group label {
    font-size: 0.86rem;
  }

  .form-group input,
  .form-group select {
    min-height: 2.45rem;
    padding: 0 0.75rem;
  }

  .form-group textarea {
    min-height: 3.35rem;
    padding: 0.7rem 0.75rem;
    line-height: 1.3;
  }

  .notes-counter {
    font-size: 0.72rem;
  }

  .glucose-record-modal-actions {
    gap: 0.6rem;
    margin-top: 0.2rem;
  }

  .modal-button {
    padding: 0.65rem 1rem;
  }
}
</style>

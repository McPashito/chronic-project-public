<script setup>
import { computed, ref } from 'vue'

const props = defineProps({
  records: {
    type: Array,
    default: () => [],
  },
  variant: {
    type: String,
    default: 'compact',
  },
  pageSize: {
    type: Number,
    default: 10,
  },
})

const emit = defineEmits(['delete-record', 'edit-record'])

const momentLabels = {
  fasting: 'En ayunas',
  before_meal: 'Antes de comer',
  after_meal: 'Después de comer',
  night: 'Noche',
  other: 'Otro',
}

const currentPage = ref(1)

const recordToDelete = ref(null)

function askDeleteRecord(record) {
  recordToDelete.value = record
}

function cancelDeleteRecord() {
  recordToDelete.value = null
}
function confirmDeleteRecord() {
  emit('delete-record', recordToDelete.value.id)
  recordToDelete.value = null
}

const totalPages = computed(() => {
  if (props.variant !== 'full') {
    return 1
  }

  return Math.ceil(props.records.length / props.pageSize)
})

function formatDate(date) {
  return new Date(date).toLocaleDateString('es-ES')
}

const visibleRecords = computed(() => {
  if (props.variant === 'compact') {
    return [...props.records].reverse().slice(0, 5)
  }

  const start = (currentPage.value - 1) * props.pageSize
  const end = start + props.pageSize

  return props.records.slice(start, end)
})

function getGlucoseValueClass(value, momentOfDay) {
  if (momentOfDay === 'fasting') {
    if (value < 70) {
      return 'glucose-value-low'
    }

    if (value < 100) {
      return 'glucose-value-normal'
    }

    if (value <= 125) {
      return 'glucose-value-warning'
    }

    return 'glucose-value-danger'
  }

  if (value < 70) {
    return 'glucose-value-low'
  }

  if (value < 140) {
    return 'glucose-value-normal'
  }

  if (value <= 180) {
    return 'glucose-value-warning'
  }

  return 'glucose-value-danger'
}

function getGlucoseStatusText(value, momentOfDay) {
  if (momentOfDay === 'fasting') {
    if (value < 70) {
      return 'Baja'
    }

    if (value < 100) {
      return 'En rango'
    }

    if (value <= 125) {
      return 'Elevada'
    }

    return 'Alta'
  }

  if (value < 70) {
    return 'Baja'
  }

  if (value < 140) {
    return 'En rango'
  }

  if (value <= 180) {
    return 'Elevada'
  }

  return 'Alta'
}

function goToPreviousPage() {
  if (currentPage.value > 1) {
    currentPage.value--
  }
}

function goToNextPage() {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
  }
}
</script>
<template>
  <div class="glucose-table" :class="`glucose-table-${props.variant}`">
    <div class="glucose-table-row glucose-table-head">
      <span>Fecha</span>
      <span v-if="props.variant === 'full'">Hora</span>
      <span>Valor</span>
      <span>Momento</span>
      <span v-if="props.variant === 'full'">Notas</span>
      <span v-if="props.variant === 'full'">Acciones</span>
    </div>

    <div v-for="record in visibleRecords" :key="record.id" class="glucose-table-row">
      <span>{{ formatDate(record.date) }}</span>
      <span v-if="props.variant === 'full'">{{ record.time }}</span>
      <div class="glucose-value-wrapper">
        <strong :class="getGlucoseValueClass(record.glucose_value, record.moment_of_day)">
          {{ record.glucose_value }} mg/dL
        </strong>
        <small
          class="glucose-status-badge"
          :class="getGlucoseValueClass(record.glucose_value, record.moment_of_day)"
        >
          {{ getGlucoseStatusText(record.glucose_value, record.moment_of_day) }}
        </small>
      </div>
      <span>{{ momentLabels[record.moment_of_day] || 'Sin especificar' }}</span>
      <span v-if="props.variant === 'full'">{{ record.notes }}</span>

      <div v-if="props.variant === 'full'" class="glucose-table-actions">
        <button type="button" @click="emit('edit-record', record)">Editar</button>
        <button type="button" @click="askDeleteRecord(record)">Borrar</button>
      </div>
    </div>
  </div>

  <div v-if="recordToDelete" class="delete-record-modal">
    <div
      class="delete-record-box"
      role="dialog"
      aria-modal="true"
      aria-labelledby="delete-record-title"
    >
      <h3 id="delete-record-title">¿Seguro que quieres borrar este registro?</h3>

      <p>
        Esta acción eliminará la glucemia del
        <strong>{{ formatDate(recordToDelete.date) }}</strong>
        con valor
        <strong>{{ recordToDelete.glucose_value }} mg/dL</strong>.
      </p>

      <div class="delete-record-actions">
        <button type="button" @click="cancelDeleteRecord">Cancelar</button>
        <button type="button" @click="confirmDeleteRecord">Sí, borrar</button>
      </div>
    </div>
  </div>

  <div v-if="props.variant === 'full' && totalPages > 1" class="glucose-pagination">
    <button type="button" :disabled="currentPage === 1" @click="goToPreviousPage">Anterior</button>

    <span>Página {{ currentPage }} de {{ totalPages }}</span>

    <button type="button" :disabled="currentPage === totalPages" @click="goToNextPage">
      Siguiente
    </button>
  </div>
</template>
<style scoped>
.glucose-table-card {
  width: 100%;
  margin-top: 1.5rem;
  padding: 1.5rem;
  background-color: var(--color-bg);
  border: 1px solid var(--color-border);
  border-radius: 1rem;
  box-shadow: 0 10px 25px rgba(15, 23, 42, 0.08);
}

.glucose-table-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 1rem;
}

.glucose-table-header h3 {
  margin: 0;
  color: var(--color-text);
  font-size: 1.35rem;
}

.glucose-table-header a {
  color: var(--color-primary);
  font-weight: 700;
  text-decoration: none;
}

.glucose-table {
  width: 100%;
  overflow: hidden;
  border: 1px solid var(--color-border);
  border-radius: 0.8rem;
}

.glucose-table-row {
  display: grid;
  align-items: center;
  gap: 1rem;
  padding: 1rem 1.25rem;
  border-bottom: 1px solid var(--color-border);
  color: var(--color-text);
  font-size: 1rem;
}

.glucose-table-row:last-child {
  border-bottom: none;
}

.glucose-table-head {
  background-color: var(--color-surface);
  color: var(--color-text-muted);
  font-weight: 700;
}

.glucose-table-compact .glucose-table-row {
  grid-template-columns: 1fr 1fr 1.3fr;
}

.glucose-table-full .glucose-table-row {
  grid-template-columns: 1fr 0.8fr 1fr 1.4fr 2fr 1.2fr;
}

.glucose-table-row strong {
  font-size: 1.05rem;
}
.glucose-value-wrapper {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.glucose-status-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.25rem 0.65rem;
  border-radius: 999px;
  font-size: 0.75rem;
  font-weight: 800;
  line-height: 1;
  white-space: nowrap;
}
.glucose-status-badge.glucose-value-low {
  color: var(--color-danger);
  background-color: var(--dashboard-red-bg);
}

.glucose-status-badge.glucose-value-normal {
  color: var(--color-success);
  background-color: var(--dashboard-green-bg);
}

.glucose-status-badge.glucose-value-warning {
  color: var(--color-warning);
  background-color: var(--dashboard-yellow-bg);
}

.glucose-status-badge.glucose-value-danger {
  color: var(--color-danger);
  background-color: var(--dashboard-red-bg);
}

.glucose-value-low {
  color: var(--color-danger);
}

.glucose-value-normal {
  color: var(--color-success);
}

.glucose-value-warning {
  color: var(--color-warning);
}

.glucose-value-danger {
  color: var(--color-danger);
}
.glucose-table-row span {
  font-weight: 500;
}

.glucose-table-actions {
  display: flex;
  gap: 0.5rem;
}

.glucose-table-actions button {
  padding: 0.45rem 0.7rem;
  border: 1px solid var(--color-border);
  border-radius: 0.5rem;
  background-color: var(--color-bg);
  cursor: pointer;
  color: var(--color-text);
}
.glucose-pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  margin-top: 1rem;
}
.glucose-pagination span {
  color: var(--color-text-muted);
  font-weight: 700;
}
.glucose-pagination button {
  padding: 0.55rem 0.9rem;
  border: 1px solid var(--color-border);
  border-radius: 0.6rem;
  background-color: var(--color-bg);
  color: var(--color-text);
  font-weight: 700;
  cursor: pointer;
}
.glucose-pagination button:disabled {
  opacity: 0.45;
  cursor: not-allowed;
}

.delete-record-modal {
  position: fixed;
  inset: 0;
  background-color: rgba(15, 23, 42, 0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
  z-index: 1000;
}

.delete-record-box {
  width: 100%;
  max-width: 420px;
  background-color: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: 1rem;
  padding: 1.5rem;
  box-shadow: 0 20px 40px rgba(15, 23, 42, 0.25);
}

.delete-record-box h3 {
  margin: 0 0 0.75rem;
  color: var(--color-text);
}

.delete-record-box p {
  margin: 0;
  color: var(--color-text-muted);
  line-height: 1.5;
}

.delete-record-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  margin-top: 1.5rem;
}

.delete-record-actions button {
  border: none;
  border-radius: 999px;
  padding: 0.65rem 1rem;
  cursor: pointer;
  font-weight: 600;
}

.delete-record-actions button:first-child {
  background-color: var(--color-surface);
  color: var(--color-text);
  border: 1px solid var(--color-border);
}

.delete-record-actions button:last-child {
  background-color: var(--color-danger);
  color: white;
}

@media (max-width: 1025px) and (orientation: portrait) {
  .glucose-value-wrapper {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.35rem;
  }
  .glucose-table-card {
    padding: 1.25rem;
  }

  .glucose-table-compact .glucose-table-row {
    grid-template-columns: 1fr 1fr 1.2fr;
  }

  .glucose-table-full .glucose-table-row {
    grid-template-columns: 1fr 0.8fr 1fr 1.2fr 1.4fr;
  }

  .glucose-table-full .glucose-table-row span:nth-child(5),
  .glucose-table-full .glucose-table-head span:nth-child(5) {
    display: none;
  }

  .glucose-table-full .glucose-table-row {
    font-size: 0.95rem;
  }

  .glucose-table-actions button {
    min-height: 2.4rem;
    padding: 0 0.85rem;
    font-size: 0.95rem;
    font-weight: 700;
  }
  .glucose-pagination {
    font-size: 1.1rem;
  }
}

@media (max-width: 768px) {
  .glucose-table-card {
    padding: 1rem;
  }

  .glucose-table-header {
    align-items: flex-start;
    flex-direction: column;
  }

  .glucose-table {
    border: none;
    border-radius: 0;
  }

  .glucose-table-row {
    margin-bottom: 0.8rem;
    padding: 1rem;
    border: 1px solid var(--color-border);
    border-radius: 0.8rem;
    background-color: var(--color-bg);
  }

  .glucose-table-compact .glucose-table-row {
    display: grid;
    grid-template-columns: 1fr 1.4fr;
    align-items: center;
    gap: 0.35rem 1rem;
  }

  .glucose-table-compact .glucose-table-row:last-child {
    border-bottom: 1px solid var(--color-border);
  }
  .glucose-table-compact .glucose-table-row span {
    font-weight: 520;
  }
  .glucose-table-full .glucose-table-row .glucose-value-wrapper {
    width: 100%;
  }
  .glucose-table-full .glucose-value-wrapper .glucose-status-badge {
    align-self: flex-end;
  }

  .glucose-table-compact .glucose-table-head {
    display: grid;
    color: var(--color-text-muted);
    font-weight: 700;
  }

  .glucose-table-compact .glucose-table-head span:nth-child(2) {
    font-size: 0;
  }

  .glucose-table-compact .glucose-table-head span:nth-child(2)::after {
    content: 'Valor / Momento';
    font-size: 1rem;
  }

  .glucose-table-compact .glucose-table-head span:nth-child(3) {
    display: none;
  }

  .glucose-table-compact .glucose-table-row .glucose-value-wrapper {
    grid-column: 2;
  }

  .glucose-table-compact .glucose-table-row strong {
    font-size: 1.2rem;
  }

  .glucose-table-compact .glucose-table-row span:nth-child(3) {
    grid-column: 2;
  }

  .glucose-table.glucose-table-full .glucose-table-head {
    display: none !important;
  }

  .glucose-table-full .glucose-table-row {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 0.3rem;
  }

  .glucose-table-full .glucose-table-row:last-child {
    border-bottom: 1px solid var(--color-border);
  }

  .glucose-table-full .glucose-table-row strong {
    font-size: 1.2rem;
  }

  .glucose-table-actions {
    width: 100%;
    margin-top: 0.45rem;
  }

  .glucose-table-actions button {
    flex: 1;
    min-height: 2.75rem;
    padding: 0 0.95rem;
    font-size: 0.98rem;
    font-weight: 700;
  }

  .glucose-pagination {
    font-size: 1rem;
    gap: 0.75rem;
  }

  .glucose-pagination button {
    padding: 0.5rem 0.7rem;
  }
  .glucose-table-full .glucose-table-row span,
  .glucose-table-full .glucose-table-row strong {
    width: 100%;
    display: flex;
    justify-content: space-between;
    gap: 1rem;
  }
  .glucose-table-full .glucose-table-row span:nth-child(1)::before {
    content: 'Fecha:';
    font-weight: 800;
    color: var(--color-text-muted);
  }

  .glucose-table-full .glucose-table-row span:nth-child(2)::before {
    content: 'Hora:';
    font-weight: 800;
    color: var(--color-text-muted);
  }

  .glucose-table-full .glucose-table-row strong::before {
    content: 'Valor:';
    font-weight: 800;
    color: var(--color-text-muted);
  }

  .glucose-table-full .glucose-table-row span:nth-child(4)::before {
    content: 'Momento:';
    font-weight: 800;
    color: var(--color-text-muted);
  }

  .glucose-table-full .glucose-table-row span:nth-child(5)::before {
    content: 'Notas:';
    font-weight: 800;
    color: var(--color-text-muted);
  }
}
</style>

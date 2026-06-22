<script setup>
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'

import { handleAuthError } from '@/utils/handleAuthError'

import GlucoseRecordsTable from '@/components/Home/GlucoseRecordsTable.vue'
import {
  createGlucoseRecord,
  deleteGlucoseRecord,
  getGlucoseRecords,
  updateGlucoseRecord,
} from '@/services/glucoseService'
import { updateCurrentUser } from '@/services/userService'
import { useCurrentUser } from '@/composables/useCurrentUser'
import GlucoseRecordFormModal from '@/components/Home/GlucoseRecordFormModal.vue'
import GlucoseHealthSummary from '@/components/Home/GlucoseHealthSummary.vue'
import PremiumPlanForm from '@/components/Home/PremiumPlanForm.vue'

import AppPrivateStart from '@/components/layout/AppPrivateStart.vue'

const router = useRouter()

const startDate = ref('')
const endDate = ref('')
const momentOfDay = ref('')
const glucoseRecords = ref([])
const isLoadingRecords = ref(false)
const recordsError = ref('')
const hasSearchedRecords = ref(false)
const appliedStartDate = ref('')
const appliedEndDate = ref('')
const { currentUser, setCurrentUser } = useCurrentUser()
const sortOrder = ref('desc')

const isRecordModalOpen = ref(false)
const recordModalMode = ref('edit')
const selectedRecord = ref(null)
const recordFormError = ref('')
const isSubmittingRecord = ref(false)

const showPremiumModal = ref(false)
const premiumError = ref('')
const premiumSuccess = ref('')
const isUpdatingPremiumPlan = ref(false)

const sortedGlucoseRecords = computed(() => {
  return [...glucoseRecords.value].sort((a, b) => {
    const dateA = new Date(`${a.date}T${a.time}`)
    const dateB = new Date(`${b.date}T${b.time}`)

    if (sortOrder.value === 'asc') {
      return dateA - dateB
    }

    return dateB - dateA
  })
})
const highestGlucoseRecord = computed(() => {
  if (glucoseRecords.value.length === 0) {
    return null
  }

  return glucoseRecords.value.reduce((highest, record) => {
    if (record.glucose_value > highest.glucose_value) {
      return record
    }

    return highest
  })
})

const lowestGlucoseRecord = computed(() => {
  if (glucoseRecords.value.length === 0) {
    return null
  }

  return glucoseRecords.value.reduce((lowest, record) => {
    if (record.glucose_value < lowest.glucose_value) {
      return record
    }

    return lowest
  })
})

const averageGlucoseValue = computed(() => {
  if (glucoseRecords.value.length === 0) {
    return null
  }

  const total = glucoseRecords.value.reduce((sum, record) => {
    return sum + record.glucose_value
  }, 0)

  return Math.round(total / glucoseRecords.value.length)
})

const historyAccessState = computed(() => {
  if (!currentUser.value || currentUser.value.subscription_type !== 'standard') {
    return 'full'
  }

  const oldestAllowedDate = new Date()
  oldestAllowedDate.setHours(0, 0, 0, 0)
  oldestAllowedDate.setDate(oldestAllowedDate.getDate() - 30)

  if (appliedEndDate.value) {
    const selectedEndDate = new Date(`${appliedEndDate.value}T00:00:00`)

    if (selectedEndDate < oldestAllowedDate) {
      return 'blocked'
    }
  }

  if (appliedStartDate.value) {
    const selectedStartDate = new Date(`${appliedStartDate.value}T00:00:00`)

    if (selectedStartDate < oldestAllowedDate) {
      return 'partial'
    }
  }

  return 'full'
})

const premiumWarningContent = computed(() => {
  if (!hasSearchedRecords.value || historyAccessState.value === 'full') {
    return null
  }

  if (historyAccessState.value === 'blocked') {
    return {
      title: 'Periodo fuera del historial disponible',
      message:
        'El intervalo seleccionado queda fuera de los últimos 30 días incluidos en tu plan Standard. Ajusta las fechas o hazte Premium para consultar periodos anteriores.',
    }
  }

  return {
    title: 'Información parcial del periodo seleccionado',
    message:
      'El intervalo solicitado supera los 30 días disponibles en tu cuenta Standard. Los resultados mostrados corresponden únicamente al tramo del periodo incluido en tu plan.',
  }
})

async function handleSearch() {
  isLoadingRecords.value = true
  recordsError.value = ''
  hasSearchedRecords.value = true
  appliedStartDate.value = startDate.value
  appliedEndDate.value = endDate.value

  try {
    const records = await getGlucoseRecords(startDate.value, endDate.value, momentOfDay.value)

    glucoseRecords.value = records
  } catch (error) {
    if (handleAuthError(error, router)) {
      recordsError.value = 'Tu sesión ha caducado. Te redirigimos al inicio de sesión.'
      return
    }

    recordsError.value = error.message || 'No se pudieron cargar las glucemias. Inténtalo de nuevo.'
  } finally {
    isLoadingRecords.value = false
  }
}
async function handleDeleteRecord(recordId) {
  recordsError.value = ''

  try {
    await deleteGlucoseRecord(recordId)

    glucoseRecords.value = glucoseRecords.value.filter((record) => record.id !== recordId)
  } catch (error) {
    if (handleAuthError(error, router)) {
      recordsError.value = 'Tu sesión ha caducado. Te redirigimos al inicio de sesión.'
      return
    }

    recordsError.value = error.message || 'No se pudo borrar la glucemia. Inténtalo de nuevo.'
  }
}
function handleClearSearch() {
  startDate.value = ''
  endDate.value = ''
  momentOfDay.value = ''
}
function formatDate(date) {
  return date.toISOString().split('T')[0]
}

function handlePopularSearch(days) {
  const today = new Date()
  const start = new Date()

  start.setDate(today.getDate() - days)

  startDate.value = formatDate(start)
  endDate.value = formatDate(today)
  momentOfDay.value = ''

  handleSearch()
}

function handleSingleDaySearch(daysAgo) {
  const selectedDate = new Date()

  selectedDate.setDate(selectedDate.getDate() - daysAgo)

  startDate.value = formatDate(selectedDate)
  endDate.value = formatDate(selectedDate)
  momentOfDay.value = ''

  handleSearch()
}
function openCreateRecordModal() {
  selectedRecord.value = null
  recordModalMode.value = 'create'
  recordFormError.value = ''
  isRecordModalOpen.value = true
}

function openEditRecordModal(record) {
  selectedRecord.value = record
  recordModalMode.value = 'edit'
  recordFormError.value = ''
  isRecordModalOpen.value = true
}

function closeRecordModal() {
  isRecordModalOpen.value = false
  selectedRecord.value = null
  recordFormError.value = ''
  isSubmittingRecord.value = false
}
async function handleSubmitRecord(recordData) {
  isSubmittingRecord.value = true
  recordFormError.value = ''

  try {
    if (recordModalMode.value === 'edit') {
      if (!selectedRecord.value) {
        recordFormError.value = 'No se ha encontrado el registro que quieres editar.'
        return
      }

      const updatedRecord = await updateGlucoseRecord(selectedRecord.value.id, recordData)

      glucoseRecords.value = glucoseRecords.value.map((record) => {
        if (record.id === updatedRecord.id) {
          return updatedRecord
        }

        return record
      })

      closeRecordModal()
      return
    }

    const createdRecord = await createGlucoseRecord(recordData)

    glucoseRecords.value = [...glucoseRecords.value, createdRecord]

    closeRecordModal()
  } catch (error) {
    if (handleAuthError(error, router)) {
      recordFormError.value = 'Tu sesión ha caducado. Te redirigimos al inicio de sesión.'
      return
    }

    recordFormError.value = error.message || 'No se pudo guardar la glucemia. Revisa los datos.'
  } finally {
    isSubmittingRecord.value = false
  }
}
function openPremiumModal() {
  premiumError.value = ''
  premiumSuccess.value = ''
  showPremiumModal.value = true
}

function closePremiumModal() {
  if (isUpdatingPremiumPlan.value) return

  showPremiumModal.value = false
  premiumError.value = ''
  premiumSuccess.value = ''
}
async function handlePremiumPlanChange(newPlan) {
  if (!currentUser.value) return

  isUpdatingPremiumPlan.value = true
  premiumError.value = ''
  premiumSuccess.value = ''

  try {
    const updatedUser = await updateCurrentUser({
      name: currentUser.value.name,
      surname: currentUser.value.surname,
      date_of_birth: currentUser.value.date_of_birth,
      subscription_type: newPlan,
    })

    setCurrentUser(updatedUser)
    premiumSuccess.value = `Plan actualizado a ${newPlan === 'premium' ? 'Premium' : 'Standard'} correctamente.`

    await handleSearch()

    setTimeout(() => {
      showPremiumModal.value = false
      premiumSuccess.value = ''
    }, 1500)
  } catch (error) {
    if (handleAuthError(error, router)) {
      premiumError.value = 'Tu sesión ha caducado. Te redirigimos al inicio de sesión.'
      return
    }

    premiumError.value = error.message || 'No se pudo actualizar el plan de cuenta.'
  } finally {
    isUpdatingPremiumPlan.value = false
  }
}
</script>

<template>
  <AppPrivateStart
    title="consulta, filtra y gestiona tus registros de glucemias"
    main="Mis glucemias"
    variant="active"
    @add-glucose="openCreateRecordModal"
  />

  <section class="glucemias-search">
    <div class="search-group">
      <label for="start-date">Fecha desde</label>

      <div class="search-control">
        <input id="start-date" v-model="startDate" type="date" />
      </div>
    </div>

    <div class="search-group">
      <label for="end-date">Fecha hasta</label>

      <div class="search-control">
        <input id="end-date" v-model="endDate" type="date" />
      </div>
    </div>

    <div class="search-group">
      <label for="moment-of-day">Momento del día</label>

      <div class="search-control">
        <select id="moment-of-day" v-model="momentOfDay">
          <option value="">Todos</option>
          <option value="fasting">Ayunas</option>
          <option value="before_meal">Antes de comer</option>
          <option value="after_meal">Después de comer</option>
          <option value="night">Noche</option>
          <option value="other">Otro</option>
        </select>
      </div>
    </div>

    <div class="search-actions">
      <button type="button" class="clear-search-button" @click="handleClearSearch">Limpiar</button>

      <button type="button" class="search-button" @click="handleSearch">Buscar</button>
    </div>
  </section>
  <section class="popular-searches">
    <span class="popular-searches-label">Búsquedas populares:</span>

    <div class="popular-searches-actions">
      <button type="button" @click="handleSingleDaySearch(0)">Hoy</button>

      <button type="button" @click="handleSingleDaySearch(1)">Ayer</button>

      <button type="button" @click="handlePopularSearch(7)">Últimos 7 días</button>

      <button type="button" @click="handlePopularSearch(30)">Últimos 30 días</button>

      <button type="button" @click="handlePopularSearch(90)">Últimos 90 días</button>
    </div>
  </section>
  <section class="glucose-records-panel" :aria-busy="isLoadingRecords">
    <div
      v-if="premiumWarningContent && !isLoadingRecords && !recordsError"
      class="premium-records-warning"
    >
      <div>
        <h3>{{ premiumWarningContent.title }}</h3>
        <p>{{ premiumWarningContent.message }}</p>
      </div>

      <button type="button" class="premium-records-button" @click="openPremiumModal">
        Hazte premium
      </button>
    </div>

    <div class="records-panel-header">
      <div class="records-panel-title">
        <h2>Listado de glucemias</h2>
        <span v-if="hasSearchedRecords">{{ glucoseRecords.length }} registros</span>
        <span v-else>Sin búsqueda</span>
      </div>

      <div class="records-panel-order">
        <label for="sort-order">Ordenar por fecha</label>

        <select id="sort-order" v-model="sortOrder">
          <option value="desc">Más recientes primero</option>
          <option value="asc">Más antiguos primero</option>
        </select>
      </div>
    </div>

    <div v-if="isLoadingRecords" class="records-state" role="status" aria-live="polite">
      Cargando glucemias...
    </div>

    <div v-else-if="recordsError" class="records-state records-state-error" role="alert">
      {{ recordsError }}
    </div>

    <div v-else-if="!hasSearchedRecords" class="records-state">
      Selecciona un periodo o utiliza una búsqueda rápida para consultar tus glucemias.
    </div>

    <div v-else-if="glucoseRecords.length === 0" class="records-state">
      <template v-if="historyAccessState === 'blocked'">
        No se pueden consultar registros de este periodo con tu plan Standard.
      </template>
      <template v-else>No hay glucemias para los filtros seleccionados.</template>
    </div>

    <GlucoseRecordsTable
      v-else
      :records="sortedGlucoseRecords"
      variant="full"
      @delete-record="handleDeleteRecord"
      @edit-record="openEditRecordModal"
    />
    <GlucoseHealthSummary
      v-if="hasSearchedRecords && !isLoadingRecords && !recordsError"
      class="glucose-summary-space"
      title="Resumen del periodo seleccionado"
      variant="wide"
      :highest-record="highestGlucoseRecord"
      :lowest-record="lowestGlucoseRecord"
      :average-value="averageGlucoseValue"
    />
  </section>
  <GlucoseRecordFormModal
    v-if="isRecordModalOpen"
    :mode="recordModalMode"
    :initial-record="selectedRecord"
    :error-message="recordFormError"
    :is-submitting="isSubmittingRecord"
    @submit="handleSubmitRecord"
    @cancel="closeRecordModal"
  />
  <PremiumPlanForm
    v-if="showPremiumModal"
    :current-user="currentUser"
    :is-submitting="isUpdatingPremiumPlan"
    :error-message="premiumError"
    :success-message="premiumSuccess"
    @cancel="closePremiumModal"
    @confirm-plan-change="handlePremiumPlanChange"
  />
</template>
<style scoped>
.glucemias-search {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr auto;
  gap: 1rem;
  align-items: end;

  padding: 1.5rem;

  background-color: var(--color-bg);
  border: 1px solid var(--color-border);
  border-radius: 18px;
  box-shadow: 0 12px 30px rgba(15, 23, 42, 0.08);
}

.search-group {
  display: flex;
  flex-direction: column;
  gap: 0.65rem;
}

.search-group label {
  font-size: 0.9rem;
  font-weight: 700;
  color: var(--color-text);
}

.search-control {
  display: flex;
  align-items: center;

  min-height: 48px;
  padding: 0 0.9rem;

  background-color: var(--color-bg);
  border: 1px solid var(--color-border);
  border-radius: 10px;
}

.search-control input,
.search-control select {
  width: 100%;

  border: none;
  outline: none;
  background: transparent;

  font: inherit;
  color: var(--color-text);
}

.search-control select {
  cursor: pointer;
}

.private-layout.dark-mode .search-control input[type='date']::-webkit-calendar-picker-indicator {
  filter: invert(1);
}

.search-actions {
  display: flex;
  gap: 0.8rem;
}

.clear-search-button,
.search-button {
  min-height: 48px;
  padding: 0 1.2rem;

  border-radius: 10px;
  font-weight: 700;
  cursor: pointer;
}

.clear-search-button {
  background-color: var(--color-bg);
  color: var(--color-text);
  border: 1px solid var(--color-border);
}

.search-button {
  background-color: var(--color-primary);
  color: var(--color-bg);
  border: 1px solid var(--color-primary);
}

.clear-search-button:hover {
  background-color: var(--color-surface);
}

.search-button:hover {
  filter: brightness(0.95);
}
.popular-searches {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;

  padding: 0 0.25rem;
  margin: 1.25rem 0.25rem;
}

.popular-searches-label {
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--color-text-muted);
}

.popular-searches-actions {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.popular-searches-actions button {
  padding: 0.55rem 0.95rem;

  background-color: transparent;
  color: var(--color-primary);

  border: 1px solid var(--color-border);
  border-radius: 999px;

  font: inherit;
  font-size: 0.9rem;
  font-weight: 700;

  cursor: pointer;
}

.popular-searches-actions button:hover {
  background-color: var(--color-bg);
  border-color: var(--color-primary);
}
.glucose-records-panel {
  gap: 1.5rem;
  padding: 1.5rem;

  background-color: var(--color-bg);
  border: 1px solid var(--color-border);
  border-radius: 18px;
  box-shadow: 0 12px 30px rgba(15, 23, 42, 0.08);
}

.records-panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;

  margin-bottom: 1.25rem;
}

.records-panel-title {
  display: flex;
  align-items: center;
  gap: 0.8rem;
}

.records-panel-title h2 {
  margin: 0;

  color: var(--color-text);
  font-size: 1.35rem;
  font-weight: 800;
}

.records-panel-title span {
  padding: 0.35rem 0.65rem;

  background-color: var(--color-bg);
  color: var(--color-text-muted);

  border-radius: 999px;

  font-size: 0.85rem;
  font-weight: 700;
}

.records-panel-order {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.records-panel-order label {
  color: var(--color-text-muted);
  font-size: 0.9rem;
  font-weight: 700;
}

.records-panel-order select {
  min-height: 42px;
  padding: 0 0.9rem;

  background-color: var(--color-surface);
  color: var(--color-text);

  border: 1px solid var(--color-border);
  border-radius: 10px;

  font: inherit;
  font-weight: 700;

  cursor: pointer;
}

.glucose-summary-space {
  margin-top: 2rem;
}
.records-state {
  padding: 2rem;

  text-align: center;
  color: var(--color-text-muted);
  font-weight: 700;

  background-color: var(--color-surface);
  border: 1px dashed var(--color-border);
  border-radius: 14px;

  margin-bottom: 1.5rem;
}
.premium-records-warning {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;

  margin-bottom: 1.25rem;
  padding: 1.25rem;

  background-color: var(--dashboard-yellow-bg);
  border: 1px solid var(--color-warning);
  border-radius: 14px;
}

.premium-records-warning h3 {
  margin: 0 0 0.4rem;

  color: var(--color-text);
  font-size: 1rem;
  font-weight: 800;
}

.premium-records-warning p {
  margin: 0;

  color: var(--color-text);
  font-size: 0.95rem;
  line-height: 1.5;
}

.premium-records-button {
  flex-shrink: 0;

  min-height: 42px;
  padding: 0 1rem;

  background-color: var(--color-primary);
  color: var(--color-bg);

  border: 1px solid var(--color-primary);
  border-radius: 10px;

  font: inherit;
  font-weight: 800;
  cursor: pointer;
}

.premium-records-button:hover {
  filter: brightness(0.95);
}
.records-state-error {
  color: var(--color-danger);
  border-color: var(--color-danger);
}
@media (max-width: 1025px) and (orientation: portrait) {
  .glucemias-search {
    grid-template-columns: 1fr 1fr;
  }

  .search-actions {
    grid-column: 1 / -1;
    justify-content: flex-end;
  }
  .records-panel-header {
    flex-wrap: wrap;
    align-items: flex-start;
  }

  .premium-records-warning {
    width: 100%;
    box-sizing: border-box;
  }
}

@media (max-width: 769px) {
  .popular-searches {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.7rem;
    margin: 0.9rem 0.15rem 0.75rem;
  }

  .popular-searches-actions {
    width: 100%;
    gap: 0.6rem;
    row-gap: 0.5rem;
  }

  .popular-searches-actions button {
    flex: 1;
    padding: 0.5rem 0.85rem;
  }
  .glucemias-search {
    grid-template-columns: 1fr;
    padding: 1rem;
  }

  .search-actions {
    grid-column: auto;
    flex-direction: column;
  }

  .clear-search-button,
  .search-button {
    width: 100%;
  }
  .glucose-records-panel {
    padding: 1rem;
  }

  .records-panel-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .records-panel-title {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }

  .records-panel-title h2 {
    font-size: 1.2rem;
  }

  .records-panel-order {
    width: 100%;
    flex-direction: column;
    align-items: flex-start;
  }

  .records-panel-order select {
    width: 100%;
  }
  .premium-records-warning {
    flex-direction: column;
    align-items: flex-start;
  }

  .premium-records-button {
    width: 100%;
  }
}

@media (max-width: 950px) and (max-height: 520px) and (orientation: landscape) {
  .records-panel-header {
    flex-wrap: wrap;
    align-items: center;
  }

  .premium-records-warning {
    width: 100%;
    box-sizing: border-box;
    margin-bottom: 1rem;
    padding: 0.9rem 1rem;
    gap: 1rem;
  }

  .premium-records-warning h3 {
    margin-bottom: 0.25rem;
    font-size: 0.95rem;
    line-height: 1.15;
  }

  .premium-records-warning p {
    font-size: 0.85rem;
    line-height: 1.3;
  }

  .premium-records-button {
    min-height: 2.5rem;
    padding: 0 0.9rem;
    white-space: nowrap;
  }
}
</style>

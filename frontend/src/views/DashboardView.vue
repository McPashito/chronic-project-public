<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

import { createGlucoseRecord, getSummary, getGlucoseRecords } from '@/services/glucoseService'
import { handleAuthError } from '@/utils/handleAuthError'

import DashCard from '@/components/Home/DashCard.vue'
import DropIcon from '@/components/Icons/DropIcon.vue'
import AverageIcon from '@/components/Icons/AverageIcon.vue'
import EyeUpIcon from '@/components/Icons/EyeUpIcon.vue'
import EyeDownIcon from '@/components/Icons/EyeDownIcon.vue'
import AppPrivateStart from '@/components/layout/AppPrivateStart.vue'
import GlucoseRecordsTable from '@/components/Home/GlucoseRecordsTable.vue'
import GlucoseRecordFormModal from '@/components/Home/GlucoseRecordFormModal.vue'
const router = useRouter()

const today = new Date()

const endDate = new Date(today)
endDate.setDate(endDate.getDate() - 1)
const endDateFormated = endDate.toISOString().split('T')[0]

const startDate = new Date(today)
startDate.setDate(startDate.getDate() - 8)
const startDateFormated = startDate.toISOString().split('T')[0]

const currentSummary = ref(null)
const isLoadingSummary = ref(true)
const summaryError = ref('')

const glucoseRecords = ref([])
const isLoadingRecentRecords = ref(true)
const recentRecordsError = ref('')

const isRecordModalOpen = ref(false)
const recordModalMode = ref('create')
const selectedRecord = ref(null)
const recordFormError = ref('')
const isSubmittingRecord = ref(false)

async function loadSummary() {
  isLoadingSummary.value = true
  summaryError.value = ''

  try {
    currentSummary.value = await getSummary(startDateFormated, endDateFormated)
  } catch (error) {
    if (handleAuthError(error, router)) {
      summaryError.value = 'Tu sesión ha caducado. Te redirigimos al inicio de sesión.'
      return
    }

    summaryError.value = error.message || 'No se pudo cargar el resumen.'
  } finally {
    isLoadingSummary.value = false
  }
}

async function loadGlucoseRecords() {
  isLoadingRecentRecords.value = true
  recentRecordsError.value = ''

  try {
    const recordsData = await getGlucoseRecords(startDateFormated, endDateFormated)

    glucoseRecords.value = recordsData
  } catch (error) {
    if (handleAuthError(error, router)) {
      recentRecordsError.value = 'Tu sesión ha caducado. Te redirigimos al inicio de sesión.'
      return
    }

    recentRecordsError.value = error.message || 'No se pudieron cargar los registros recientes.'
  } finally {
    isLoadingRecentRecords.value = false
  }
}

function openCreateRecordModal() {
  selectedRecord.value = null
  recordModalMode.value = 'create'
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
    const createdRecord = await createGlucoseRecord(recordData)

    glucoseRecords.value = [...glucoseRecords.value, createdRecord]

    await loadSummary()

    closeRecordModal()
  } catch (error) {
    if (handleAuthError(error, router)) {
      recordFormError.value = 'Tu sesión ha caducado. Te redirigimos al inicio de sesión.'
      return
    }

    recordFormError.value = error.message || 'No se pudo crear la glucemia. Revisa los datos.'
  } finally {
    isSubmittingRecord.value = false
  }
}

onMounted(() => {
  loadSummary()
  loadGlucoseRecords()
})

function formatGlucoseDateTime(date, time) {
  if (!date || !time) return ''

  const dateParts = String(date).split('-')

  if (dateParts.length !== 3) return `${date} · ${time}`

  const [year, month, day] = dateParts
  const shortTime = String(time).slice(0, 5)

  return `${day}/${month}/${year} · ${shortTime}`
}
</script>
<template>
  <section class="dash">
    <section class="dash-flex">
      <AppPrivateStart
        title="aquí tienes el resumen de tus últimos 7 días"
        main="Bienvenido!"
        variant="active"
        @add-glucose="openCreateRecordModal"
      />

      <div class="dash-card-grid" :aria-busy="isLoadingSummary">
        <div v-if="isLoadingSummary" class="dash-state" role="status" aria-live="polite">
          Cargando resumen...
        </div>

        <div v-else-if="summaryError" class="dash-state dash-state-error" role="alert">
          {{ summaryError }}
        </div>

        <div v-else-if="currentSummary?.total_records === 0" class="dash-state" role="status">
          No hay glucemias en los últimos 7 días.
        </div>

        <DashCard
          v-if="!isLoadingSummary && !summaryError && currentSummary?.last_glucemia"
          title="Tu última glucemia"
          :icon="DropIcon"
          :value="currentSummary.last_glucemia.glucose_value"
          unit="mg/dL"
          :meta="
            formatGlucoseDateTime(
              currentSummary.last_glucemia.date,
              currentSummary.last_glucemia.time,
            )
          "
          :glucose-value="currentSummary.last_glucemia.glucose_value"
          :moment-of-day="currentSummary.last_glucemia.moment_of_day"
        />

        <DashCard
          v-if="!isLoadingSummary && !summaryError && currentSummary?.min_glucemia"
          title="Glucemia mínima"
          :icon="EyeDownIcon"
          :value="currentSummary.min_glucemia.glucose_value"
          unit="mg/dL"
          :meta="
            formatGlucoseDateTime(
              currentSummary.min_glucemia.date,
              currentSummary.min_glucemia.time,
            )
          "
          :glucose-value="currentSummary.min_glucemia.glucose_value"
          :moment-of-day="currentSummary.min_glucemia.moment_of_day"
        />

        <DashCard
          v-if="!isLoadingSummary && !summaryError && currentSummary?.max_glucemia"
          title="Glucemia máxima"
          :icon="EyeUpIcon"
          :value="currentSummary.max_glucemia.glucose_value"
          unit="mg/dL"
          :meta="
            formatGlucoseDateTime(
              currentSummary.max_glucemia.date,
              currentSummary.max_glucemia.time,
            )
          "
          :glucose-value="currentSummary.max_glucemia.glucose_value"
          :moment-of-day="currentSummary.max_glucemia.moment_of_day"
        />

        <DashCard
          v-if="
            !isLoadingSummary &&
            !summaryError &&
            currentSummary &&
            currentSummary.average_glucemia !== null
          "
          title="Glucemia media"
          :icon="AverageIcon"
          variant="blue"
          :value="currentSummary.average_glucemia"
          unit="mg/dL"
          meta="Media últimos 7 días"
        />
      </div>
      <section class="dash-records-panel" :aria-busy="isLoadingRecentRecords">
        <div class="dash-records-header">
          <div>
            <span class="dash-records-kicker">Últimos registros</span>
            <h2>Glucemias recientes</h2>
          </div>

          <RouterLink to="/glucemias" class="dash-records-link"> Panel de glucemias </RouterLink>
        </div>

        <div
          v-if="isLoadingRecentRecords"
          class="dash-records-table dash-state"
          role="status"
          aria-live="polite"
        >
          Cargando registros recientes...
        </div>

        <div
          v-else-if="recentRecordsError"
          class="dash-records-table dash-state dash-state-error"
          role="alert"
        >
          {{ recentRecordsError }}
        </div>

        <div v-else-if="glucoseRecords.length === 0" class="dash-records-table dash-state">
          No hay registros recientes.
        </div>

        <div v-else class="dash-records-table">
          <GlucoseRecordsTable variant="compact" :records="glucoseRecords" />
        </div>
      </section>
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
  </section>
</template>
<style scoped>
.dash-card-grid {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr 1fr;
  justify-content: flex-start;
  gap: 1rem;
}
.dash-state {
  grid-column: 1 / -1;
  padding: 2rem;
  color: var(--color-text-muted);
  text-align: center;
}
.dash-state-error {
  color: var(--color-danger);
}
.dash-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}
.dash-records-table {
  padding: 1.5rem;
}
.dash-records-panel {
  margin-top: 1.5rem;
  background-color: var(--color-bg);
  border: 1px solid var(--color-border);
  border-radius: 1rem;
  box-shadow: 0 12px 30px rgba(15, 23, 42, 0.08);
  overflow: hidden;
}

.dash-records-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid var(--color-border);
}

.dash-records-kicker {
  display: block;
  margin-bottom: 0.25rem;
  color: var(--color-primary);
  font-size: 0.8rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.dash-records-header h2 {
  margin: 0;
  color: var(--color-text);
  font-size: 1.25rem;
}

.dash-records-link {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 44px;
  padding: 0 1rem;
  box-sizing: border-box;
  border: 1px solid var(--color-primary);
  border-radius: 0.5rem;
  background-color: var(--color-primary);
  color: var(--color-bg);
  font-size: 0.95rem;
  font-weight: 700;
  text-decoration: none;
  white-space: nowrap;
}

.dash-records-link:hover {
  background-color: var(--color-bg);
  color: var(--color-primary);
}
.dash-records-link:focus-visible {
  outline: 3px solid var(--color-primary-muted);
  outline-offset: 2px;
}
@media (max-width: 1025px) and (orientation: portrait) {
  .dash-card-grid {
    grid-template-columns: 1fr;
  }
  .dash-records-panel {
    margin-top: 1rem;
    border-radius: 0.85rem;
  }

  .dash-records-header h2 {
    font-size: 1.1rem;
  }

  .dash-records-kicker {
    font-size: 0.72rem;
  }
}
@media (max-width: 768px) {
  .dash-records-header {
    align-items: flex-start;
    flex-direction: column;
    padding: 1rem;
  }

  .dash-records-link {
    width: 100%;
  }
}

@media (max-width: 950px) and (max-height: 520px) and (orientation: landscape) {
  .dash-card-grid {
    grid-template-columns: repeat(4, minmax(180px, 1fr));
    gap: 0.75rem;
    margin-top: 0;
    overflow-x: auto;
    padding-bottom: 0;
    scroll-snap-type: x proximity;
  }

  .dash-card-grid > * {
    scroll-snap-align: start;
  }

  .dash-records-panel {
    margin-top: 1rem;
  }
}
</style>

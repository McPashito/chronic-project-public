<script setup>
import { computed } from 'vue'

import DropIcon from '@/components/Icons/DropIcon.vue'
import EyeDownIcon from '@/components/Icons/EyeDownIcon.vue'
import AverageIcon from '@/components/Icons/AverageIcon.vue'

const props = defineProps({
  title: {
    type: String,
    default: 'Resumen del periodo seleccionado',
  },
  variant: {
    type: String,
    default: 'wide',
    validator(value) {
      return ['wide', 'compact'].includes(value)
    },
  },
  highestRecord: {
    type: Object,
    default: null,
  },
  lowestRecord: {
    type: Object,
    default: null,
  },
  averageValue: {
    type: Number,
    default: null,
  },
})

const momentLabels = {
  fasting: 'Ayunas',
  before_meal: 'Antes de comer',
  after_meal: 'Después de comer',
  night: 'Noche',
  other: 'Otro momento',
}

function getMomentLabel(momentOfDay) {
  return momentLabels[momentOfDay] || 'Momento no indicado'
}

function getResolvedBadge(glucoseValue, momentOfDay) {
  if (glucoseValue === null || glucoseValue === undefined) {
    return ''
  }

  if (glucoseValue < 70) {
    return 'Baja'
  }

  if (momentOfDay === 'fasting') {
    if (glucoseValue <= 99) return 'En rango'
    if (glucoseValue <= 125) return 'Revisar'
    return 'Alta'
  }

  if (momentOfDay === 'after_meal') {
    if (glucoseValue < 140) return 'En rango'
    if (glucoseValue <= 180) return 'Revisar'
    return 'Alta'
  }

  if (glucoseValue <= 180) {
    return 'En rango'
  }

  return 'Alta'
}

function getResolvedVariant(glucoseValue, momentOfDay) {
  if (glucoseValue === null || glucoseValue === undefined) {
    return 'blue'
  }

  if (glucoseValue < 70) {
    return 'yellow'
  }

  if (momentOfDay === 'fasting') {
    if (glucoseValue <= 99) return 'green'
    if (glucoseValue <= 125) return 'yellow'
    return 'red'
  }

  if (momentOfDay === 'after_meal') {
    if (glucoseValue < 140) return 'green'
    if (glucoseValue <= 180) return 'yellow'
    return 'red'
  }

  if (glucoseValue <= 180) {
    return 'green'
  }

  return 'red'
}

const summaryItems = computed(() => [
  {
    key: 'highest',
    title: 'Glucemia más alta',
    icon: DropIcon,
    value: props.highestRecord?.glucose_value ?? null,
    unit: 'mg/dL',
    meta: props.highestRecord ? getMomentLabel(props.highestRecord.moment_of_day) : 'Sin registros',
    badge: props.highestRecord
      ? getResolvedBadge(props.highestRecord.glucose_value, props.highestRecord.moment_of_day)
      : '',
    variant: props.highestRecord
      ? getResolvedVariant(props.highestRecord.glucose_value, props.highestRecord.moment_of_day)
      : 'blue',
  },
  {
    key: 'lowest',
    title: 'Glucemia más baja',
    icon: EyeDownIcon,
    value: props.lowestRecord?.glucose_value ?? null,
    unit: 'mg/dL',
    meta: props.lowestRecord ? getMomentLabel(props.lowestRecord.moment_of_day) : 'Sin registros',
    badge: props.lowestRecord
      ? getResolvedBadge(props.lowestRecord.glucose_value, props.lowestRecord.moment_of_day)
      : '',
    variant: props.lowestRecord
      ? getResolvedVariant(props.lowestRecord.glucose_value, props.lowestRecord.moment_of_day)
      : 'blue',
  },
  {
    key: 'average',
    title: 'Media del periodo',
    icon: AverageIcon,
    value: props.averageValue,
    unit: 'mg/dL',
    meta: 'Promedio',
    badge:
      props.averageValue !== null && props.averageValue !== undefined
        ? getResolvedBadge(props.averageValue, '')
        : '',
    variant:
      props.averageValue !== null && props.averageValue !== undefined
        ? getResolvedVariant(props.averageValue, '')
        : 'blue',
  },
])
</script>

<template>
  <section class="glucose-health-summary" :class="`summary-${variant}`">
    <header class="summary-header">
      <div class="summary-header-icon">
        <svg viewBox="0 0 24 24" aria-hidden="true">
          <path
            d="M12 20.2s-6.7-4.2-9.1-8.4C1.1 8.6 2.8 5 6.3 5c2 0 3.4 1.1 4.2 2.3C11.3 6.1 12.7 5 14.7 5c3.5 0 5.2 3.6 3.4 6.8C15.7 16 12 20.2 12 20.2Z"
            fill="none"
            stroke="currentColor"
            stroke-width="1.8"
            stroke-linejoin="round"
          />
          <path
            d="M5.5 12h3l1.3-2.4 2.1 4.5 1.4-2.1h5.2"
            fill="none"
            stroke="currentColor"
            stroke-width="1.8"
            stroke-linecap="round"
            stroke-linejoin="round"
          />
        </svg>
      </div>

      <h2>{{ title }}</h2>
    </header>

    <div class="summary-list">
      <article v-for="item in summaryItems" :key="item.key" class="summary-row">
        <div class="summary-icon" :class="`variant-${item.variant}`">
          <component :is="item.icon" />
        </div>

        <div class="summary-content">
          <p class="summary-label">{{ item.title }}</p>

          <div v-if="item.value !== null && item.value !== undefined" class="summary-value-line">
            <strong>{{ item.value }}</strong>
            <span>{{ item.unit }}</span>
          </div>

          <p v-else class="summary-empty">Sin datos</p>

          <p class="summary-meta">{{ item.meta }}</p>
        </div>

        <strong v-if="item.badge" class="summary-badge" :class="`badge-${item.variant}`">
          {{ item.badge }}
        </strong>
      </article>
    </div>
  </section>
</template>

<style scoped>
.glucose-health-summary {
  width: 100%;
  padding: 1.25rem;

  background-color: var(--color-bg);
  border: 1.5px solid var(--color-border);
  border-radius: 1rem;
}

.summary-header {
  display: flex;
  align-items: center;
  gap: 0.9rem;

  padding-bottom: 1rem;
  margin-bottom: 0.25rem;

  border-bottom: 1px solid var(--color-border);
}

.summary-header-icon {
  width: 44px;
  height: 44px;

  display: flex;
  align-items: center;
  justify-content: center;

  color: var(--dashboard-blue-icon);
  background-color: var(--dashboard-blue-bg);
  border-radius: 50%;
  flex-shrink: 0;
}

.summary-header-icon svg {
  width: 27px;
  height: 27px;
}

.summary-header h2 {
  margin: 0;

  font-size: 1.25rem;
  font-weight: 800;
  color: var(--color-text);
}

.summary-list {
  display: grid;
}

.summary-wide .summary-list {
  grid-template-columns: repeat(3, 1fr);
}

.summary-compact .summary-list {
  grid-template-columns: 1fr;
}

.summary-row {
  display: grid;
  grid-template-columns: auto 1fr auto;
  align-items: center;
  gap: 1rem;

  padding: 1.25rem 1rem;
}

.summary-wide .summary-row + .summary-row {
  border-left: 1px solid var(--color-border);
}

.summary-compact .summary-row + .summary-row {
  border-top: 1px solid var(--color-border);
}

.summary-icon {
  width: 54px;
  height: 54px;

  display: flex;
  align-items: center;
  justify-content: center;

  border-radius: 50%;
  flex-shrink: 0;
}

.summary-icon svg {
  width: 27px;
  height: 27px;
}

.summary-icon.variant-blue {
  background-color: var(--dashboard-blue-bg);
  color: var(--dashboard-blue-icon);
}

.summary-icon.variant-red {
  background-color: var(--dashboard-red-bg);
  color: var(--dashboard-red-icon);
}

.summary-icon.variant-green {
  background-color: var(--dashboard-green-bg);
  color: var(--dashboard-green-icon);
}

.summary-icon.variant-yellow {
  background-color: var(--dashboard-yellow-bg);
  color: var(--dashboard-yellow-icon);
}

.summary-content {
  min-width: 0;
}

.summary-label {
  margin: 0 0 0.25rem;

  font-size: 0.95rem;
  font-weight: 600;
  color: var(--color-text-muted);
}

.summary-value-line {
  display: flex;
  align-items: baseline;
  gap: 0.35rem;
}

.summary-value-line strong {
  font-size: 1.8rem;
  line-height: 1;
  font-weight: 800;
  color: var(--color-text);
}

.summary-value-line span {
  font-size: 0.9rem;
  font-weight: 700;
  color: var(--color-text);
}

.summary-meta,
.summary-empty {
  margin: 0.35rem 0 0;

  font-size: 0.9rem;
  color: var(--color-text-muted);
}

.summary-badge {
  width: fit-content;
  padding: 0.35rem 0.75rem;

  border-radius: 999px;

  font-size: 0.85rem;
  font-weight: 700;
  white-space: nowrap;
}

.summary-badge.badge-blue {
  background-color: var(--dashboard-blue-bg);
  color: var(--dashboard-blue-icon);
}

.summary-badge.badge-red {
  background-color: var(--dashboard-red-bg);
  color: var(--dashboard-red-icon);
}

.summary-badge.badge-green {
  background-color: var(--dashboard-green-bg);
  color: var(--dashboard-green-icon);
}

.summary-badge.badge-yellow {
  background-color: var(--dashboard-yellow-bg);
  color: var(--dashboard-yellow-icon);
}

@media (max-width: 1025px) and (orientation: portrait) {
  .summary-row {
    grid-template-columns: auto max-content auto;
    justify-content: center;
    column-gap: 1rem;
  }

  .summary-wide .summary-list {
    grid-template-columns: 1fr;
  }

  .summary-wide .summary-row + .summary-row {
    border-left: 0;
    border-top: 1px solid var(--color-border);
  }

  .summary-header h2 {
    font-size: 1.45rem;
  }

  .summary-label {
    font-size: 1.1rem;
  }

  .summary-content {
    min-width: 220px;
  }

  .summary-value-line strong {
    font-size: 2rem;
  }

  .summary-value-line span,
  .summary-meta,
  .summary-empty {
    font-size: 1rem;
  }
}

@media (max-width: 600px) and (orientation: portrait) {
  .glucose-health-summary {
    padding: 1rem;
  }

  .summary-header {
    gap: 0.75rem;
  }

  .summary-header-icon {
    width: 40px;
    height: 40px;
  }

  .summary-header-icon svg {
    width: 24px;
    height: 24px;
  }

  .summary-header h2 {
    font-size: 1.1rem;
  }

  .summary-row {
    grid-template-columns: auto 1fr;
    padding: 1rem 0.25rem;
  }

  .summary-badge {
    grid-column: 2;
    justify-self: start;
  }

  .summary-icon {
    width: 50px;
    height: 50px;
  }

  .summary-icon svg {
    width: 25px;
    height: 25px;
  }
}

@media (max-width: 950px) and (max-height: 520px) and (orientation: landscape) {
  .glucose-health-summary {
    padding: 0.9rem 1rem;
    border-radius: 0.85rem;
  }

  .summary-header {
    gap: 0.65rem;
    padding-bottom: 0.7rem;
    margin-bottom: 0;
  }

  .summary-header-icon {
    width: 34px;
    height: 34px;
  }

  .summary-header-icon svg {
    width: 21px;
    height: 21px;
  }

  .summary-header h2 {
    font-size: 1.05rem;
    line-height: 1.15;
  }

  .summary-wide .summary-list {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }

  .summary-compact .summary-list {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }

  .summary-row {
    grid-template-columns: auto 1fr;
    align-items: center;
    gap: 0.65rem;
    padding: 0.75rem 0.85rem;
  }

  .summary-compact .summary-row + .summary-row {
    border-top: 0;
    border-left: 1px solid var(--color-border);
  }

  .summary-icon {
    width: 38px;
    height: 38px;
  }

  .summary-icon svg {
    width: 20px;
    height: 20px;
  }

  .summary-label {
    margin-bottom: 0.15rem;
    font-size: 0.8rem;
    line-height: 1.05;
  }

  .summary-value-line {
    gap: 0.25rem;
  }

  .summary-value-line strong {
    font-size: 1.45rem;
  }

  .summary-value-line span {
    font-size: 0.74rem;
  }

  .summary-meta,
  .summary-empty {
    margin-top: 0.2rem;
    font-size: 0.78rem;
    line-height: 1.1;
  }

  .summary-badge {
    grid-column: 2;
    justify-self: start;
    padding: 0.25rem 0.55rem;
    font-size: 0.72rem;
  }
}
</style>

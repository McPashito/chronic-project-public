<script setup>
import { computed } from 'vue'


const props = defineProps({
  title: {
    type: String,
    required: true,
  },
  icon: {
    type: [Object, Function],
    required: true,
  },
  variant: {
    type: String,
    default: 'blue',
  },
  value: {
    type: [String, Number],
    required: true,
  },
  unit: {
    type: String,
    default: '',
  },
  subtitle: {
    type: String,
    default: '',
  },
  badge: {
    type: String,
    default: '',
  },
  badgeVariant: {
    type: String,
    default: 'blue',
  },
  meta: {
    type: String,
    default: '',
  },
  glucoseValue: {
    type: Number,
    default: null,
  },
  momentOfDay: {
    type: String,
    default: '',
  },
})

function getResolvedBadge(glucoseValue, momentOfDay) {
  if (glucoseValue === null || glucoseValue === undefined) {
    return props.badge
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

const resolvedBadge = computed(() => {
  return getResolvedBadge(props.glucoseValue, props.momentOfDay)
})
function getResolvedVariant(glucoseValue, momentOfDay) {
  if (glucoseValue === null || glucoseValue === undefined) {
    return props.variant
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

const resolvedVariant = computed(() => {
  return getResolvedVariant(props.glucoseValue, props.momentOfDay)
})

const resolvedBadgeVariant = computed(() => {
  return getResolvedVariant(props.glucoseValue, props.momentOfDay)
})
</script>
<template>
  <article class="dash-card">
    <header class="dash-card-header">
      <p>{{ title }}</p>
    </header>

    <section class="dash-card-body">
      <div class="dash-card-main-icon" :class="`variant-${resolvedVariant}`">
        <component :is="icon" />
      </div>

      <div class="dash-card-data">
        <div class="dash-card-text">
          <h3 class="dash-card-value">
            {{ value }}
            <span v-if="unit">{{ unit }}</span>
          </h3>

          <p v-if="subtitle" class="dash-card-subtitle">
            {{ subtitle }}
          </p>
          <p v-if="meta" class="dash-card-meta">{{ meta }}</p>
        </div>

        <strong
          v-if="resolvedBadge"
          class="dash-card-badge"
          :class="`badge-${resolvedBadgeVariant}`"
        >
          {{ resolvedBadge }}
        </strong>
      </div>
    </section>
  </article>
</template>
<style scoped>
.dash-card {
  display: flex;
  flex-direction: column;
  gap: 0.85rem;

  width: 100%;
  min-width: 240px;
  max-width: none;
  min-height: 150px;
  padding: 1.25rem;

  background-color: var(--color-bg);
  border: 1.5px solid var(--color-border);
  border-radius: 0.75rem;
  box-shadow: var(--shadow-soft);
}

.dash-card-header {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
}

.dash-card-header p {
  margin: 0;

  font-size: 0.9rem;
  font-weight: 600;
  color: var(--color-text);
}
.dash-card-body {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 1rem;
  align-items: flex-start;
}
.dash-card-main-icon {
  width: 56px;
  height: 56px;

  display: flex;
  align-items: center;
  justify-content: center;

  border-radius: 50%;

  flex-shrink: 0;
}

.dash-card-main-icon svg {
  width: 28px;
  height: 28px;
}
.dash-card-main-icon.variant-blue {
  background-color: var(--dashboard-blue-bg);
  color: var(--dashboard-blue-icon);
}

.dash-card-main-icon.variant-red {
  background-color: var(--dashboard-red-bg);
  color: var(--dashboard-red-icon);
}

.dash-card-main-icon.variant-green {
  background-color: var(--dashboard-green-bg);
  color: var(--dashboard-green-icon);
}

.dash-card-main-icon.variant-yellow {
  background-color: var(--dashboard-yellow-bg);
  color: var(--dashboard-yellow-icon);
}
.dash-card-data {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.dash-card-value {
  display: flex;
  align-items: baseline;
  gap: 0.35rem;
  flex-wrap: nowrap;

  margin: 0;

  font-size: 2rem;
  font-weight: 800;
  color: var(--color-text);
}

.dash-card-value span {
  font-size: 0.95rem;
  font-weight: 700;
  white-space: nowrap;
}

.dash-card-subtitle {
  margin: 0;

  font-size: 0.95rem;
  color: var(--color-text-muted);
}
.dash-card-meta {
  margin: 0;

  font-size: 0.85rem;
  font-weight: 500;
  color: var(--color-text-muted);
}

.dash-card-badge {
  width: fit-content;
  margin-top: 0.4rem;
  padding: 0.35rem 0.75rem;

  border-radius: 999px;

  font-size: 0.85rem;
  font-weight: 700;
}
.dash-card-badge.badge-blue {
  background-color: var(--dashboard-blue-bg);
  color: var(--dashboard-blue-icon);
}

.dash-card-badge.badge-red {
  background-color: var(--dashboard-red-bg);
  color: var(--dashboard-red-icon);
}

.dash-card-badge.badge-green {
  background-color: var(--dashboard-green-bg);
  color: var(--dashboard-green-icon);
}

.dash-card-badge.badge-yellow {
  background-color: var(--dashboard-yellow-bg);
  color: var(--dashboard-yellow-icon);
}

@media (max-width: 1025px) and (orientation: portrait) {
  .dash-card {
    min-width: 0;
    max-width: 100%;
  }
  .dash-card-header {
    justify-content: flex-start;
    width: 100%;
    gap: 0.5rem;
    padding-left: 8rem;
  }

  .dash-card-header p {
    text-align: left;
    font-size: 1.5rem;
  }
  .dash-card-body {
    display: grid;
    grid-template-columns: auto 1fr;
    gap: 1.5rem;
    align-items: flex-start;
  }
  .dash-card-main-icon {
    width: 62px;
    height: 62px;
  }

  .dash-card-main-icon svg {
    width: 32px;
    height: 32px;
  }

  .dash-card-data {
    position: relative;

    display: flex;
    align-items: center;
    justify-content: center;

    width: 100%;
  }
  .dash-card-text {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    transform: translateX(-3rem);
  }

  .dash-card-value {
    font-size: 2.4rem;
  }

  .dash-card-value span {
    font-size: 1.25rem;
  }

  .dash-card-subtitle {
    font-size: 1.25rem;
  }
  .dash-card-meta {
    margin: 0;

    font-size: 1.35rem;
    font-weight: 500;
    color: var(--color-text-muted);
  }

  .dash-card-badge {
    position: absolute;
    right: 0;
    top: 50%;
    transform: translateY(-50%);

    width: fit-content;
    margin-top: 0;
    padding: 0.35rem 0.75rem;

    border-radius: 999px;

    font-size: 1.25rem;
    font-weight: 700;
  }
}

@media (max-width: 600px) and (orientation: portrait) {
  .dash-card {
    width: 100%;
    min-width: 0;
    max-width: 100%;
    padding: 1.1rem;
    gap: 0.85rem;
  }

  .dash-card-header {
    justify-content: center;
    width: 100%;
    gap: 0.5rem;
    padding-left: 0;
  }

  .dash-card-header p {
    margin: 0;
    text-align: center;
    font-size: 0.95rem;
    line-height: 1.2;
  }

  .dash-card-body {
    display: grid;
    grid-template-columns: auto 1fr;
    align-items: flex-start;
    gap: 1rem;
  }

  .dash-card-main-icon {
    width: 52px;
    height: 52px;
    margin-top: 0.45rem;
  }

  .dash-card-main-icon svg {
    width: 27px;
    height: 27px;
  }

  .dash-card-data {
    position: static;

    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: center;
    gap: 0.4rem;

    width: 100%;
  }

  .dash-card-text {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    text-align: left;

    transform: none;
  }

  .dash-card-value {
    margin: 0;
    font-size: 1.9rem;
    line-height: 1;
  }

  .dash-card-value span {
    font-size: 0.95rem;
  }

  .dash-card-subtitle {
    margin: 0;
    font-size: 0.9rem;
    text-align: left;
  }

  .dash-card-meta {
    margin: 0.3rem 0 0;

    font-size: 0.9rem;
    font-weight: 500;
    color: var(--color-text-muted);
    text-align: left;
  }

  .dash-card-badge {
    position: static;
    transform: none;

    width: fit-content;
    margin-top: 0.25rem;
    padding: 0.3rem 0.7rem;

    font-size: 0.9rem;
    font-weight: 700;
  }
}

@media (max-width: 950px) and (max-height: 520px) and (orientation: landscape) {
  .dash-card {
    min-width: 180px;
    min-height: 118px;
    gap: 0.55rem;
    padding: 0.7rem 0.75rem;
    border-radius: 0.65rem;
  }

  .dash-card-header {
    justify-content: flex-start;
    gap: 0.45rem;
  }

  .dash-card-header p {
    font-size: 0.85rem;
    line-height: 1.1;
  }

  .dash-card-body {
    grid-template-columns: 34px 1fr;
    gap: 0.55rem;
  }

  .dash-card-main-icon {
    width: 34px;
    height: 34px;
  }

  .dash-card-main-icon svg {
    width: 19px;
    height: 19px;
  }

  .dash-card-data {
    gap: 0.2rem;
  }

  .dash-card-value {
    font-size: 1.5rem;
    line-height: 1;
  }

  .dash-card-value span {
    font-size: 0.74rem;
  }

  .dash-card-subtitle,
  .dash-card-meta {
    font-size: 0.72rem;
    line-height: 1.2;
  }

  .dash-card-badge {
    margin-top: 0.2rem;
    padding: 0.25rem 0.55rem;
    font-size: 0.72rem;
  }
}
</style>

<script setup>
import { computed } from 'vue'

import { useCurrentUser } from '@/composables/useCurrentUser'

const props = defineProps({
  title: {
    type: String,
    required: true,
  },
  main: {
    type: String,
    required: true,
  },
  variant: {
    type: String,
    default: 'active',
  },
})

const emit = defineEmits(['add-glucose'])
const { currentUser } = useCurrentUser()

const resolvedTitle = computed(() => {
  if (currentUser.value?.name) {
    return `${currentUser.value.name}, ${props.title}`
  }

  return `${props.title.charAt(0).toUpperCase()}${props.title.slice(1)}`
})
</script>
<template>
  <article class="private-head">
    <section class="private-left">
      <span class="main-message"
        ><h2>{{ main }}</h2></span
      >
      <div class="private-head-sub-message">
        <h3>{{ resolvedTitle }}</h3>
      </div>
    </section>
    <button type="button" class="private-right" :class="`${variant}`" @click="emit('add-glucose')">
      <h2>+</h2>
      <h3>Añadir glucemia</h3>
    </button>
  </article>
</template>
<style scoped>
.private-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 100%;
  min-height: 120px;
  margin-bottom: 1rem;
  color: var(--color-text);
}
.private-left {
  display: flex;
  flex-direction: column;
  justify-items: flex-start;
  gap: 0.4rem;
  margin-right: auto;
}
.main-message h2 {
  margin: 0;
  font-size: 1.75rem;
  font-weight: 800;
  line-height: 1.2;
}
.private-head-sub-message h3 {
  margin: 0;
  color: var(--color-text);
  font-size: 1rem;
  font-weight: 600;
  line-height: 1.4;
}

.private-right.active {
  display: flex;
  align-items: center;

  gap: 1rem;
  margin-left: auto;
  min-height: 44px;
  padding: 0 1rem;
  box-sizing: border-box;

  border-radius: 0.5rem;
  background-color: var(--color-primary);
  border: 1px solid var(--color-primary);

  cursor: pointer;
}
.private-right.active h3 {
  margin: 0;
  color: var(--color-bg);
  font-size: 18px;
}
.private-right.active h2 {
  margin: 0;
  color: var(--color-bg);
  font-size: 22px;
}
.private-right.inactive {
  visibility: hidden;
}
.private-right.active:hover {
  background-color: var(--color-primary-dark);
}
.private-right.active:focus-visible {
  outline: 3px solid var(--color-primary-muted);
  outline-offset: 2px;
}
@media (max-width: 1025px) and (orientation: portrait) {
  .private-head {
    display: flex;
    flex-direction: column;
  }

  .main-message h2 {
    font-size: clamp(1.5rem, 4vw, 1.875rem);
  }

  .private-head-sub-message h3 {
    font-size: clamp(0.95rem, 2.2vw, 1.05rem);
  }

  .private-right.inactive {
    display: none;
  }

  .private-right.active {
    margin-left: 0;
    padding: 0.6rem 1rem;

    border-radius: 0.5rem;

    width: 100%;
  }
}

@media (max-width: 950px) and (max-height: 520px) and (orientation: landscape) {
  .private-head {
    min-height: auto;
    margin-bottom: 1rem;
    gap: 0.75rem;
  }

  .private-left {
    gap: 0.2rem;
  }

  .main-message h2 {
    margin: 0;
    font-size: 1.5rem;
    line-height: 1.1;
  }

  .private-head-sub-message h3 {
    margin: 0;
    font-size: 1rem;
    line-height: 1.25;
  }

  .private-right.inactive {
    display: none;
  }

  .private-right.active {
    gap: 0.65rem;
    padding: 0.55rem 0.9rem;
  }

  .private-right.active h2 {
    font-size: 1.2rem;
  }

  .private-right.active h3 {
    font-size: 0.95rem;
  }
}
</style>

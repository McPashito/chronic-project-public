<script setup>
import LogArrow from '@/components/Icons/LogArrow.vue'
defineProps({
  title: String,
  text: String,
  icon: Object,
  variant: String,
  link: String,
})
</script>
<template>
  <article class="diabetes-card">
    <div class="logo" :class="variant">
      <component :is="icon" />
    </div>
    <div class="content">
      <div class="content-text">
        <h4>{{ title }}</h4>
        <p>{{ text }}</p>
      </div>
      <a class="content-link" :class="variant" :href="link" target="_blank">
        Ver más
        <LogArrow />
      </a>
    </div>
  </article>
</template>
<style scoped>
.diabetes-card {
  display: grid;
  grid-template-columns: 1fr 3fr;
  background-color: var(--color-bg);
  border-radius: 1rem;
  border: 1px solid var(--color-border);
  box-shadow: var(--shadow-soft);
}
.logo {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 48px;
  height: 48px;
  padding: 0;
  border-radius: 50%;
  align-self: center;
  margin-left: 1rem;
}

.logo svg {
  width: 28px;
  height: 28px;
}

.logo.blue {
  background-color: var(--color-surface);
  color: var(--color-primary);
}
.logo.green {
  background-color: var(--color-success-soft);
  color: var(--color-success);
}
.content {
  display: flex;
  flex-direction: column;
  align-items: start;
  justify-content: center;
  margin: 0.5rem;
}
.content-text {
  display: flex;
  flex-direction: column;
  align-content: center;
  justify-content: center;
  gap: 8px;
  margin: 0.5rem 0.4rem;
}

.content-text h4,
.content-text p {
  margin: 0;
}
.content-text h4 {
  font-size: 14px;
  font-weight: bold;
}
.content-text p {
  font-size: 12px;
}
.content-link {
  display: flex;
  justify-content: center;
  align-items: center;
  width: auto;
  margin-left: 0.3rem;
  gap: 8px;
  border-radius: 0.2rem;
  padding: 0.3rem 0.4rem;
  align-items: center;
  justify-items: center;
  text-decoration: none;
  font-size: 12px;
}
.content-link .content-link a {
}
.content-link.blue {
  background-color: var(--color-surface);
  color: var(--color-primary);
}
.content-link.green {
  background-color: var(--color-success-soft);
  color: var(--color-success);
}
@media (max-width: 1025px) and (orientation: portrait) {
  .content-text h4 {
    font-size: 22px;
  }

  .content-text p {
    font-size: 20px;
  }

  .content-link {
    font-size: 16px;
  }
}
@media (max-width: 768px) {
  .content-text h4 {
    font-size: 18px;
  }

  .content-text p {
    font-size: 16px;
  }

  .content-link {
    font-size: 12px;
  }
}
</style>

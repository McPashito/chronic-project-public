<script setup>
defineProps({
  title: String,
  text: String,
  icon: Object,
  variant: String,
})
</script>
<template>
  <article class="home-card">
    <div class="icon-box" :class="variant">
      <component :is="icon" />
    </div>
    <div class="text">
      <h4>{{ title }}</h4>
      <p>{{ text }}</p>
    </div>
  </article>
</template>
<style>
.home-card {
  display: flex;
  align-items: center;
  width: 100%;
  gap: 1rem;
  border: 1px solid var(--color-border);
  border-radius: 1rem;
  background-color: var(--color-bg);
  box-shadow: var(--shadow-soft);
  padding: 16px 20px;
}

.icon-box {
  width: 56px;
  height: 56px;
  border-radius: 50%;

  display: flex;
  align-items: center;
  justify-content: center;
}
.pencil {
  background-color: rgba(25, 135, 84, 0.12);
  color: var(--color-success);
}
.schedule {
  background-color: rgba(51, 117, 222, 0.12);
  color: var(--color-primary);
}
.chart {
  background-color: rgba(135, 115, 25, 0.12);
  color: var(--color-warning);
}

.icon-box svg {
  width: 32px;
  height: 32px;
}
.home-card .text {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.text h4,
.text p {
  margin: 0;
}

.text h4 {
  font-size: 14px;
}

.text p {
  font-size: 12px;
  max-width: 220px;
}
@media (max-width: 1025px) and (orientation: portrait) {
  .home-card {
    padding: 24px 28px;
    gap: 1.5rem;
  }

  .icon-box {
    width: 72px;
    height: 72px;
    flex-shrink: 0;
  }

  .icon-box svg {
    width: 42px;
    height: 42px;
  }

  .text h4 {
    font-size: 22px;
  }

  .text p {
    font-size: 20px;
    max-width: none;
  }
}
@media (max-width: 768px) {
  .home-card {
    padding: 20px 22px;
    gap: 1rem;
  }

  .icon-box {
    width: 60px;
    height: 60px;
    flex-shrink: 0;
  }

  .icon-box svg {
    width: 34px;
    height: 34px;
  }

  .text h4 {
    font-size: 18px;
  }

  .text p {
    font-size: 16px;
    max-width: none;
  }
}
</style>

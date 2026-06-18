<script setup>
import InfoIcon from '@/components/Icons/InfoIcon.vue'
import diabetes from '../assets/diabetes.png'
import DiabetesViewCard from '@/components/Home/DiabetesViewCard.vue'

import HeartBeat from '@/components/Icons/HeartBeat.vue'
import DropIcon from '@/components/Icons/DropIcon.vue'
import SecurityIcon from '@/components/Icons/SecurityIcon.vue'
import SeedIcon from '@/components/Icons/SeedIcon.vue'
import AtentionIcon from '@/components/Icons/AtentionIcon.vue'
import AppleIcon from '@/components/Icons/AppleIcon.vue'
import ActivityIcon from '@/components/Icons/ActivityIcon.vue'
import MoonIcon from '@/components/Icons/MoonIcon.vue'
import DropIconFull from '@/components/Icons/DropIconFull.vue'
</script>
<template>
  <section class="diabetes">
    <section class="diabetes-head-grid">
      <div class="diabetes-head-containt">
        <h1>¿Que es la diabetes?</h1>
        <p>La diabetes es una enfermedad crónica que afecta al control de la glucosa en sangre.</p>
        <p>
          Conocerla y llevar un buen seguimiento ayuda a prevenir complicaciones y mejorar el
          autocuidado.
        </p>
      </div>
      <div class="diabetes-head-image">
        <img :src="diabetes" alt="diabetes" class="diabetes-head-image-png" />
      </div>
      <div class="diabetes-head-side">
        <div class="mas-info">
          <InfoIcon class="info" />
          <h3>¿Necesitas mas información?</h3>
        </div>
        <div class="info-info">
          <p>
            La información de esta página es orientativa y no sustituye la valoración de un
            profesional sanitario. Puedes ampliar información en la web oficial de la International
            Diabetes Federation a través del enlace debajo del texto.
          </p>
        </div>

        <a class="link" href="https://idf.org/es/about-diabetes/what-is-diabetes/"
          >IDF - ¿Que es la diabetes?</a
        >
      </div>
    </section>
    <section class="diabetes-tail-grid">
      <div class="diabetes-info">
        <div class="diabetes-info-head"><h2>Aprende más sobre la diabetes</h2></div>
        <div class="diabetes-info-cards">
          <DiabetesViewCard
            title="Tipos de diabetes"
            text="Conoce las principales clasificaciones y sus caracteristicas"
            :icon="DropIcon"
            variant="blue"
            link="https://idf.org/es/about-diabetes/what-is-diabetes/"
          />
          <DiabetesViewCard
            title="Sintoma"
            text="Identifica los síntomas comunes y cuándo prestar atencion"
            :icon="HeartBeat"
            variant="green"
            link="https://idf.org/es/about-diabetes/prediabetes/"
          />
          <DiabetesViewCard
            title="Complicaciones"
            text="Descubre qué complicaciones pueden surgir en la diabetes mal tratada"
            :icon="SecurityIcon"
            variant="blue"
            link="https://idf.org/es/about-diabetes/complications/"
          />
          <DiabetesViewCard
            title="Consejos y prevención"
            text="Hábitos saludables que tu ayudan a prevenir y controlar tu diabetes"
            :icon="SeedIcon"
            variant="green"
            link="https://idf.org/es/about-diabetes/diabetes-prevention/"
          />
        </div>
        <div class="diabetes-info-banner">
          <div class="diabetes-info-banner-logo">
            <AtentionIcon />
          </div>
          <div class="diabetes-info-banner-text">
            <h3>Importante</h3>
            <p>
              Esta información es educativa y no sustituye la opinión de un profesional de la salud.
              Consulta siempre con tu médico para un diagnóstico y tratamiento adecuados.
            </p>
          </div>
        </div>
      </div>
      <div class="diabetes-advice">
        <h3 class="diabetes-advice-heading">Consejos clave</h3>
        <article class="diabetes-advice-text">
          <div class="diabetes-advice-text-detail"><DropIconFull /></div>
          <p class="diabetes-advice-text-content">
            Controla tus niveles de glucosa de forma regular.
          </p>
        </article>
        <article class="diabetes-advice-text">
          <div class="diabetes-advice-text-detail"><AppleIcon /></div>
          <p class="diabetes-advice-text-content">Lleva una alimentación balanceada y saludable.</p>
        </article>
        <article class="diabetes-advice-text">
          <div class="diabetes-advice-text-detail"><ActivityIcon /></div>
          <p class="diabetes-advice-text-content">Realiza actividad física moderada cada día.</p>
        </article>
        <article class="diabetes-advice-text">
          <div class="diabetes-advice-text-detail"><MoonIcon /></div>
          <p class="diabetes-advice-text-content">Descansa lo suficiente y reduce el estrés.</p>
        </article>
        <a
          class="diabetes-advice-link"
          href="https://idf.org/es/about-diabetes/diabetes-prevention/"
          >Ver mas consejos</a
        >
      </div>
    </section>
  </section>
</template>
<style scoped>
.diabetes-head-grid,
.diabetes-tail-grid {
  width: 100%;
  max-width: 1200px;
}
.diabetes {
  display: flex;
  flex-direction: column;
  align-items: center;

  margin: 1rem 2rem;
}
.diabetes-head-grid {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr;
  color: var(--color-primary-dark);

  margin: 0 2rem 2rem 2rem;
  background-color: var(--color-surface);
  border-radius: 1rem;
}
.diabetes-head-containt h1,
.diabetes-head-containt p {
  margin: 0;
}
.diabetes-head-containt h1 {
  font-size: 40px;
}
.diabetes-head-containt p {
  font-size: 24px;
}
.diabetes-head-containt {
  display: flex;
  flex-direction: column;

  justify-content: center;
  margin: 2rem;
  gap: 2rem;
}
.diabetes-head-side {
  display: flex;
  flex-direction: column;
  justify-content: center;
  margin: 2rem;
  gap: 0.5rem;
  background-color: var(--color-bg);
  border-radius: 0.5rem;
  box-shadow: var(--shadow-soft);
  padding: 0.5rem 0.5rem;
}
.mas-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin: 8px;
  font-weight: 600;
}
.mas-info h3 {
  font-size: 12px;
  margin: 0;
}
.info {
  color: var(--color-primary);
}
.info-info p {
  font-size: 12px;
}
.link {
  text-decoration: none;
  border-radius: 0.5rem;
  border-style: solid;
  background-color: var(--color-primary);
  color: var(--color-surface);
  padding: 0.5rem 0.7rem;
}
.diabetes-head-image {
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}
.diabetes-head-image::after {
  content: '';
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  height: 120px;
  background: linear-gradient(to bottom, transparent, var(--color-surface));
  pointer-events: none;
}
.diabetes-head-image .diabetes-head-image-png {
  width: 130%;
  height: auto;
  max-width: none;
}
.diabetes-tail-grid {
  display: grid;
  grid-template-columns: 4fr 1fr;
}
.diabetes-info {
  display: flex;
  flex-direction: column;
}
.diabetes-info-head {
  color: var(--color-primary);
}
.diabetes-info-head h2 {
  font-size: 28px;
  font-weight: 600;
  margin: 1em 0;
}

.diabetes-info-cards {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr 1fr;

  gap: 1rem;
}

.diabetes-info-banner {
  display: flex;
  justify-content: start;
  align-items: center;
  background-color: var(--color-success-soft);
  border: 1px solid var(--color-success);
  border-radius: 1rem;
  margin-top: 2rem;
  padding: 1rem;
}
.diabetes-info-banner-logo {
  display: flex;
  justify-content: center;
  color: var(--color-success);
  width: 90px;
}
.diabetes-info-banner-text {
  display: flex;
  flex-direction: column;
  gap: 8px;
  color: var(--color-success);
}
.diabetes-info-banner-text p,
.diabetes-info-banner-text h3 {
  margin: 0;
}
.diabetes-info-banner-text h3 {
  font-size: 12px;
  font-weight: bolder;
}
.diabetes-info-banner-text p {
  font-size: 12px;

  max-width: 500px;
}
.diabetes-advice {
  display: flex;
  flex-direction: column;

  background-color: var(--color-surface);
  border-radius: 1rem;
  padding: 1rem 1rem;
  margin: 0rem 1rem;
}
.diabetes-advice h3 {
  margin: 0;
  font-size: 20px;
}
.diabetes-advice-text {
  display: flex;
  justify-items: flex-start;
  align-items: center;
  gap: 1rem;
}
.diabetes-advice-text-detail {
  background-color: var(--color-bg);
  border-radius: 0.5rem;
  color: var(--color-primary);
}
.diabetes-advice-text-detail svg {
  height: 28px;
  width: 28px;
}
.diabetes-advice-text-content {
  font-size: 12px;
}
.diabetes-advice-link {
  background-color: var(--color-primary);
  color: var(--color-bg);
  border-radius: 0.5rem;
  margin: 0.5rem 0;
  padding: 0.4rem 0.5rem;
  text-decoration: none;
}
@media (max-width: 1025px) and (orientation: portrait) {
  .diabetes-head-grid,
  .diabetes-tail-grid {
    width: 100%;
    max-width: 1024px;
  }
  .diabetes {
    margin: 0.5rem 1rem;
  }
  .diabetes-head-grid {
    display: grid;
    grid-template-columns: 1fr;
    margin: 0 0 2rem 0;
    border-radius: 0.5rem;
  }
  .diabetes-head-containt {
    max-width: 90%;
  }
  .diabetes-head-image .diabetes-head-image-png {
    width: 60%;
    height: auto;
    max-width: none;
  }
  .diabetes-tail-grid {
    display: grid;
    grid-template-columns: 1fr;
  }
  .diabetes-advice {
    margin-top: 1rem;
  }
  .diabetes-info-cards {
    display: grid;
    grid-template-columns: 1fr;
  }
  .diabetes-head-containt h1 {
    font-size: 40px;
  }

  .diabetes-head-containt p {
    font-size: 24px;
  }

  .info-info p,
  .mas-info h3 {
    font-size: 20px;
  }

  .link,
  .diabetes-advice-link {
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    font-size: 18px;
  }
  .content-text h4 {
    font-size: 22px;
  }

  .content-text p {
    font-size: 20px;
  }

  .content-link {
    font-size: 16px;
  }
  .diabetes-info-banner-text h3 {
    font-size: 20px;
  }

  .diabetes-info-banner-text p {
    font-size: 18px;
  }

  .diabetes-info-banner-logo svg {
    width: 42px;
    height: 45px;
  }
  .diabetes-advice h3 {
    font-size: 20px;
  }

  .diabetes-advice-text-content {
    font-size: 18px;
  }

  .diabetes-advice-text-detail svg {
    width: 42px;
    height: 42px;
  }
  .diabetes-advice-text {
    gap: 0.5rem;
  }

  .diabetes-advice-link {
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    text-align: center;
  }
}
@media (max-width: 768px) {
  .diabetes-head-grid,
  .diabetes-tail-grid {
    width: 100%;
    max-width: 740px;
  }
  .diabetes-head-image .diabetes-head-image-png {
    width: 90%;
    height: auto;
    max-width: none;
  }
  .diabetes-info-cards {
    display: grid;
    grid-template-columns: 1fr;
  }
  .diabetes-head-containt h1 {
    font-size: 28px;
  }

  .diabetes-head-containt p {
    font-size: 16px;
  }

  .info-info p,
  .mas-info h3 {
    font-size: 16px;
  }

  .link,
  .diabetes-advice-link {
    font-size: 16px;
  }

  .content-text h4 {
    font-size: 18px;
  }

  .content-text p {
    font-size: 16px;
  }

  .content-link {
    font-size: 12px;
  }

  .diabetes-info-banner-text h3 {
    font-size: 16px;
  }

  .diabetes-info-banner-text p {
    font-size: 14px;
  }

  .diabetes-advice h3 {
    font-size: 16px;
  }

  .diabetes-advice-text-content {
    font-size: 14px;
  }
}
</style>

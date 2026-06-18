<script setup>
import HomeCard from '@/components/Home/HomeCard.vue'
import about from '../assets/about.png'
import FormPencil from '@/components/Icons/FormPencil.vue'
import ChartIcon from '@/components/Icons/ChartIcon.vue'
import SecurityIcon from '@/components/Icons/SecurityIcon.vue'
import HeartIcon from '@/components/Icons/HeartIcon.vue'
import PeopleIcon from '@/components/Icons/PeopleIcon.vue'
import StarIcon from '@/components/Icons/StarIcon.vue'
</script>
<template>
  <section class="about">
    <section class="about-flex">
      <div class="about-flex-head">
        <div class="about-flex-head-info">
          <h1>Sobre Chronic Project</h1>
          <h2>Tu compañero diario en el control de la diabetes</h2>
          <p>
            Chronic Project nace con la misión de ayudar a las personas con diabetes a llevar un
            mejor control de su glucosa en sangre de forma sencilla, visual y segura. Nuestra
            aplicación te permite registrar tus mediciones, analizar tu evolución y tomar decisiones
            informadas para mejorar tu bienestar cada día.
          </p>
        </div>
        <div class="about-flex-head-image">
          <img class="image" :src="about" alt="Mockup de app de about" />
        </div>
      </div>
      <div class="about-flex-head-subtitle">
        <h2>¿Qué puedes hacer con Chronic Project?</h2>
      </div>
      <div class="about-flex-head-grid">
        <HomeCard
          title="Registra tus mediciones"
          text="Añade tus niveles de glucosa en segundos y lleva un control completo de tu día a día."
          :icon="FormPencil"
          variant="schedule"
        />
        <HomeCard
          title="Analiza tu evolución"
          text="Visualiza tus datos con gráficos y filtros por fechas y momentos del día."
          :icon="ChartIcon"
          variant="pencil"
        />
        <HomeCard
          title="Tu información segura"
          text="Tus datos están protegidos y solo tú tienes acceso a ellos. Privacidad y seguridad garantizadas."
          :icon="SecurityIcon"
          variant="schedule"
        />
        <HomeCard
          title="Mejora tu bienestar"
          text="Con información clara puedes tomar mejores decisiones para cuidar tu salud cada día."
          :icon="HeartIcon"
          variant="pencil"
        />
        <HomeCard
          title="Hecho para ti"
          text="Diseñado para ser fácil de usar, intuitivo y adaptado a tus necesidades."
          :icon="PeopleIcon"
          variant="schedule"
        />
      </div>
      <div class="about-flex-head-ending">
        <div class="about-flex-head-ending-logo">
          <StarIcon />
        </div>
        <div class="about-flex-head-ending-text">
          <h3>Este proyecto está en constante evolución</h3>
          <p>
            Seguimos trabajando para ofrecerte nuevas herramientas para la mejor experiencia posible
          </p>
        </div>
      </div>
    </section>
  </section>
</template>

<style scoped>
.about-flex-head,
.about-flex-head-subtitle,
.about-flex-head-grid,
.about-flex-head-ending {
  width: 100%;
  max-width: 1200px;
}
.about-flex-head-info h1 {
  font-size: 40px;
  color: var(--color-primary-dark);
  font-weight: 600;
}
.about-flex-head-info h2 {
  font-size: 28px;
  color: var(--color-primary-dark);
  font-weight: 400;
}
.about-flex-head-info p {
  font-size: 24px;
}
.about-flex-head-info p,
.about-flex-head-info h2,
.about-flex-head-info h1 {
  margin: 12px;
}
.about {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 3rem;
  margin: 1rem 2rem;
}
.about-flex-head {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  background-color: var(--color-surface);
  padding: 2rem;
  border-radius: 1rem;
}
.about-flex-head-info {
  display: flex;
  flex-direction: column;
}
.about-flex-head-image {
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0;
  padding: 0;
}

.about-flex-head-image .image {
  width: 100%;
  max-width: 300px;
  height: auto;
  display: block;
}
.about-flex-head-subtitle h2 {
  font-size: 28px;
  color: var(--color-primary-dark);
  font-weight: 400;
  margin: 1.33em 0;
}
.about-flex-head-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 1rem;
}
.about-flex-head-ending {
  display: flex;
  justify-content: start;
  align-items: center;
  background-color: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: 1rem;
  margin-top: 2rem;
  padding: 1rem;
}
.about-flex-head-ending-logo {
  display: flex;
  justify-content: center;
  color: var(--color-primary);
  width: 90px;
}
.about-flex-head-ending-text {
  display: flex;
  flex-direction: column;
  gap: 8px;
  color: var(--color-primary);
}
.about-flex-head-ending-text p,
.about-flex-head-ending-text h3 {
  margin: 0;
}
.about-flex-head-ending-text h3 {
  font-size: 12px;
  font-weight: bolder;
}
.about-flex-head-ending-text p {
  font-size: 12px;

  max-width: 500px;
}

@media (max-width: 1025px) and (orientation: portrait) {
  .about-flex-head,
  .about-flex-head-subtitle,
  .about-flex-head-grid,
  .about-flex-head-ending {
    width: 100%;
    max-width: 1024px;
  }
  .about {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 1.5rem;
    margin: 0.5rem 1rem;
  }
  .about-flex-head {
    display: grid;
    grid-template-columns: 1fr;
    gap: 1rem;
    background-color: var(--color-surface);
    padding: 2rem;
    border-radius: 0.5rem;
  }
  .about-flex-head-image .image {
    max-width: 280px;
  }
  .about-flex-head-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    align-items: stretch;

    gap: 1.5rem;
  }
  .about-flex-head-grid > :last-child {
    grid-column: 1 / -1;
  }
  .about-flex-head-ending-logo {
    width: 70px;
    flex-shrink: 0;
  }
  .about-flex-head-ending-text {
    gap: 4px;
  }
  .about-flex-head-ending-text h3 {
    font-size: 20px;
  }

  .about-flex-head-ending-text p {
    font-size: 18px;
  }

  .about-flex-head-ending-logo svg {
    width: 42px;
    height: 42px;
  }
}
@media (max-width: 768px) {
  .about-flex-head,
  .about-flex-head-subtitle,
  .about-flex-head-grid,
  .about-flex-head-ending {
    width: 100%;
    max-width: 740px;
  }
  .about-flex-head-grid {
    grid-template-columns: 1fr;
  }

  .about-flex-head-grid > :last-child {
    grid-column: auto;
  }
  .about-flex-head-grid {
    gap: 1rem;
  }
  .about-flex-head-ending-text h3 {
    font-size: 16px;
  }

  .about-flex-head-ending-text p {
    font-size: 14px;
  }

  .about-flex-head-ending-logo {
    width: 50px;
    flex-shrink: 0;
  }

  .about-flex-head-ending-logo svg {
    width: 32px;
    height: 32px;
  }
  .about-flex-head {
    padding: 1.2rem;
  }
  .about-flex-head-image .image {
    max-width: 180px;
  }
  .about-flex-head-info h1 {
    font-size: 28px;
  }

  .about-flex-head-info h2 {
    font-size: 20px;
  }

  .about-flex-head-info p {
    font-size: 16px;
  }

  .about-flex-head-subtitle h2 {
    font-size: 20px;
  }
}
</style>

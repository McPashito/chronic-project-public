<script setup>
import LogArrow from '@/components/Icons/LogArrow.vue'
import RegisterUserIcon from '@/components/Icons/RegisterUserIcon.vue'
import SecurityIcon from '@/components/Icons/SecurityIcon.vue'
import HomeCard from '@/components/Home/HomeCard.vue'
import FormPencil from '@/components/Icons/FormPencil.vue'
import ScheduleIcon from '@/components/Icons/ScheduleIcon.vue'
import ChartIcon from '@/components/Icons/ChartIcon.vue'
import SeedIcon from '@/components/Icons/SeedIcon.vue'
import DropIcon from '@/components/Icons/DropIcon.vue'
import HeartBeat from '@/components/Icons/HeartBeat.vue'
import PillIcon from '@/components/Icons/PillIcon.vue'
import hero from '../assets/hero.png'
</script>
<template>
  <section class="home-page">
    <section class="home-hero">
      <div class="hero-content">
        <h1>Controla tus glucemias,<br />controla tu bienestar</h1>
        <p>
          Registra, consulta y visualiza tus mediciones de glucosa de forma sencilla para tomar
          mejores decisiones cada día
        </p>
        <nav class="hero-actions">
          <RouterLink class="register" to="/register"
            ><RegisterUserIcon class="logicon" /> Crear cuenta gratis</RouterLink
          >
          <RouterLink class="login" to="/login">
            Iniciar sesión <LogArrow class="logicon"
          /></RouterLink>
        </nav>
        <nav class="security">
          <SecurityIcon class="icon" />
          <p class="message">Tus datos estan seguros y protegidos</p>
        </nav>
      </div>

      <div class="hero-visual">
        <img class="hero-image" :src="hero" alt="Mockup de app de glucemias" />
      </div>
    </section>

    <section class="features-section">
      <HomeCard
        title="Registro sencillo"
        text="Añade tus mediciones de glucosa estés donde estés"
        :icon="FormPencil"
        variant="pencil"
      />
      <HomeCard
        title="Historial completo"
        text="Consulta todos tus registros y detecta patrones a lo largo del tiempo"
        :icon="ScheduleIcon"
        variant="schedule"
      />
      <HomeCard
        title="Evolución visual"
        text="Gráficas claras que te ayudan a entender tu evolución de un vistazo"
        :icon="ChartIcon"
        variant="chart"
      />
    </section>

    <section class="future-section">
      <div class="left">
        <div class="future-icon-box">
          <SeedIcon class="seed" />
        </div>
        <div class="future">
          <h2>Un proyecto que mira al futuro</h2>
          <p>
            Chronic Project comienza con el control de la glucosa, pero está pensado para crecer
            contigo. Proximamente podrás también llevar el seguimiento de otras condiciones crónicas
            como la tensión arterial y la medicación
          </p>
        </div>
      </div>
      <div class="right">
        <div class="right-item">
          <div class="right-box">
            <DropIcon />
          </div>
          <span>Glucosa</span>
        </div>

        <div class="right-item">
          <div class="right-box">
            <HeartBeat />
          </div>
          <span>Tensión arterial</span>
        </div>

        <div class="right-item">
          <div class="right-box">
            <PillIcon />
          </div>
          <span>Medicación</span>
        </div>
      </div>
    </section>
  </section>
</template>
<style>
.home-hero,
.features-section,
.future-section {
  width: 100%;
  max-width: 1200px;
}
.home-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2rem;
  margin: 1rem 2rem;
}
.home-hero {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  background-color: var(--color-surface);
  padding: 2rem;
  border-radius: 1rem;
}

.hero-content {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.hero-content h1 {
  font-size: 40px;
}
.hero-content p {
  font-size: 24px;
}
.hero-content .hero-actions {
  display: flex;
  gap: 0.5rem;
}
.hero-actions a {
  display: flex;
  gap: 0.5rem;
  text-decoration: none;
  border-radius: 0.5rem;
  border-style: solid;
  border-width: 1px;
  border-color: var(--color-border);
  padding: 0.7rem;
}
.hero-actions .register {
  background-color: var(--color-primary);
  color: var(--color-surface);
  gap: 0.5rem;
}
.hero-actions .login {
  background-color: var(--color-bg);
  gap: 0.5rem;
  color: var(--color-primary);
}

.security {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 1rem;
  font-size: 12px;
}
.security .icon {
  fill: var(--color-success);
  height: 18px;
  width: 18px;
}
.hero-visual {
  display: flex;
  align-items: center;
  justify-content: center;
}

.hero-image {
  width: 100%;
  max-width: 420px;
  height: auto;
  display: block;
}
.features-section {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
}

.future-section {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  background-color: var(--color-success-soft);
  border: 1px solid var(--color-success-border);
  border-radius: 1rem;
}
.future h2,
.future p {
  margin: 0;
}
.future h2 {
  font-size: 12px;
}
.future p {
  font-size: 12px;
  max-width: 400px;
}
.future {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}
.future-icon-box {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background-color: var(--color-success-soft);
  color: var(--color-success);
  display: flex;
  align-items: center;
  justify-content: center;
}

.future-icon-box svg {
  width: 32px;
  height: 32px;
}
.left {
  display: flex;
  align-items: center;
  gap: 2rem;
  padding: 2rem;
}

.future-section .right {
  display: flex;
  gap: 2rem;
  align-items: center;
  justify-content: space-evenly;
}
.right-box {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background-color: var(--color-bg);
  display: flex;
  align-items: center;
  justify-content: center;
}
.right-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  font-size: 12px;
}

@media (max-width: 1025px) and (orientation: portrait) {
  .home-hero,
  .features-section,
  .future-section {
    width: 100%;
    max-width: 1024px;
  }
  .home-page {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    margin: 0.5rem 1rem;
  }
  .home-hero {
    display: grid;
    grid-template-columns: repeat(1, 2fr);
    gap: 1rem;
    padding: 1rem;
    border-radius: 0.5rem;
  }
  .hero-content {
    order: 2;
    gap: 8px;
  }
  .hero-content .hero-actions {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }
  .hero-actions a {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 0.7rem;
  }
  .features-section {
    display: grid;
    grid-template-columns: repeat(1, 3fr);
    gap: 1rem;
  }
  .features-section .home-card {
    border-radius: 0.5rem;
  }
  .future-section {
    display: grid;
    grid-template-columns: repeat(1, 2fr);
    border-radius: 0.5rem;
    margin: 0.5rem;
    padding-right: 0.5rem;
  }
  .future-section .right {
    margin-bottom: 1rem;
  }
  .hero-content h1 {
    font-size: 28px;
  }
  .hero-content p {
    font-size: 16px;
  }
  .future h2 {
    font-size: 20px;
  }
  .future p {
    font-size: 18px;
  }
}
@media (max-width: 768px) {
  .home-hero,
  .features-section,
  .future-section {
    width: 100%;
    max-width: 740px;
  }
  .hero-content h1 {
    font-size: 24px;
  }
  .hero-content p {
    font-size: 14px;
  }
  .future h2 {
    font-size: 20px;
  }
  .future p {
    font-size: 14px;
  }
}
</style>

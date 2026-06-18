<script setup>
import MailIcon from '@/components/Icons/MailIcon.vue'
import contact from '../assets/contact.png'
import ClockIcon from '@/components/Icons/ClockIcon.vue'
import LocationIcon from '@/components/Icons/LocationIcon.vue'
import ChatIcon from '@/components/Icons/ChatIcon.vue'
</script>
<template>
  <section class="contact">
    <section class="contact-flex">
      <div class="contact-flex-head">
        <div class="contact-flex-head-info">
          <h1>Contacto</h1>
          <h2>Estamos aquí para ayudarte</h2>
          <p>
            Si tienes dudas, sugerencias o tienes algun problema, no dudes en ponerte en contacto
            con nosotros.
          </p>
        </div>
        <div class="contact-flex-head-image">
          <img class="image" :src="contact" alt="Mockup de app de contact" />
        </div>
      </div>
      <div class="contact-flex-tail">
        <div class="contact-form">
          <form class="form" action="">
            <h3>Envíanos un mensaje</h3>

            <label class="sr-only" for="nombre">Nombre</label>
            <input id="nombre" type="text" placeholder="Nombre" />

            <label class="sr-only" for="email">Correo electrónico</label>
            <input id="email" type="email" placeholder="Correo Electronico" />

            <label class="sr-only" for="asunto">Asunto</label>
            <input id="asunto" type="text" placeholder="Asunto" />

            <label class="sr-only" for="mensaje">Mensaje</label>
            <textarea id="mensaje" placeholder="Mensaje"></textarea>
            <button type="button">Enviar</button>
          </form>
        </div>
        <div class="contact-info">
          <h3>Otras formas de contacto</h3>
          <article class="contact-banner">
            <div class="contact-banner-content">
              <MailIcon class="contact-icon" />
              <div class="contact-text">
                <h6>E-Mail</h6>
                <p>info@chronicproject.com</p>
              </div>
            </div>
            <div class="contact-banner-content">
              <ClockIcon class="contact-icon" />
              <div class="contact-text">
                <h6>Horarios</h6>
                <p>Lunes a viernes (09:00 - 18:00)</p>
              </div>
            </div>
            <div class="contact-banner-content">
              <LocationIcon class="contact-icon" />
              <div class="contact-text">
                <h6>Ubicación</h6>
                <p>España</p>
              </div>
            </div>
            <div class="contact-banner-content">
              <ChatIcon class="contact-icon" />
              <div class="contact-text">
                <h6>Respuesta</h6>
                <p>Te responderemos lo antes posible</p>
              </div>
            </div>
          </article>
        </div>
      </div>
    </section>
  </section>
</template>
<style scoped>
.contact-flex-head,
.contact-flex-head-subtitle,
.contact-flex-head-grid,
.contact-flex-head-ending {
  width: 100%;
  max-width: 1200px;
}
.contact-flex-head-info h1 {
  font-size: 40px;
  color: var(--color-primary-dark);
  font-weight: 600;
}
.contact-flex-head-info h2 {
  font-size: 28px;
  color: var(--color-primary-dark);
  font-weight: 400;
}
.contact-flex-head-info p {
  font-size: 24px;
}
.contact-flex-head-info p,
.contact-flex-head-info h2,
.contact-flex-head-info h1 {
  margin: 12px;
}
.contact {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 3rem;
  margin: 1rem 2rem;
}
.contact-flex-head {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  background-color: var(--color-surface);
  padding: 2rem;
  border-radius: 1rem;
}
.contact-flex-head-info {
  display: flex;
  flex-direction: column;
}
.contact-flex-head-image {
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0;
  padding: 0;
}

.contact-flex-head-image .image {
  width: 100%;
  max-width: 200px;
  height: auto;
  display: block;
  background-color: var(--color-surface);
}
.contact-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  margin: 1rem;
  width: 90%;
}
.contact-banner {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
.contact-banner-content {
  display: flex;
  background-color: var(--color-surface);
  border-radius: 0.25rem;
  padding: 0.8rem 0.7rem;
  gap: 0.5rem;
}
.contact-info h3 {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
  color: var(--color-primary);
}
.contact-text h6 {
  margin: 0;
  font-size: 14px;
  font-weight: 400;
  color: var(--color-primary);
}
.contact-text p {
  margin: 0;
  font-size: 14px;
}
.contact-icon {
  color: var(--color-primary);
}
.contact-icon svg {
  height: 32px;
  width: 32px;
  border-radius: 50%;
  background-color: var(--color-bg);
}
.contact-flex-tail {
  display: grid;
  grid-template-columns: 2fr 1fr;
}
.contact-form {
  display: flex;
  flex-direction: column;
}
.form {
  display: flex;
  flex-direction: column;
  gap: 18px;
  width: 75%;
}
.form h3 {
  font-size: 20px;
  color: var(--color-primary);
}

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

.form input,
.form textarea {
  font-size: 10px;
  border-radius: 0.25rem;
  border: 1px solid var(--color-border);
  padding: 0.4rem 0.4rem;
  color: var(--color-border);
  font-family: inherit;
}
#mensaje {
  min-height: 110px;
}
.form button {
  border: none;
  border-radius: 0.24rem;
  background-color: var(--color-primary);
  color: var(--color-bg);
  padding: 0.6rem 0.7rem;
  width: 25%;
  cursor: pointer;
}

@media (max-width: 1025px) and (orientation: portrait) {
  .contact,
  .contact-flex-head,
  .contact-flex-head-grid,
  .contact-flex-tail {
    width: 100%;
    max-width: 1024px;
  }
  .contact {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 1.5rem;
    margin: 0.5rem 0.5rem;
  }
  .contact-flex-head {
    display: grid;
    grid-template-columns: 1fr;
    gap: 1rem;
    background-color: var(--color-surface);
    padding: 2rem;
    border-radius: 0.5rem;
  }

  .contact-flex-head-image .image {
    max-width: 200px;
  }
  .contact-flex-head-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    align-items: stretch;

    gap: 1.5rem;
  }
  .contact-flex-tail {
    display: grid;
    grid-template-columns: 1fr;
    justify-items: center;
  }
  .contact-info h3 {
    font-size: 24px;
  }
  .contact-form {
    width: 100%;
    align-items: center;
  }
  .form {
    width: 100%;
  }
  .form h3 {
    font-size: 24px;
  }
  .contact-info {
    align-items: flex-start;
    width: 100%;
    gap: 3rem;
    margin-top: 1rem;
  }

  .contact-banner {
    margin: 0;
    width: 100%;
  }
  .contact-banner-content {
    margin: 0;
    padding: 1.5rem 2.2rem;
    gap: 1.5rem;
  }
  .contact-text h6 {
    font-size: 20px;
  }
  .contact-text p {
    font-size: 20px;
  }
  .form input,
  .form textarea {
    font-size: 20px;
    padding: 0.6rem 1.5rem;
  }
  .form button {
    width: 100%;
    font-size: 20px;
    text-align: center;
    width: 75%;
    margin: 0 auto;
  }
  #mensaje {
    min-height: 160px;
  }
}
@media (max-width: 768px) {
  .contact,
  .contact-flex-head,
  .contact-flex-head-grid,
  .contact-flex-tail {
    width: 100%;
    max-width: 740px;
  }
  .contact {
    width: auto;
    margin: 0.5rem 1rem;
  }
}
</style>

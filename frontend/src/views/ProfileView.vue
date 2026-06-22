<script setup>
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'

import AppPrivateStart from '@/components/layout/AppPrivateStart.vue'
import GlucoseHealthSummary from '@/components/Home/GlucoseHealthSummary.vue'
import ProfileModal from '@/components/Home/ProfileModal.vue'
import PremiumPlanForm from '@/components/Home/PremiumPlanForm.vue'

import ConfigIcon from '@/components/Icons/ConfigIcon.vue'
import EyeUpIcon from '@/components/Icons/EyeUpIcon.vue'
import LockerIcon from '@/components/Icons/LockerIcon.vue'
import MailIcon from '@/components/Icons/MailIcon.vue'
import PeopleIcon from '@/components/Icons/PeopleIcon.vue'
import ScheduleIcon from '@/components/Icons/ScheduleIcon.vue'
import SecurityIcon from '@/components/Icons/SecurityIcon.vue'

import { updateCurrentUser } from '@/services/userService'
import { useCurrentUser } from '@/composables/useCurrentUser'
import { changePassword } from '@/services/securityService'
import { getGlucoseRecords } from '@/services/glucoseService'
import { handleAuthError } from '@/utils/handleAuthError'
import StarIcon from '@/components/Icons/StarIcon.vue'
import PencilIcon from '@/components/Icons/PencilIcon.vue'

const router = useRouter()

const { currentUser, isCurrentUserLoading, currentUserError, setCurrentUser } = useCurrentUser()
const glucoseRecords = ref([])
const glucoseRecordsError = ref('')
const isLoadingGlucoseRecords = ref(false)

const isProfileModalOpen = ref(false)
const profileModalMode = ref('edit-profile')
const profileModalError = ref('')
const profileModalSuccess = ref('')
const isSubmittingProfileModal = ref(false)

const showPremiumModal = ref(false)
const premiumError = ref('')
const premiumSuccess = ref('')
const isUpdatingPremiumPlan = ref(false)

const fullName = computed(() => {
  if (!currentUser.value) return 'Usuario'

  return `${currentUser.value.name} ${currentUser.value.surname}`.trim()
})

const userInitials = computed(() => {
  if (!currentUser.value) return 'U'

  return `${currentUser.value.name?.[0] || ''}${currentUser.value.surname?.[0] || ''}`.toUpperCase()
})

const subscriptionLabel = computed(() => {
  if (!currentUser.value?.subscription_type) return 'Standard'

  return currentUser.value.subscription_type === 'premium' ? 'Premium' : 'Standard'
})

const highestGlucoseRecord = computed(() => {
  if (glucoseRecords.value.length === 0) return null

  return glucoseRecords.value.reduce((highest, record) => {
    return record.glucose_value > highest.glucose_value ? record : highest
  })
})

const lowestGlucoseRecord = computed(() => {
  if (glucoseRecords.value.length === 0) return null

  return glucoseRecords.value.reduce((lowest, record) => {
    return record.glucose_value < lowest.glucose_value ? record : lowest
  })
})

const averageGlucoseValue = computed(() => {
  if (glucoseRecords.value.length === 0) return null

  const total = glucoseRecords.value.reduce((sum, record) => {
    return sum + record.glucose_value
  }, 0)

  return Math.round(total / glucoseRecords.value.length)
})

function formatDate(dateString) {
  if (!dateString) return 'No disponible'

  return new Date(dateString).toLocaleDateString('es-ES')
}

function formatMemberSince(dateString) {
  if (!dateString) return 'No disponible'

  return new Date(dateString).toLocaleDateString('es-ES', {
    month: 'long',
    year: 'numeric',
  })
}

function goToSettings() {
  router.push('/settings')
}

function openProfileModal(mode) {
  profileModalMode.value = mode
  profileModalError.value = ''
  profileModalSuccess.value = ''
  isProfileModalOpen.value = true
}

function closeProfileModal() {
  isProfileModalOpen.value = false
  profileModalError.value = ''
  profileModalSuccess.value = ''
  isSubmittingProfileModal.value = false
}

function openPremiumModal() {
  premiumError.value = ''
  premiumSuccess.value = ''
  showPremiumModal.value = true
}

function closePremiumModal() {
  if (isUpdatingPremiumPlan.value) return

  showPremiumModal.value = false
  premiumError.value = ''
  premiumSuccess.value = ''
}

async function handleSubmitProfileModal(formData) {
  isSubmittingProfileModal.value = true
  profileModalError.value = ''
  profileModalSuccess.value = ''

  try {
    if (profileModalMode.value === 'edit-profile') {
      const updatedUser = await updateCurrentUser(formData)
      setCurrentUser(updatedUser)
      profileModalSuccess.value = 'Perfil actualizado correctamente.'
    } else {
      await changePassword(formData)
      profileModalSuccess.value = 'Contraseña actualizada correctamente.'
    }

    setTimeout(() => {
      isProfileModalOpen.value = false
      profileModalSuccess.value = ''
    }, 1500)
  } catch (error) {
    if (handleAuthError(error, router)) {
      profileModalError.value = 'Tu sesión ha caducado. Te redirigimos al inicio de sesión.'
      return
    }

    profileModalError.value = error.message || 'No se pudo completar la operación.'
  } finally {
    isSubmittingProfileModal.value = false
  }
}
async function loadProfileGlucoseRecords() {
  isLoadingGlucoseRecords.value = true
  glucoseRecordsError.value = ''

  try {
    glucoseRecords.value = await getGlucoseRecords()
  } catch (error) {
    if (handleAuthError(error, router)) {
      glucoseRecordsError.value = 'Tu sesión ha caducado. Te redirigimos al inicio de sesión.'
      return
    }

    glucoseRecordsError.value = error.message || 'No se pudo cargar el resumen de glucemias.'
  } finally {
    isLoadingGlucoseRecords.value = false
  }
}

loadProfileGlucoseRecords()

async function handlePremiumPlanChange(newPlan) {
  if (!currentUser.value) return

  isUpdatingPremiumPlan.value = true
  premiumError.value = ''
  premiumSuccess.value = ''

  try {
    const updatedUser = await updateCurrentUser({
      name: currentUser.value.name,
      surname: currentUser.value.surname,
      date_of_birth: currentUser.value.date_of_birth,
      subscription_type: newPlan,
    })

    setCurrentUser(updatedUser)
    premiumSuccess.value = `Plan actualizado a ${newPlan === 'premium' ? 'Premium' : 'Standard'} correctamente.`

    setTimeout(() => {
      showPremiumModal.value = false
      premiumSuccess.value = ''
    }, 1500)
  } catch (error) {
    if (handleAuthError(error, router)) {
      premiumError.value = 'Tu sesión ha caducado. Te redirigimos al inicio de sesión.'
      return
    }

    premiumError.value = error.message || 'No se pudo actualizar el plan de cuenta.'
  } finally {
    isUpdatingPremiumPlan.value = false
  }
}
</script>

<template>
  <AppPrivateStart
    title="consulta y gestiona tu información personal"
    main="Mi perfil"
    variant="inactive"
  />

  <section class="profile-main-flex" :aria-busy="isCurrentUserLoading && !currentUser">
    <div
      v-if="isCurrentUserLoading && !currentUser"
      class="profile-state"
      role="status"
      aria-live="polite"
    >
      Cargando perfil...
    </div>

    <div
      v-else-if="currentUserError && !currentUser"
      class="profile-state profile-state-error"
      role="alert"
    >
      {{ currentUserError }}
    </div>

    <template v-else-if="currentUser">
      <section class="profile-user-grid">
        <div class="profile-user-logo">
          {{ userInitials }}
        </div>

        <div class="profile-user-resume-flex">
          <h3>{{ fullName }}</h3>
          <h4>{{ currentUser?.email }}</h4>

          <strong class="user-subsctiprion-badge">
            <StarIcon />
            {{ subscriptionLabel }}
          </strong>

          <div class="member-since-wrap">
            <ScheduleIcon />
            <h4>Miembro desde {{ formatMemberSince(currentUser?.created_at) }}</h4>
          </div>
        </div>

        <button type="button" class="edit-user" @click="openProfileModal('edit-profile')">
          <PencilIcon />
          Editar perfil
        </button>
      </section>

      <section class="profile-details-grid" :aria-busy="isLoadingGlucoseRecords">
        <article class="profile-extended-info-flex">
          <div class="info-flex info-head">
            <div class="info-icon"><PeopleIcon /></div>
            <h3>Información personal</h3>
          </div>

          <div class="info-flex">
            <div class="info-label">
              <div class="info-icon-mini"><PeopleIcon /></div>
              <h3>Nombre</h3>
            </div>
            <strong>{{ currentUser?.name }}</strong>
          </div>

          <div class="info-flex">
            <div class="info-label">
              <div class="info-icon-mini"><PeopleIcon /></div>
              <h3>Apellidos</h3>
            </div>
            <strong>{{ currentUser?.surname }}</strong>
          </div>

          <div class="info-flex">
            <div class="info-label">
              <div class="info-icon-mini"><MailIcon /></div>
              <h3>Correo electrónico</h3>
            </div>
            <strong>{{ currentUser?.email }}</strong>
          </div>

          <div class="info-flex">
            <div class="info-label">
              <div class="info-icon-mini"><ScheduleIcon /></div>
              <h3>Fecha de nacimiento</h3>
            </div>
            <strong>{{ formatDate(currentUser?.date_of_birth) }}</strong>
          </div>

          <div class="info-flex-badge">
            <div class="info-label">
              <div class="info-icon-mini"><SecurityIcon /></div>
              <h3>Tipo de cuenta</h3>
            </div>

            <strong class="badge">
              <StarIcon />
              {{ subscriptionLabel }}
            </strong>
          </div>
        </article>

        <article class="profile-actions">
          <div class="actions-head-flex">
            <div class="actions-mini-icon"><SecurityIcon /></div>
            <h3>Seguridad y cuenta</h3>
          </div>

          <button type="button" class="actions-flex" @click="openProfileModal('change-password')">
            <div class="action-icon"><LockerIcon /></div>

            <div class="action-text">
              <strong>Cambiar contraseña</strong>
              <span>Actualiza tu contraseña periódicamente para mantener tu cuenta segura.</span>
            </div>

            <span class="actions-arrow">›</span>
          </button>

          <button type="button" class="actions-flex" @click="goToSettings">
            <div class="action-icon"><ConfigIcon /></div>

            <div class="action-text">
              <strong>Configuración de la cuenta</strong>
              <span>Revisa y gestiona tus preferencias principales.</span>
            </div>

            <span class="actions-arrow">›</span>
          </button>
          <button type="button" class="actions-flex actions-flex-premium" @click="openPremiumModal">
            <div class="action-icon"><StarIcon /></div>

            <div class="action-text">
              <strong>Plan de cuenta</strong>
              <span>Gestiona tu plan Standard o Premium y el acceso a tu historial.</span>
            </div>

            <span class="actions-arrow">›</span>
          </button>
        </article>

        <div v-if="isLoadingGlucoseRecords" class="profile-state" role="status" aria-live="polite">
          Cargando resumen de glucemias...
        </div>

        <div v-else-if="glucoseRecordsError" class="profile-state profile-state-error" role="alert">
          {{ glucoseRecordsError }}
        </div>

        <GlucoseHealthSummary
          v-else
          title="Resumen de tu salud"
          variant="compact"
          :highest-record="highestGlucoseRecord"
          :lowest-record="lowestGlucoseRecord"
          :average-value="averageGlucoseValue"
        />
      </section>

      <section class="preferences-flex">
        <strong class="preferences-heading">
          <ConfigIcon />
          Preferencias del usuario
        </strong>

        <article class="preferences-actions-row">
          <button type="button" class="preferences-actions-flex" @click="goToSettings">
            <div class="preferences-action-icon"><EyeUpIcon /></div>

            <div class="preferences-action-text">
              <strong>Preferencias visuales</strong>
              <span>Configura la forma en la que ves la aplicación.</span>
            </div>

            <span class="preferences-actions-arrow">›</span>
          </button>
        </article>
      </section>
    </template>
  </section>
  <ProfileModal
    v-if="isProfileModalOpen"
    :mode="profileModalMode"
    :current-user="currentUser"
    :error-message="profileModalError"
    :success-message="profileModalSuccess"
    :is-submitting="isSubmittingProfileModal"
    @submit="handleSubmitProfileModal"
    @cancel="closeProfileModal"
  />
  <PremiumPlanForm
    v-if="showPremiumModal"
    :current-user="currentUser"
    :is-submitting="isUpdatingPremiumPlan"
    :error-message="premiumError"
    :success-message="premiumSuccess"
    @cancel="closePremiumModal"
    @confirm-plan-change="handlePremiumPlanChange"
  />
</template>

<style scoped>
.profile-main-flex {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.profile-state {
  padding: 2rem;
  border: 1px solid var(--color-border);
  border-radius: 1rem;
  background-color: var(--color-bg);
  color: var(--color-text-muted);
  text-align: center;
}

.profile-state-error {
  color: var(--color-danger);
}

.profile-user-grid {
  display: grid;
  grid-template-columns: auto 1fr auto;
  align-items: center;
  gap: 2rem;
  padding: 2rem;
  border: 1px solid var(--color-border);
  border-radius: 1rem;
  background-color: var(--color-bg);
  box-shadow: var(--shadow-soft);
}

.profile-user-logo {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 7rem;
  height: 7rem;
  border-radius: 50%;
  background-color: var(--color-bg);
  color: var(--color-primary);
  font-size: 2rem;
  font-weight: 800;
}

.profile-user-resume-flex {
  display: flex;
  flex-direction: column;
  gap: 0.45rem;
}

.profile-user-resume-flex h3,
.profile-user-resume-flex h4 {
  margin: 0;
}

.profile-user-resume-flex h3 {
  color: var(--color-text);
  font-size: 1.7rem;
}

.profile-user-resume-flex h4 {
  color: var(--color-text-muted);
  font-size: 0.95rem;
  font-weight: 500;
}

.user-subsctiprion-badge,
.badge {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  width: fit-content;
  padding: 0.45rem 0.75rem;
  border-radius: 999px;
  background-color: var(--color-surface);
  color: var(--color-primary);
  font-size: 0.9rem;
}
.user-subsctiprion-badge svg {
  width: 1.45rem;
  height: 1.45rem;
}

.member-since-wrap {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--color-text-muted);
}

.edit-user {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.85rem 1.4rem;
  border: none;
  border-radius: 0.65rem;
  background-color: var(--color-primary);
  color: var(--color-bg);
  font-weight: 700;
  cursor: pointer;
}
.edit-user svg {
  color: var(--color-bg);
  width: 1.55rem;
  height: 1.55rem;
}

.profile-details-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
}

.profile-extended-info-flex,
.profile-actions,
.preferences-flex {
  display: flex;
  flex-direction: column;
  gap: 1.1rem;
  padding: 1.5rem;
  border: 1px solid var(--color-border);
  border-radius: 1rem;
  background-color: var(--color-bg);
  box-shadow: var(--shadow-soft);
}

.info-flex,
.info-flex-badge {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--color-border);
}

.info-flex:last-child,
.info-flex-badge:last-child {
  padding-bottom: 0;
  border-bottom: none;
}

.info-head,
.actions-head-flex,
.preferences-heading {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--color-border);
  justify-content: flex-start;
}
.info-flex.info-head h3,
.actions-head-flex h3,
.preferences-heading {
  margin: 0;
  color: var(--color-text);
  font-size: 1.25rem;
  font-weight: 800;
  line-height: 1.2;
}

.info-label {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.info-flex h3,
.info-flex-badge h3 {
  margin: 0;
  color: var(--color-text);
  font-size: 0.95rem;
}

.info-flex strong {
  color: var(--color-text-muted);
  font-size: 0.9rem;
}

.info-icon,
.actions-mini-icon,
.preferences-action-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 3rem;
  height: 3rem;
  border-radius: 50%;
  background-color: var(--color-surface);
  color: var(--color-primary);
}
.info-icon svg,
.actions-mini-icon svg {
  width: 1.45rem;
  height: 1.45rem;
}

.info-icon-mini {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 1.8rem;
  height: 1.8rem;
  flex-shrink: 0;
  color: var(--color-text-muted);
}
.info-icon-mini svg {
  width: 1.35rem;
  height: 1.35rem;
}

.actions-flex {
  display: flex;
  align-items: center;
  gap: 1rem;
  width: 100%;
  padding: 1rem 0;
  border: none;
  border-bottom: 1px solid var(--color-border);
  background: transparent;
  text-align: left;
  cursor: pointer;
}

.actions-flex:last-child {
  border-bottom: none;
}

.action-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 3rem;
  height: 3rem;
  flex-shrink: 0;
  border-radius: 50%;
  background-color: var(--color-bg);
  color: var(--color-primary);
}

.action-text {
  display: flex;
  flex: 1;
  flex-direction: column;
  gap: 0.25rem;
}

.action-text strong,
.preferences-action-text strong {
  color: var(--color-text);
  font-size: 0.95rem;
}

.action-text span,
.preferences-action-text span {
  color: var(--color-text-muted);
  font-size: 0.82rem;
  line-height: 1.4;
}

.actions-arrow,
.preferences-actions-arrow {
  color: var(--color-text-muted);
  font-size: 1.7rem;
}

.preferences-actions-row {
  display: flex;
  gap: 1.5rem;
}

.preferences-actions-flex {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex: 1;
  padding: 0;
  border: none;
  background: transparent;
  text-align: left;
  cursor: pointer;
}

.preferences-action-text {
  display: flex;
  flex: 1;
  flex-direction: column;
  gap: 0.25rem;
}
.actions-flex-premium {
  position: relative;

  margin-top: 1rem;
  padding: 1.5rem 1.4rem;

  border-radius: 1.2rem;
  background-color: var(--dashboard-blue-bg);
  box-shadow: none;
}

.actions-flex-premium::after {
  display: none;
}

.actions-flex-premium .action-icon {
  background-color: var(--color-primary);
  color: var(--color-bg);
}

.actions-flex-premium strong {
  color: var(--color-primary);
}
@media (min-width: 820px) and (max-width: 1025px) and (orientation: portrait) {
  .profile-user-grid,
  .profile-details-grid,
  .preferences-actions-row {
    grid-template-columns: 1fr;
  }

  .profile-user-grid {
    gap: 1.35rem;
    padding: 1.5rem 1.75rem;
    justify-items: center;
    text-align: center;
  }

  .profile-user-logo {
    width: 5.5rem;
    height: 5.5rem;
    font-size: 2.35rem;
  }

  .profile-user-resume-flex,
  .member-since-wrap {
    align-items: center;
  }

  .profile-user-resume-flex {
    gap: 0.3rem;
  }

  .profile-details-grid {
    display: grid;
  }

  .preferences-actions-row {
    display: flex;
    flex-direction: column;
  }
  .profile-user-resume-flex h3 {
    font-size: 2.15rem;
    line-height: 1.1;
  }

  .profile-user-resume-flex h4,
  .member-since-wrap h4 {
    font-size: 1.2rem;
  }

  .user-subsctiprion-badge {
    gap: 0.5rem;
    padding: 0.5rem 0.85rem;
    font-size: 1.18rem;
  }

  .user-subsctiprion-badge svg {
    width: 1.3rem;
    height: 1.3rem;
  }

  .member-since-wrap {
    gap: 0.65rem;
  }

  .member-since-wrap svg {
    width: 1.15rem;
    height: 1.15rem;
    flex-shrink: 0;
  }

  .edit-user {
    margin-top: 0.2rem;
    padding: 0.8rem 1.25rem;
    font-size: 1rem;
  }

  .edit-user svg {
    width: 1.35rem;
    height: 1.35rem;
  }
  .info-flex.info-head h3,
  .actions-head-flex h3,
  .preferences-heading {
    font-size: 1.6rem;
  }
  .info-flex h3,
  .info-flex-badge h3 {
    font-size: 1.5rem;
  }

  .info-flex strong {
    min-width: 0;
    max-width: 48%;
    text-align: right;
    overflow-wrap: anywhere;
    font-size: 1.5rem;
  }
  .action-text strong,
  .preferences-action-text strong {
    font-size: 1.5rem;
  }

  .action-text span,
  .preferences-action-text span {
    font-size: 1.5rem;
  }
}

@media (max-width: 768px) {
  .profile-main-flex {
    gap: 1.25rem;
  }

  .profile-user-grid {
    grid-template-columns: 1fr;
    gap: 1.25rem;
    padding: 1.5rem;
    justify-items: center;
    text-align: center;
  }

  .profile-user-logo {
    width: 5rem;
    height: 5rem;
    font-size: 2rem;
  }

  .profile-user-resume-flex,
  .member-since-wrap {
    align-items: center;
  }

  .profile-user-resume-flex {
    gap: 0.35rem;
  }

  .profile-user-resume-flex h3 {
    font-size: 2rem;
    line-height: 1.1;
  }

  .profile-user-resume-flex h4,
  .member-since-wrap h4 {
    font-size: 1.05rem;
  }

  .profile-user-resume-flex h4 {
    max-width: 100%;
    overflow-wrap: anywhere;
  }

  .user-subsctiprion-badge {
    font-size: 1rem;
  }

  .edit-user {
    min-height: 3rem;
    padding: 0.8rem 1.25rem;
    font-size: 1rem;
  }

  .profile-details-grid {
    grid-template-columns: 1fr;
  }

  .profile-extended-info-flex,
  .profile-actions,
  .preferences-flex {
    gap: 1rem;
    padding: 1.25rem;
  }

  .info-flex.info-head h3,
  .actions-head-flex h3,
  .preferences-heading {
    font-size: 1.35rem;
  }

  .info-flex,
  .info-flex-badge {
    align-items: flex-start;
    flex-direction: column;
    gap: 0.55rem;
  }

  .info-label {
    align-items: center;
  }

  .info-flex h3,
  .info-flex-badge h3 {
    font-size: 1.1rem;
  }

  .info-flex strong {
    max-width: 100%;
    overflow-wrap: anywhere;
    color: var(--color-text-muted);
    font-size: 1.18rem;
    text-align: left;
  }

  .actions-flex,
  .preferences-actions-flex {
    gap: 0.85rem;
  }

  .action-text strong,
  .preferences-action-text strong {
    font-size: 1.1rem;
  }

  .action-text span,
  .preferences-action-text span {
    font-size: 1rem;
    line-height: 1.35;
  }

  .preferences-actions-row {
    flex-direction: column;
  }
}

@media (max-width: 950px) and (max-height: 520px) and (orientation: landscape) {
  .profile-main-flex {
    gap: 1rem;
  }

  .profile-user-grid {
    gap: 1rem;
    padding: 1rem 1.25rem;
  }

  .profile-user-logo {
    width: 4.5rem;
    height: 4.5rem;
    font-size: 1.8rem;
  }

  .profile-user-resume-flex {
    gap: 0.25rem;
  }

  .profile-user-resume-flex h3 {
    font-size: 1.35rem;
    line-height: 1.15;
  }

  .profile-user-resume-flex h4,
  .member-since-wrap h4 {
    font-size: 0.86rem;
  }

  .user-subsctiprion-badge {
    padding: 0.3rem 0.65rem;
    font-size: 0.82rem;
  }

  .user-subsctiprion-badge svg {
    width: 1.15rem;
    height: 1.15rem;
  }

  .edit-user {
    padding: 0.65rem 1rem;
    font-size: 0.9rem;
  }

  .profile-details-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .profile-extended-info-flex,
  .profile-actions,
  .preferences-flex {
    gap: 0.85rem;
    padding: 1rem;
  }

  .info-head,
  .actions-head-flex,
  .preferences-heading {
    padding-bottom: 0.75rem;
  }

  .info-flex.info-head h3,
  .actions-head-flex h3,
  .preferences-heading {
    font-size: 1.15rem;
  }

  .info-flex,
  .info-flex-badge {
    gap: 0.8rem;
    padding-bottom: 0.8rem;
  }

  .info-flex h3,
  .info-flex-badge h3,
  .action-text strong,
  .preferences-action-text strong {
    font-size: 0.9rem;
  }

  .info-flex strong,
  .action-text span,
  .preferences-action-text span {
    font-size: 0.82rem;
    line-height: 1.3;
  }

  .actions-flex {
    padding: 0.8rem 0;
  }

  .actions-flex-premium {
    margin-top: 0.5rem;
    padding: 1rem;
  }

  .preferences-actions-row {
    gap: 1rem;
  }
}
</style>

import { ref } from 'vue'

import { getCurrentUser } from '@/services/userService'

const currentUser = ref(null)
const isCurrentUserLoading = ref(false)
const currentUserError = ref('')

let loadedToken = null
let pendingRequest = null

async function loadCurrentUser(options = {}) {
  const { force = false } = options
  const token = localStorage.getItem('access_token')

  if (!token) {
    clearCurrentUser()
    return null
  }

  if (pendingRequest && loadedToken === token) {
    return pendingRequest
  }

  if (!force && currentUser.value && loadedToken === token) {
    return currentUser.value
  }

  loadedToken = token
  isCurrentUserLoading.value = true
  currentUserError.value = ''

  const request = getCurrentUser()
  pendingRequest = request

  try {
    const user = await request

    if (localStorage.getItem('access_token') === token) {
      currentUser.value = user
    }

    return user
  } catch (error) {
    if (localStorage.getItem('access_token') === token) {
      currentUser.value = null
      currentUserError.value = error.message || 'No se ha podido obtener el usuario'
    }

    throw error
  } finally {
    if (pendingRequest === request) {
      pendingRequest = null
      isCurrentUserLoading.value = false
    }
  }
}

function setCurrentUser(user) {
  currentUser.value = user
  loadedToken = localStorage.getItem('access_token')
  currentUserError.value = ''
}

function clearCurrentUser() {
  currentUser.value = null
  isCurrentUserLoading.value = false
  currentUserError.value = ''
  loadedToken = null
  pendingRequest = null
}

export function useCurrentUser() {
  return {
    currentUser,
    isCurrentUserLoading,
    currentUserError,
    loadCurrentUser,
    setCurrentUser,
    clearCurrentUser,
  }
}

import { useCurrentUser } from '@/composables/useCurrentUser'

export function handleAuthError(error, router) {
  if (error.status === 401) {
    const { clearCurrentUser } = useCurrentUser()

    localStorage.removeItem('access_token')
    clearCurrentUser()

    setTimeout(() => {
      router.push('/login')
    }, 2000)

    return true
  }

  return false
}

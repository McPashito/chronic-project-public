export function handleAuthError(error, router) {
  if (error.status === 401) {
    localStorage.removeItem('access_token')

    setTimeout(() => {
      router.push('/login')
    }, 2000)

    return true
  }

  return false
}

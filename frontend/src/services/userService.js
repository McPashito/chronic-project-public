import { API_BASE_URL } from '@/config/api'
import { createApiError } from '@/utils/apiErrors'
import Http from './user'

export async function getCurrentUser() {
  const http = new Http(null, null, 'users/me')

  try {
    const data = await http.get()
    return data
  } catch (error) {
    throw error
  }
}
export async function updateCurrentUser(userData) {
  const token = localStorage.getItem('access_token')

  const respuesta = await fetch(`${API_BASE_URL}/users/edit_user`, {
    method: 'PUT',
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(userData),
  })

  const data = await respuesta.json()

  if (!respuesta.ok) {
    throw createApiError(data, 'No se ha podido editar el perfil', respuesta.status)
  }

  return data
}

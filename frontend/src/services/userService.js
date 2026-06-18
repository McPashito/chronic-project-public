import { API_BASE_URL } from '@/config/api'

export async function getCurrentUser() {
  const token = localStorage.getItem('access_token')

  const respuesta = await fetch(`${API_BASE_URL}/users/me`, {
    method: 'GET',
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })

  const data = await respuesta.json()

  if (!respuesta.ok) {
    const error = new Error(data.detail || 'No se ha podido obtener el usuario')
    error.status = respuesta.status
    throw error
  }

  return data
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
    const error = new Error(data.detail || 'No se ha podido editar el perfil')
    error.status = respuesta.status
    throw error
  }

  return data
}

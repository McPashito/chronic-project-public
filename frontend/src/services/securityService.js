import { API_BASE_URL } from '@/config/api'
import { createApiError } from '@/utils/apiErrors'

export async function changePassword(passwordData) {
  const token = localStorage.getItem('access_token')

  const respuesta = await fetch(`${API_BASE_URL}/users/change_password`, {
    method: 'PUT',
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(passwordData),
  })

  const data = await respuesta.json()

  if (!respuesta.ok) {
    throw createApiError(data, 'No se ha podido cambiar la contraseña', respuesta.status)
  }

  return data
}

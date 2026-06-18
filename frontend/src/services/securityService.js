import { API_BASE_URL } from '@/config/api'

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
    const error = new Error(data.detail || 'No se ha podido cambiar la contraseña')
    error.status = respuesta.status
    throw error
  }

  return data
}

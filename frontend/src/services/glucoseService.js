import { API_BASE_URL } from '@/config/api'
import { createApiError } from '@/utils/apiErrors'

export async function getSummary(startDate, endDate) {
  const token = localStorage.getItem('access_token')

  const respuesta = await fetch(
    `${API_BASE_URL}/glucose-records/summary?start_date=${startDate}&end_date=${endDate}`,
    {
      method: 'GET',
      headers: {
        Authorization: `Bearer ${token}`,
      },
    },
  )

  const data = await respuesta.json()

  if (!respuesta.ok) {
    throw createApiError(data, 'No se ha podido obtener el resumen de glucemias', respuesta.status)
  }

  return data
}

export async function getGlucoseRecords(startDate, endDate, momentOfDay) {
  const token = localStorage.getItem('access_token')

  const params = new URLSearchParams()

  if (startDate) params.append('start_date', startDate)
  if (endDate) params.append('end_date', endDate)
  if (momentOfDay) params.append('moment_of_day', momentOfDay)

  const respuesta = await fetch(`${API_BASE_URL}/glucose-records/?${params.toString()}`, {
    method: 'GET',
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })

  const data = await respuesta.json()

  if (!respuesta.ok) {
    throw createApiError(data, 'No se han podido obtener las glucemias', respuesta.status)
  }

  return data
}

export async function deleteGlucoseRecord(recordId) {
  const token = localStorage.getItem('access_token')

  const respuesta = await fetch(`${API_BASE_URL}/glucose-records/${recordId}`, {
    method: 'DELETE',
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })

  const data = await respuesta.json()

  if (!respuesta.ok) {
    throw createApiError(data, 'No se ha podido borrar la glucemia', respuesta.status)
  }

  return data
}

export async function updateGlucoseRecord(recordId, recordData) {
  const token = localStorage.getItem('access_token')

  const respuesta = await fetch(`${API_BASE_URL}/glucose-records/${recordId}`, {
    method: 'PUT',
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(recordData),
  })

  const data = await respuesta.json()

  if (!respuesta.ok) {
    throw createApiError(data, 'No se ha podido editar la glucemia', respuesta.status)
  }

  return data
}

export async function createGlucoseRecord(recordData) {
  const token = localStorage.getItem('access_token')

  const respuesta = await fetch(`${API_BASE_URL}/glucose-records/`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(recordData),
  })

  const data = await respuesta.json()

  if (!respuesta.ok) {
    throw createApiError(data, 'No se ha podido crear la glucemia', respuesta.status)
  }

  return data
}

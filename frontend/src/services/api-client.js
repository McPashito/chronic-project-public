import { API_BASE_URL } from '@/config/api'
import { createApiError } from '@/utils/apiErrors'

function buildHeaders() {
  const token = localStorage.getItem('access_token')

  return {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  }
}

function buildQuery(params) {
  if (!params) return ''

  const search = new URLSearchParams()

  for (const [key, value] of Object.entries(params)) {
    if (value !== undefined && value !== null && value !== '') {
      search.append(key, value)
    }
  }

  const query = search.toString()

  return query ? `?${query}` : ''
}

class ApiClient {
  constructor(baseUrl = API_BASE_URL) {
    this.baseUrl = baseUrl
  }

  async request(endpoint, method, body, options = {}) {
    if (!this.baseUrl) {
      throw new Error('La URL base de la API no está configurada (VITE_API_BASE_URL).')
    }

    let response

    try {
      response = await fetch(`${this.baseUrl}/${endpoint}`, {
        method,
        headers: buildHeaders(),
        signal: options.signal,
        ...(body !== undefined ? { body: JSON.stringify(body) } : {}),
      })
    } catch (error) {
      if (error.name === 'AbortError') throw error
      throw createApiError(null, 'No se ha podido conectar con el servidor.', 0)
    }

    if (response.status === 204) {
      return null
    }

    const data = await response.json().catch(() => null)

    if (!response.ok) {
      throw createApiError(data, 'No se ha podido completar la solicitud', response.status)
    }

    return data
  }

  get(endpoint, params, options) {
    return this.request(`${endpoint}${buildQuery(params)}`, 'GET', undefined, options)
  }

  post(endpoint, body, options) {
    return this.request(endpoint, 'POST', body, options)
  }

  put(endpoint, body, options) {
    return this.request(endpoint, 'PUT', body, options)
  }

  delete(endpoint, body, options) {
    return this.request(endpoint, 'DELETE', body, options)
  }
}

// Instancia única compartida en todo el proyecto (singleton de módulo).
export const api = new ApiClient()

export default api

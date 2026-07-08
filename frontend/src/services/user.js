import { API_BASE_URL, HEADERS } from '@/config/api'

class Http {
  constructor(baseUrl, headers, endpoint) {
    this.baseUrl = baseUrl ?? API_BASE_URL
    this.headers = headers ?? HEADERS
    this.url = `${this.baseUrl}/${endpoint}`
  }

  get() {
    try {
      const response = fetch(this.url, {
        method: 'GET',
        headers: this.headers,
      })
      return response
    } catch (error) {
      throw error
    }
  }

  post(body) {
    try {
      const response = fetch(this.url, {
        method: 'POST',
        headers: this.headers,
        body: JSON.stringify(body),
      })
      return response
    } catch (error) {
      throw error
    }
  }

  put(body) {
    try {
      const response = fetch(this.url, {
        method: 'PUT',
        headers: this.headers,
        body: JSON.stringify(body),
      })
      return response
    } catch (error) {
      throw error
    }
  }

  delete(body) {
    try {
      const response = fetch(this.url, {
        method: 'DELETE',
        headers: this.headers,
        body: JSON.stringify(body),
      })
      return response
    } catch (error) {
      throw error
    }
  }
}

export default Http

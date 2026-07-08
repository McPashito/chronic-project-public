export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL

export const ACCESS_TOKEN = localStorage.getItem('access_token')

export const HEADERS = {
  'Content-Type': 'application/json',
  Authorization: `Bearer ${ACCESS_TOKEN}`,
}

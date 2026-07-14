import { api } from './api-client'

export async function getCurrentUser() {
  return api.get('users/me')
}

export async function updateCurrentUser(userData) {
  return api.put('users/edit_user', userData)
}

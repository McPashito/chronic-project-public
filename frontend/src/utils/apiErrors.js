const FIELD_LABELS = {
  date: 'Fecha',
  date_of_birth: 'Fecha de nacimiento',
  email: 'Correo electrónico',
  glucose_value: 'Valor de glucemia',
  moment_of_day: 'Momento del día',
  name: 'Nombre',
  new_password: 'Nueva contraseña',
  notes: 'Notas',
  old_password: 'Contraseña actual',
  password: 'Contraseña',
  surname: 'Apellidos',
  time: 'Hora',
}

function getFieldLabel(location) {
  if (!Array.isArray(location)) return null

  const fieldName = [...location].reverse().find((item) => typeof item === 'string')

  if (!fieldName || fieldName === 'body' || fieldName === 'query' || fieldName === 'path') {
    return null
  }

  return FIELD_LABELS[fieldName] || fieldName.replaceAll('_', ' ')
}

function cleanMessage(message) {
  if (!message) return ''

  return String(message).replace(/^Value error,\s*/i, '').trim()
}

function formatValidationIssue(issue) {
  const fieldLabel = getFieldLabel(issue.loc)
  const context = issue.ctx || {}
  const originalMessage = cleanMessage(issue.msg)

  let message = originalMessage

  if (issue.type === 'missing') {
    message = 'es obligatorio.'
  } else if (issue.type === 'string_too_short') {
    message = `debe tener al menos ${context.min_length} caracteres.`
  } else if (issue.type === 'string_too_long') {
    message = `debe tener como máximo ${context.max_length} caracteres.`
  } else if (issue.type === 'greater_than_equal') {
    message = `debe ser mayor o igual que ${context.ge}.`
  } else if (issue.type === 'less_than_equal') {
    message = `debe ser menor o igual que ${context.le}.`
  } else if (issue.type === 'literal_error') {
    message = 'tiene un valor no permitido.'
  } else if (issue.type?.includes('date')) {
    message = originalMessage || 'debe tener una fecha válida.'
  } else if (issue.type?.includes('time')) {
    message = originalMessage || 'debe tener una hora válida.'
  } else if (issue.type?.includes('int')) {
    message = originalMessage || 'debe ser un número válido.'
  }

  if (!message) {
    message = 'no tiene un valor válido.'
  }

  if (!fieldLabel) {
    return message
  }

  return `${fieldLabel}: ${message}`
}

export function formatApiError(data, fallbackMessage) {
  const detail = data?.detail

  if (typeof detail === 'string') {
    return detail
  }

  if (Array.isArray(detail)) {
    return detail.map(formatValidationIssue).filter(Boolean).join(' ') || fallbackMessage
  }

  if (detail && typeof detail === 'object') {
    return cleanMessage(detail.msg) || fallbackMessage
  }

  return fallbackMessage
}

export function createApiError(data, fallbackMessage, status) {
  const error = new Error(formatApiError(data, fallbackMessage))
  error.status = status
  return error
}

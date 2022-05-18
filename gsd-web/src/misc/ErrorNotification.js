import { Notify } from 'quasar'

export function errorNotification(error, fallbackMessage) {
  let errorMessage = ''
  if (typeof error.response !== 'undefined') {
    errorMessage = error.response.data.error
  } else {
    errorMessage = `${fallbackMessage}: ${error.message}`
  }
  Notify.create({
    color: 'negative',
    position: 'top',
    message: errorMessage,
    icon: 'report_problem'
  })
}

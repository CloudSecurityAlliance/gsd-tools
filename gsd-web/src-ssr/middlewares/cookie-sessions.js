import cookieSession from 'cookie-session'
import cookieParser from 'cookie-parser'
import { ssrMiddleware } from 'quasar/wrappers'

export default ssrMiddleware(({ app }) => {
  app.use(cookieSession({
    name: 'gsdSession',
    secret: process.env.GSD_SESSION_KEY,
    maxAge: 1000 * 60 * 60 * 24 // 24 hours
  }))
  app.use(cookieParser())
})

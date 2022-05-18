import csrf from 'csurf'
import { ssrMiddleware } from 'quasar/wrappers'

export default ssrMiddleware(({ app }) => {
  app.use(csrf({ cookie: true }))
})

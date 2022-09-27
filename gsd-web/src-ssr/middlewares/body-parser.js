import bodyParser from 'body-parser'
import { ssrMiddleware } from 'quasar/wrappers'

export default ssrMiddleware(({ app }) => {
  app.use(bodyParser.json())
  app.use(bodyParser.urlencoded({ extended: false }))
})

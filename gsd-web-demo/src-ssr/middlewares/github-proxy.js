import axios from 'axios'
import { ssrMiddleware } from 'quasar/wrappers'

const githubClientID = process.env.GSD_GITHUB_KEY
const githubClientSecret = process.env.GSD_GITHUB_SECRET

export default ssrMiddleware(async ({ app, resolve }) => {
  app.get(resolve.urlPath('/oauth/callback/github'), async (req, res) => {
    try {
      const tokenBody = {
        client_id: githubClientID,
        client_secret: githubClientSecret,
        code: req.query.code
      }
      const tokenOpts = {
        headers: {
          accept: 'application/json'
        }
      }
      const tokenResponse = await axios.post(
        'https://github.com/login/oauth/access_token',
        tokenBody,
        tokenOpts
      )

      req.session.access_token = tokenResponse.data['access_token']

      const userOpts = {
        headers: {
          accept: 'application/json',
          authorization: `token ${req.session.access_token}`
        }
      }

      const userResponse = await axios.get(
        'https://api.github.com/user',
        userOpts
      )

      req.session.username = userResponse.data['login']

      res.redirect('/')
    } catch(error) {
      console.log(error)
      res.redirect('/')
    }
  })

  app.delete(resolve.urlPath('/logout'), (req, res) => {
    req.session = null
    res.json({ message: 'Session destroyed' })
  })
})

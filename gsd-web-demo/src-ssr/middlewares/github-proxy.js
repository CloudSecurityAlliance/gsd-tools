import axios from 'axios'
import { ssrMiddleware } from 'quasar/wrappers'

export default ssrMiddleware(({ app, resolve }) => {
  app.get(resolve.urlPath('/testing'), (req, res) => {
    axios.get('https://api.github.com/zen').then(
      (response) => {
        if(req.session.previous_zen === undefined) {
          req.session.previous_zen = 'No previous data'
        }
        console.log('Previous: ' + req.session.previous_zen)
        console.log('Current: ' + response.data)
        const page = 'Previous: ' + req.session.previous_zen + "<br>Current: " + response.data
        req.session.previous_zen = response.data
        res.send(page)
      },
      (error) => {
        res.send('Uh oh! Broke')
      }
    )
  })
})

import axios from 'axios'
import { ssrMiddleware } from 'quasar/wrappers'
import { Octokit } from 'octokit'

const githubClientID = process.env.GSD_GITHUB_KEY
const githubClientSecret = process.env.GSD_GITHUB_SECRET

async function createFork(octokit) {
  return await octokit.rest.forks.create({
    owner: 'cloudsecurityalliance',
    repo: 'gsd-database'
  })
}

async function createBranch(octokit) {
  // TODO: Allow multiple edits without overwriting existing edits
  const branchPrefix = `automated/${identifier}`
  const editNumber = 1
  const branchName = `${branchPrefix}/${editNumber}`
  // octokit.rest.branches.
}

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

  // FIXME: Seems like CSURF is doing literally nothing
  app.patch(resolve.urlPath('/update-gsd'), async (req, res) => {
    if(!req.session.access_token) {
      res.status(403).send('Login first!')
      return
    }

    try {
      const octokit = new Octokit({ auth: req.session.access_token });

      console.log(req.body)

      const identifier = req.body.identifier
      const fileContent = req.body.file_content

      const issueTitle = `Update Request - ${identifier}`
      const issueBody =
        '**Automated Edit Request**\n\n' +
        `For: "${identifier}"\n\n` +
        `\`\`\`json\n${fileContent}\n\`\`\``

      // await createFork(octokit)
      // await createBranch(octokit)
      // await updateFile(octokit)
      // await submitPullRequest(octokit)

      // FIXME: Labels don't appear to work via this method, perhaps have the bot auto add them?
      const response = await octokit.rest.issues.create({
        owner: 'cloudsecurityalliance',
        repo: 'gsd-database',
        title: issueTitle,
        body: issueBody
      })

      res.json({ redirect_url: response.data['html_url'] })
    } catch(error) {
      console.log(error)
      res.send('broke')
    }
  })
})

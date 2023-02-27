import axios from 'axios'
import { ssrMiddleware } from 'quasar/wrappers'
import { Octokit } from 'octokit'

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

      res.redirect('/home')
    } catch(error) {
      console.log(error)
      res.redirect('/home')
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

      // console.log(req.body)

      const identifier = req.body.identifier
      // Split navigation data from identifier
      const year = identifier.split('-')[1]
      const thousands = `${identifier.split('-')[2].slice(0, -3)}xxx`
      // Resolve file path
      const filePath = `${year}/${thousands}/${identifier}.json`

      // Other meta
      const title = `Update Request - ${identifier}`
      const fileContent = btoa(req.body.file_content)
      const username = req.session.username
      const branchName = `automated/${identifier}`
      const branchRef = `refs/heads/${branchName}`
      const branchHead = `${username}:${branchName}`

      const createForkResponse = await octokit.request('POST /repos/{owner}/{repo}/forks', {
        owner: 'cloudsecurityalliance',
        repo: 'gsd-database',
        name: 'gsd-database',
        default_branch_only: true
      })

      const syncForkResponse = await octokit.request('POST /repos/{owner}/{repo}/merge-upstream', {
        owner: username,
        repo: 'gsd-database',
        branch: 'main'
      })

      const getMainBranchResponse = await octokit.request('GET /repos/{owner}/{repo}/branches/{branch}', {
        owner: username,
        repo: 'gsd-database',
        branch: 'main'
      })

      const mainBranchSha = getMainBranchResponse.data['commit']['sha']

      try {
        const createBranchResponse = await octokit.request('POST /repos/{owner}/{repo}/git/refs', {
          owner: username,
          repo: 'gsd-database',
          ref: branchRef,
          sha: mainBranchSha
        })
      } catch(error) {
        console.log(error)
      }

      const existingContentResponse = await octokit.request('GET /repos/{owner}/{repo}/contents/{path}', {
        owner: username,
        repo: 'gsd-database',
        path: filePath,
        ref: branchRef
      })

      const contentSha = existingContentResponse.data['sha']

      const contentResponse = await octokit.request('PUT /repos/{owner}/{repo}/contents/{path}', {
        owner: username,
        repo: 'gsd-database',
        path: filePath,
        branch: branchName,
        message: title,
        content: fileContent,
        sha: contentSha
      })

      const existingPullResponse = await octokit.request('GET /repos/{owner}/{repo}/pulls', {
        owner: 'cloudsecurityalliance',
        repo: 'gsd-database',
        head: branchHead,
        base: 'main'
      })

      let redirectUrl = null
      const existingPullRequests = existingPullResponse.data

      if (Array.isArray(existingPullRequests) && existingPullRequests.length > 0) {
        redirectUrl = existingPullRequests[0]['html_url']
      } else {
        const pullResponse = await octokit.request('POST /repos/{owner}/{repo}/pulls', {
          owner: 'cloudsecurityalliance',
          repo: 'gsd-database',
          title: title,
          body: 'This pull request was created using https://data.gsd.id',
          head: branchHead,
          base: 'main',
          maintainer_can_modify: true
        })

        redirectUrl = pullResponse.data['html_url']
      }

      res.json({ redirect_url: redirectUrl })
    } catch(error) {
      console.log(error)
      res.send('broke')
    }
  })
})

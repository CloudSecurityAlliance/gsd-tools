# GSD request tools

# How to contribute
We have instructions in [CONTRIBUTING.md](https://github.com/cloudsecurityalliance/gsd-tools/blob/main/CONTRIBUTING.md) on how to work with git and submit a pull request.

# How to develop

You will need some environment variables to make this work

You must set these environment variables

**GH_TOKEN**
The token for authenticating against the GH_REPO. This is something you generate for yourself, there are instructions here
https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token

**GH_CLIENT_ID
GH_OAUTH_SECRET**
The two above get you from github after creating an OAuth application
Instructions to create this application can be found here
https://docs.github.com/en/developers/apps/creating-an-oauth-app
Your homepage URL can be http://localhost:3000 for local development.
The callback URL is http://localhost:3000/authcallback

**GIT_ASKPASS**
Only set this for your dev system, the containers will take care of this
for prod. You have to use the absolute path, for example on my system

export GIT_ASKPASS=/home/XXX/src/gsd-tools/gsd-bot/helpers/git-askpass.py

**GH_REPO**
The repo name in github. This is the repo the bot and web form will be working with
For example the prod repo is "cloudsecurityalliance/security-database"

**GH_USERNAME**
The username you will auth against github with

**SESSION_KEY**
This can be literally anything. It's the key used to encrypt the session
cookie.

## Docker

See [docker-compose README](docker-compose/README.md)

## webform

See [webform README](webform/README.md)

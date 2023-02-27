# GSD Web

- **Website:** https://data.gsd.id/
- **Depends on:** [GSD API][gsd-api-link], [GSD Schema][gsd-schema-link]

A web based user interface for the GSD data (gsd-database repo) allowing users to explore and edit the data. *** TODO ***

## How to use this tool

For the live version of this tool, please visit https://data.gsd.id/

To try the code locally, please see [Running Locally](#running-locally).

*** TODO ***

## How to contribute to this tool

You'll want to fork this repo, and clone the fork locally. To run the code locally and see your changes before committing them, see [Running Locally](#running-locally).

See also the [CONTRIBUTING.md](../CONTRIBUTING.md) file for further guidance.

## How to file an issue

*** CREATE TEMPLATE ***

## Issues and PR Labels for this tool

Please use "gsd-web-demo" as a label.

## Reference Documentation

For documentation on the other tools used to create this project, please see the following:

- [Quasar Framework](https://quasar.dev)
	- Which is based on [Vue 3](https://vuejs.org/guide/introduction.html) (we're using the composition API)
- [Github REST API](https://docs.github.com/en/rest/guides/getting-started-with-the-rest-api)
	- This is used for interacting with the GSD Database, which is hosted via a Github Repository.

## Tool Code Owner

@joshbuker

## Running Locally

This project uses the [Quasar Framework](https://quasar.dev). You may also want to use NVM for managing multiple node versions between different projects. This is purely for convenience however, and is not necessary to build or run the project. The Quasar CLI on the otherhand will be required to build and run the project.

### Installation

#### Dependencies

- Required:
	- [Quasar CLI](https://quasar.dev/start/quasar-cli)
	- Yarn
	- [Github OAuth App for localhost](#creating-your-github-oauth-app)
	- A unix system for development
		- e.g. Windows Subsystem for Linux, Mac OS X, Linux, etc.
- Optional:
	- [nvm](https://github.com/nvm-sh/nvm#installing-and-updating)

#### Creating your Github OAuth App

To be able to use the sign in functionality locally, you'll need to create a Github OAuth App.

1. First, if you don't already have a Github account, create one for free at https://github.com.
2. Once logged into your Github account, you'll want to go to the [Register a new OAuth application](https://github.com/settings/applications/new) page.
3. You should see something like the following: ![Register a new OAuth application](Register%20a%20new%20OAuth%20application.png)
4. Fill out the form with the following information, then click the **Register application** button.
	1. Application Name: `GSD Web Localhost`
	2. Homepage URL: `https://localhost:8080`
	3. Application description: _leave blank_
	4. Authorization Callback URL: `https://localhost:8080/oauth/callback/github`
	5. Enable Device Flow: _leave unchecked_
4. You'll want to have a safe place to store the client secret, which will only be shown to you once. Your password manager (e.g. [Lastpass](https://www.lastpass.com/), [1Password](https://1password.com/), or [BitWarden](https://bitwarden.com/)) would be an appropriate place.
5. Click the **Generate a new client secret** button.
6. Copy both the Client ID and Client Secret into a safe location like your password manager. *Once you leave this page, you will need to delete and regenerate your secret if you lose it!*
7. Done! You can now move onto the next step.

#### Setting the ENV variables

You'll need to save three ENV variables in your terminal profile so that the application can properly load.

Most commonly, the profile file will be a hidden dot file in your home directory, for example:

- `~/.bash_profile`
- `~/.profile`
- `~/.zprofile`

This will vary slightly depending on which operating system and terminal you are using.

Once you've located your profile file, add the following variables to it at the bottom:

> Be sure to replace the placeholders (e.g. `<any secure random string>`) with the actual value (e.g. `SomeSecureRandomString!@#$1234`). Note that the angle brackets `<>` are not included in the final result.

> Ensure that the file actually saves before continuing, the application will not render without these ENV variables present.

```bash
export GSD_SESSION_KEY='<any secure random string>'
export GSD_GITHUB_KEY='<your oauth app client id>'
export GSD_GITHUB_SECRET='<your oauth app client secret>'
```

If your terminal application was open, restart it to reload the profile file.

#### Commands

> You must run these commands within the project directory, as it will search for the `.nvmrc` file to decide what version of node to use when running `nvm install` and `nvm use`, as well as the `package.json` file when running `yarn` / `yarn install`.
>
> Replace `<path-to-repo>` with the path to the gsd-tools repo.

```bash
cd <path-to-repo>/gsd-web/
nvm install
nvm use
yarn install
```

### Running the server

> You may run into issues with hotloading when making changes to the SSR middleware. It may be necessary to stop and restart the dev server using `ctrl+c` and `yarn dev` respectively.

To start the server, use the following command:

```bash
yarn dev
```

The server can be stopped with `ctrl+c`.

### Troubleshooting

The server runs fine, but returns `Cannot GET /`: Make sure you properly setup the ENV variables, and restarted your terminal application to load the new profile.

In general, try ensuring your dependencies are up-to-date if encountering any issues.

For example, on a Debian based linux distro (e.g. Ubuntu):

```bash
sudo apt update && sudo apt upgrade
nvm use
yarn install
```

[gsd-api-link]: /gsd-api/ "REST API for interfacing with the GSD Database"
[gsd-schema-link]: /gsd-schema/  "The JSON schema of a GSD identifier"

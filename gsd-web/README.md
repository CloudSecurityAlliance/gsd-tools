# GSD Web

A web based user interface for the GSD data (gsd-database repo) allowing users to explore and edit the data. *** TODO ***

## How to use this tool

For the live version of this tool, please visit https://edit.globalsecuritydatabase.org

To try the code locally, please see [Running Locally](#running-locally).

*** TODO ***

## How to contribute to this tool

You'll want to fork this repo, and clone the fork locally. To run the code locally and see your changes before committing them, see [Running Locally](#running-locally).

See also the [CONTRIBUTING.md](../CONTRIBUTING.md) file for further guidance.

## How to file an issue

*** CREATE TEMPLATE ***

## Issues and PR Labels for this tool

Please use "gsd-web-demo" as a label.

## Tools Used

- [Quasar Framework](https://quasar.dev)
	- Which is based on [Vue 3](https://vuejs.org/guide/introduction.html) (we're using the composition API)
- [Github REST API](https://docs.github.com/en/rest/guides/getting-started-with-the-rest-api)
	- This is used for interacting with the GSD Database, which is hosted via a Github Repository.

## Running Locally

This project uses the [Quasar Framework](https://quasar.dev). You may also want to use NVM for managing multiple node versions between different projects. This is purely for convenience however, and is not necessary to build or run the project. The Quasar CLI on the otherhand will be required to build and run the project.

### Installation

#### Dependencies

- Required:
	- [Quasar CLI](https://quasar.dev/start/quasar-cli)
	- Yarn
- Optional:
	- [nvm](https://github.com/nvm-sh/nvm#installing-and-updating)

#### Commands

> [!info]+
> You must run these commands within the project directory, as it will search for the `.nvmrc` file to decide what version of node to use when running `nvm install` and `nvm use`, as well as the `package.json` file when running `yarn` / `yarn install`.
>
> Replace `<path-to-repo>` with the path to the gsd-tools repo.

```bash
cd <path-to-repo>/gsd-web/
nvm install
nvm use
yarn
```

### Running the server

> [!attention]+
> You may run into issues with hotloading when making changes to the SSR middleware. It may be necessary to stop and restart the dev server using `ctrl+c` and `yarn dev` respectively.

To start the server, use the following command:

```bash
yarn dev
```

The server can be stopped with `ctrl+c`.

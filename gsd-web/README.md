# GSD Web

Provides a web interface for viewing, searching, and editing the GSD Database.

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

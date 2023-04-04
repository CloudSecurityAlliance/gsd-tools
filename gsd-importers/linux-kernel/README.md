# GSD Bot

This bot will look for github GSD issue requests and approvals.

To run the container you have to set the environment variable GH_TOKEN. This
token will be used for REST and git access

- **Depends on:** _None_

## Usage

To retrieve your GitHub user ID, visit https://api.github.com/users/<GH_USERNAME>

You'll need to be added to the allowlist.json in your test repo, see: https://github.com/cloudsecurityalliance/gsd-database/blob/main/allowlist.json

### Using .devcontainer

1. Fork `gsd-database` for usage as a test repo
1. Copy `.env.sample` to `.env`: `cp .env.sample .env`
1. Update `.env` to contain the relevant env variables:
    1. `GH_TOKEN`: The Personal Access Token with write access to your test repo
    1. `GH_REPO`: The test repo to create your commit with
    1. `GH_USERNAME`: Your GitHub username
    1. `GH_USER_ID`: Your GitHub user ID
1. Create `kernel-request.txt` with the latest values from Kernel devs
    1. `kernel-request.txt` is a plaintext file containing a list from the Kernel folks, can live anywhere as long as you can pipe it into the script. Ask @joshbressers if you have questions
1. Clone `https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git` to `~/Repos/csa/linux`
    1. TODO: Make this adjustable, see `.devcontainer/devcontainer.json` mounts definition
1. Rebuild & Reopen in Container
1. From the devcontainer terminal, run: `./helpers/linux-kernel-generator.py /linux/kernel < kernel-request.txt`

## Tool Code Owner

@joshbressers

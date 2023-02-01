# GSD Tools

This repository (repo) is a part of the [Global Security Database (GSD)](https://globalsecuritydatabase.org), an open source project by the [Cloud Security Alliance (CSA)](https://cloudsecurityalliance.org) to address gaps within the current vulnerability identifier space.

If you are unfamiliar with the GSD and the vulnerability identifier space, please read the following document: **TODO: Create a tl;dr of what GSD & vuln ids are within gsd-project**

If you're looking to contribute or file a bug, please see the following guide: **TODO: Extract the repo descriptions & issue guide to a doc within gsd-project**

The `gsd-tools` repo contains any tools, parsers, applications, and other code related to the GSD. The data for the identifiers themselves live within the [gsd-database](https://github.com/cloudsecurityalliance/gsd-database) repo, and any non-data, non-code related documentation (such as meeting times and policies) live within the [gsd-project](https://github.com/cloudsecurityalliance/gsd-project) repo.

## Licensing

Please note that the data for GSD is `CC0`, everything else is `Apache v2.0`. See the [LICENSE.md](LICENSE.md) file for each project for more details.

## Tools

Each project has its own README and supporting documents. Included below is a short one line description of each project and a quick link to its more detailed README.

### Table of Contents

- [GSD Analysis](#gsd-analysis)
- [GSD API](#gsd-api)
- [GSD Bot](#gsd-bot)
- [GSD GitHub Actions](#gsd-github-actions)
- [GSD Requests](#gsd-requests)
- [GSD Schema](#gsd-schema)
- [GSD URL Processing](#gsd-url-processing)
- [GSD Web](#gsd-web)
- [Local Scripts](#local-scripts)

### GSD Analysis

- **Website:** _N/A_
- **Location:** `gsd-tools/gsd-analysis/`
- **README:** [GSD Analysis README](gsd-analysis/README.md)
- **Short Description:** A review of the GSD data using a python parser.
- **Depends on:** _None_

### GSD API

- **Website:** https://api.gsd.id
- **Location:** `gsd-tools/gsd-api/`
- **README:** [GSD API README](gsd-api/README.md)
- **Short Description:** Provides a simple REST API for interfacing with the GSD Database.
- **Depends on:**  GSD Database

### GSD Bot

- **Website:** _N/A_
- **Location:** `gsd-tools/gsd-bot/`
- **README:** [GSD Bot README](gsd-bot/README.md)
- **Short Description:** Provides automation around specifically formatted issues within the gsd-database repo.
- **Depends on:** _None_

### GSD GitHub Actions

- **Website:** _N/A_
- **Location:** `gsd-tools/gsd-github-actions/`
- **README:** [GSD GitHub Actions README](gsd-github-actions/README.md)
- **Short Description:** The GitHub actions used by GSD Database to validate new and existing identifiers.
- **Depends on:** _None_

### GSD Requests

- **Website:** https://requests.globalsecuritydatabase.org
- **Location:** `gsd-tools/gsd-requests/`
- **README:** [Requests Webform README](gsd-requests/README.md)
- **Short Description:** A utilitarian webform for submitting new GSD IDs.
- **Depends on:** GSD Database

### GSD Schema

- **Website:** _N/A_
- **Location:** `gsd-tools/gsd-schema/`
- **README:** [GSD Schema README](gsd-schema/README.md)
- **Short Description:** Provides the json schema of a GSD identifier.
- **Depends on:** _None_

### GSD URL Processing

- **Website:** _N/A_
- **Location:** `gsd-tools/gsd-url-processing/`
- **README:** [GSD URL Processing README](gsd-url-processing/README.md)
- **Short Description:** Various scripts written by @kurtseifried to process urls into GSD ids.
- **Depends on:** _None_

### GSD Web

- **Website:** https://gsd.id/home
- **Location:** `gsd-tools/gsd-web`
- **README:** [GSD Web README](gsd-web/README.md)
- **Short Description:** A human interface for interacting with and updating the GSD data.
- **Depends on:** GSD API, GSD Schema

### Local Scripts

- **Website:** _N/A_
- **Location:** `gsd-tools/local-scripts/`
- **README:** [Local Scripts README](local-scripts/README.md)
- **Short Description:** _TODO_ - Ask @kurtseifried
- **Depends on:** _None_

### GSD Project Notes

- **Website:** _N/A_
- **Location:** `gsd-tools/gsd-project/`
- **README:** [GSD URL Processing README](gsd-project/README.md)
- **Short Description:** Project Plans which contains all the GSD project plans and related material. 
- **Depends on:** _None_

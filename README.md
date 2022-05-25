# Global Security Database (GSD)

The Global Security Database is a new Working Group project from the Cloud Security Alliance meant to address the gaps in the current vulnerability identifier space.

The world of vulnerability identifiers has changed drastically in the last 20 years while the infrastructure and management of public and private vulnerability data have changed very little. This has created a sizable gap between the current needs of industry and the ability of existing projects to be effective.

For more information please see [csaurl.org/gsd-quick-links](https://csaurl.org/gsd-quick-links).

## Table of contents

1. [GSD Repos](#gsd-repos)
	1. [GSD Database](#gsd-database)
	2. [GSD Project](#gsd-project)
	3. [GSD Tools](#gsd-tools)
2. [Projects and tools](#projects-and-tools)
	1. [actions](#actions)
	2. [cloudflare-workers](#cloudflare-workers)
	3. [docker-compose](#docker-compose)
	4. [gsd-api](#gsd-api)
	5. [gsd-bot](#gsd-bot)
	6. [gsd-url-processing](#gsd-url-processing)
	7. [gsd-web](#gsd-web)
	8. [local-scripts](#local-scripts)
	9. [securitylist](#securitylist)
	10. [webform](#webform)

## GSD Repos

There are 3 primary repositories. 

### gsd-database
 
The gsd-database repo is the actual data for identifiers in the Global Security Database in the form of GSD-YEAR-INTEGER. To maintain easier compatibility with the CVE ecosystem we have decided to reserve numbers below 1 million for CVE data, using the same integer to make matching up entries easy.

#### Issues

Please file any data related issues in the gsd-database repo. If you need to file issues against the data format(s) themselves please file an issue in the gsd-project repo.

### gsd-project

The gsd-project repo is designed to support the project, meeting times, agendas, minutes, planning, roadmaps, vision, etc. are contained here.

#### Issues

Please file any project, governance, road maps, planning, data formats, process related issues or any general cross repo or project issues in the gsd-project repo.

### gsd-tools

The gsd-tools repo is the Global Security Database (GSD) tools repo which contains all the GSD tools. For more informaiton please see https://csaurl.org/gsd-quick-links.

#### Issues

Please file any tooling related issues in the gsd-tools repo. If you need to file issues against the data format(s) themselves please file an issue in the gsd-project repo.

## Projects and tools

*** TODO *** one line description and link to the README.md (which includes the WHY)

### actions
### cloudflare-workers
### docker-compose
### gsd-api

**WIP**

Provides a simple REST API for interfacing with the GSD Database.

[GSD API README](gsd-api/README.md)

### gsd-bot
### gsd-url-processing
### gsd-web

**WIP**

Provides a web interface for viewing, searching, and editing the GSD Database.

Relies on the gsd-api tool for retrieving the GSD data.

[GSD Web README](gsd-web/README.md)

### local-scripts
### securitylist
### webform

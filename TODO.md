# GSD Tools

The gsd-tools repo is the Global Security Database (GSD) tools repo which contains all the GSD tools. For more information please see https://csaurl.org/gsd-quick-links.

### Todo
- [ ] Update README.md
- [ ] https://github.com/cloudsecurityalliance/gsd-tools Please see the CONTRIBUTING and DEVELOP files. They both probably need some clarity. If someone could try to stand up some of these tools and see what instructions are missing.
- [ ] The webform https://requests.globalsecuritydatabase.org is EXTREMELY ugly. Please make it pretty.
- [ ] The webform https://requests.globalsecuritydatabase.org can only request simple IDs. It would be nice if there were more "dropdown" type elements to avoid having to type everything in (like vulnerability type for example)
- [ ] The webform https://requests.globalsecuritydatabase.org The webform could probably stand an API to interact with GSD
- [ ] The webform https://requests.globalsecuritydatabase.org The webform only captures URLs for references. We should be capturing other types of references (git commit IDs for example)
- [ ] https://edit.globalsecuritydatabase.org/ The only way to update an ID today is via a github PR. We should have a nice form to allow editing data.
- [ ] The tools run via docker-compose today. We should build some helm charts for this probably
- [ ] The securitylist tool is how we mirror NVD and CVE data. There is ZERO error checking in these scripts. It's also sort of hacked together. Some cleanup and documentation are needed
- [ ] The gsd-bot directory holds the bot. This bot looks are issues in github and creates files in the database. It has minimal error checking.
- [ ] The bot only outputs OSV data for kernel entries, it should output OSV format for everything (this will probably require some webform changes also)
- [ ] The bot has a special kernel mode and a special kernel helper script. The scripts are bad, not documented, and the process is a mystery to everyone except Josh and Oliver
- [ ] The bot has some tests, it needs more. A bunch of the tests probably fail
- [ ] What even is the cloudflare-workers directory? - the https://raw.globalsecuritydatabase.org/ e.g. https://raw.globalsecuritydatabase.org/GSD-2022-0821
- [ ] We have some codeql workflows. We could probably use more.

### In progress

### Completed

### Cancelled

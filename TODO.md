# GSD Tools TODO

NOTICE:

We are migrating these todos to GitHub issues for now this file exists as a bridge while those stories are enhanced. Do not add more items to this file, open an issue instead.

### Todo

- [x] Update README.md
	- Done
- [x] https://github.com/cloudsecurityalliance/gsd-tools Please see the CONTRIBUTING and DEVELOP files. They both probably need some clarity. If someone could try to stand up some of these tools and see what instructions are missing.
	- The README for each project should and will contain the necessary instructions to use and contribute to the project. The CONTRIBUTING file at the root level will provide general guidance and instructions on how to do pull requests. There is no need for a DEVELOP file anywhere, as the READMEs will accomplish that goal.
- [x] The webform https://requests.globalsecuritydatabase.org is EXTREMELY ugly. Please make it pretty.
	- Obsolete - the webform will be ingested into GSD Web, and _that_ should be made pretty.
- [x] The webform https://requests.globalsecuritydatabase.org can only request simple IDs. It would be nice if there were more "dropdown" type elements to avoid having to type everything in (like vulnerability type for example)
	- GSD Web will have a submission form similar in nature to how GitHub does theirs, using the GSD Schema (which is the OSV when doing traditional vuln ids). Said form will also include the auto description generator that Josh Bressers did.
- [x] The webform https://requests.globalsecuritydatabase.org The webform could probably stand an API to interact with GSD
	- Obsolete, GSD Web and GSD API fulfill this need.
- [x] The webform https://requests.globalsecuritydatabase.org The webform only captures URLs for references. We should be capturing other types of references (git commit IDs for example)
	- Obsolete - GSD Web will provide a form that has an add/remove button for references, and a dropdown for type, along with the URL and a comment field.
- [ ] ~https://gsd.id/ The only way to update an ID today is via a github PR. We should have a nice form to allow editing data.~
	- This should also open a PR directly instead of generating an issue.
	- Migrated to https://github.com/cloudsecurityalliance/gsd-tools/issues/24
- [x] The tools run via docker-compose today. We should build some helm charts for this probably
	- The CI/CD pipeline should use GitHub actions for deployment and cron tasks, or otherwise directly interface with the repo.
- [ ] ~The securitylist tool is how we mirror NVD and CVE data. There is ZERO error checking in these scripts. It's also sort of hacked together. Some cleanup and documentation are needed~
	- Migrated to https://github.com/cloudsecurityalliance/gsd-tools/issues/118
- [ ] ~The gsd-bot directory holds the bot. This bot looks are issues in github and creates files in the database. It has minimal error checking.~
	- Migrated to https://github.com/cloudsecurityalliance/gsd-tools/issues/119
- [ ] ~The bot only outputs OSV data for kernel entries, it should output OSV format for everything (this will probably require some webform changes also)~
	- Migrated to https://github.com/cloudsecurityalliance/gsd-tools/issues/120
- [ ] ~The bot has a special kernel mode and a special kernel helper script. The scripts are bad, not documented, and the process is a mystery to everyone except Josh and Oliver~
	- Migrated to https://github.com/cloudsecurityalliance/gsd-tools/issues/121
- [ ] ~The bot has some tests, it needs more. A bunch of the tests probably fail~
	- Migrated to:
		- https://github.com/cloudsecurityalliance/gsd-tools/issues/121
		- https://github.com/cloudsecurityalliance/gsd-tools/issues/120
		- https://github.com/cloudsecurityalliance/gsd-tools/issues/110
- [x] What even is the cloudflare-workers directory? - the https://raw.globalsecuritydatabase.org/ e.g. https://raw.globalsecuritydatabase.org/GSD-2022-0821
	- Donno, don't care. Deleted it for now, and we can always pull it out of Git history if needed again in the future.
- [ ] ~We have some codeql workflows. We could probably use more.~
	- Migrated to https://github.com/cloudsecurityalliance/gsd-tools/issues/122
- [ ] ~Replace all the scripts and manual processing that we're doing with GitHub actions.~
	- Migrated to https://github.com/cloudsecurityalliance/gsd-tools/issues/123

### In progress

### Completed

### Cancelled

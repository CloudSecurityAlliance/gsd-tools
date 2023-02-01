# MVP Requirements
## NOT a requirement

- Machine readable changelog / git blame

## Data format

[We use OSV by default, and may use other data formats or unspecified formats as well.](https://github.com/cloudsecurityalliance/gsd-project/blob/main/data-formats/Thoughts-on-data-formats.md) We will indicate what format we're using within the GSD, e.g.:

**Generalized format:**
```json
{
	"data_format": "NAMESPACE",
	"data_type": "NAME_OF_DATA_FORMAT",
	"data_version": "x.y.z"
}
```

**OSV Format example:**
```json
{
	"data_format": "osv.dev",
	"data_type": "OSV",
	"data_version": "1.0"
}
```

**CVE Format example:**
```json
{
	"data_format": "MITRE",
	"data_type": "CVE",
	"data_version": "4.0"
}
```

## Human Web Interface

Example identifiers:
- GSD ID - https://globalsecuritydatabase.org/identifier/GSD-2021-1000XXX
- CVE ID - https://globalsecuritydatabase.org/identifier/CVE-2021-1337
- GHSA ID - https://globalsecuritydatabase.org/identifier/GHSA-jc8m-cxhj-668x
- Git commit hash - https://globalsecuritydatabase.org/identifier/d3a83576378b4c904f711598dde2c5e881c4295c
- Named vuln
	- Heartbleed - https://globalsecuritydatabase.org/identifier/Heartbleed
	- BigSig - https://globalsecuritydatabase.org/identifier/BigSig
	- Log4Shell - https://globalsecuritydatabase.org/identifier/Log4Shell

---

- [ ] Present the data, in a nice / well formatted manner
- [ ] Allow updates/corrections of the data (from web interface)
	- Requires Github login & Github ID attached to update/data (via OAuth)
	- Show the GSD updates by default, and show the original data (we can discuss presentation options)
- [ ] Search GSDs
	- Present single/multiple results if exists
	- Otherwise allow creation of new GSD
	- When searching by identifier, match GSDs by "equivalent" not by "related"
- [ ] Guided process / web form for creation of new GSDs

## Machine Readable API

- [ ] Parsed json blob (GSD world view w/ GSD updates to referenced data by default)
	- https://api.globalsecuritydatabase.io/GSD-2021-1000XXX


# Thoughts on data formats

This is not a final document nor an official statement on the data format(s) used by the GSD. This is designed to help structure and encourage discussion around vulnerability identifer data formats.

The GSD can use other peoples data formats, especially if we clearly label them as such. We can also provide mappings, e.g. OSV:affected:package:name maps to CVE:product:product_name to translate the data and make it easier to consume.

# Compariong data formats

[Google Sheet - Data Formats and versions Compared](https://docs.google.com/spreadsheets/d/14VHXigdynIGB8okW3jyvtNj-LE0fxEsoBNMvswX4Kwg/edit?usp=sharing)

# GSD Identifer data components

What data components MUST/SHOULD/CAN a GSD identifier have, what is the bare minimum to make these useful?

## a GSD Identifier MUST have:

* Identifier
* Meta data (time assigned, who requested it, etc.)
* Reference URL (optional: type of URL, copy of data, etc.) OR Source (e.g. a namespace and an identifier, "redhat.com:RHSA-2021-1234" OR known exploit OR known exploitation

Essentially we need some path of discoverability and some data with a degree of confidence indicated (e.g. confirmed, rumour, etc.). 

## a GSD Identifier SHOULD have

* Affected / Fixed / Vulnerable / Not Vulnerable products/services (CPE? JSON? Purl?)
* Vulnerability information/type (e.g. CWE)
* An overall confidence score between 0 and 10 based on sources, confirmation, etc.

And ideally we want some information to make the security identifier directly useful for systems and humans beings that consume the data.

## a GSD Identifier CAN have:

* Text description
* Severity scores
* Relationship data (parent/child/sibling/etc of)
* Exploits (code/reproducers)
* Exploitation (knowledge of exploitation)
* Patches
* Workarounds
* Configuration related information

# String and value handling - multiple values

Anything that is a string or a value that can be more than one value needs to be a list so that multiple values can be clearly supported. A perfect example of this is [GSD-2021-1002352.json](https://github.com/cloudsecurityalliance/gsd-database/blob/main/2021/1002xxx/GSD-2021-1002352.json) which is called "log4j" and "log4j2" by Apache and other organizations use the names interchangeably it appears. This means that anything that is not clearly defined as having only a single possible value (e.g. the GSD ID itself, the assigned time) must be assumed to potentially be a list of values.

# Human-readable vs machine-readable data

The JSON data should contain both the human and machine readable data. Ideally a strong distinction should be made, e.g. machine readable affected product data should be highly structured, but a human readable text description should be allowed (e.g. the current style of CVE text description), and any human readable data MUST allow basic formatting, I think standardizing on Markdown is the most sensible solution. The current mess that is CVE text descriptions (overly short, some unreadable due to "ths is not CVE-FOO" and so on) and the experience of turning the text description in GSD-2021-1002352 into something more readable comes to mind. It should be noted that MITRE doesn't even allow line returns to split text up into paragraphs/etc (if you submit a CVE JSON entry they strip the line returns). 

# Types of fields

## Unique vs multiple occurances

Some fields must be unique across the GSD database, e.g. the GSD identifier for a specific GSD must be unique. But for example relationship data could contain multiple instances of a GSD identiifier across multiple different GSD identifiers

Some fields are expected to have non unique values, e.g. timestamps, lists of affected products, etc.

## Human-readable vs machine-readable

All fields should be assumed to be primarily machine readable (and ideally machine generated) except where specifically noted such as the description, or notes fields. 

## Generated vs manually created

Ideally fields should be generated with tools rather than being manually entered where possible, e.g. timestamps, or extracting data from a vendor advisory.

Many fields SHOULD (MUST?) support manual overrides, e.g. affected product lists, very few fields should not allow a manual override (GSD Identifier even? Timestamps?)

# Namespacing

All data must exist within a namespace, the two primary ones are "GSD" and "OSV", additional namespaces would typically be represented by a domain name, an email address, a URL, or a GitHub username/id combination (since names can change). Namespaces are available for entities, and entity can be an individual, a group, a company, an organization, an automated tool/AI/ML, etc.

# Other security data format examples:

* CSAF2 https://docs.oasis-open.org/csaf/csaf/v2.0/csd01/csaf-v2.0-csd01.html
* CVE https://github.com/CVEProject/cve-schema/tree/master/schema
* CVRF https://www.icasi.org/cvrf/
* OSV https://ossf.github.io/osv-schema/
* OVAL https://oval.mitre.org/

# Other security data format examples for specific subtypes of data:

* CPE https://nvd.nist.gov/products/cpe (Product ID)
* CVSS https://www.first.org/cvss/ (Vulnerability Impact)
* CWE https://cwe.mitre.org/community/submissions/guidelines.html (Vulnerability Type)
* EPSS https://www.first.org/epss/ (Exploitation Prediction)
* purl https://github.com/package-url/purl-spec (Product ID)
* NIST Vulnerability Ontology https://github.com/usnistgov/vulntology
* VEX https://github.com/CycloneDX/bom-examples/tree/master/VEX https://cyclonedx.org/capabilities/vex/

# Top Level Tagging

I think some top level tagging such as "vulnerability" would be useful to allow people to more easily sort/view data, some clusters:

* exposure
* vulnerability
* weakness
    
* availability
* confidentiality
* integrity
    
* backdoor
* deceptive software
* malware
    
* closed source
* cloud
* on premises
* open source
* service
    
* could have been worse
    
* exploit
* exploitation
* exploit code
* exposure
* incident
* ioc
    
* rugpull
* scam
* spam
    
* state actor
    
* configuration
* hardening
* enhancement
* patch
* removal of unsafe feature
* workaround
    
* project 
* publisher
* researcher 
* vendor

# Vulnerability Identifier Landscape

This list may be incomplete. If there is a project that you feel should be listed but is currently missing, please open a pull request to add it!

- SBOM Formats
	- [CycloneDX](https://cyclonedx.org/)
	- [SPDX](https://spdx.dev/)
- Software ID Formats
	- [cpe](https://nvd.nist.gov/products/cpe)
	- [pURL](https://github.com/package-url/purl-spec)
- Vulnerability Applicability
	- [VEX](https://cyclonedx.org/capabilities/vex/)
- Vulnerability ID Formats
	- [OSV Schema](https://ossf.github.io/osv-schema/)
	- [CSAF](https://oasis-open.github.io/csaf-documentation/)
- Vuln ID Centralization
	- [GSD](https://globalsecuritydatabase.org)
	- [OSV Database](https://osv.dev)
	- [GitHub Advisory Database](https://github.com/github/advisory-database)


# GSD Schema

The JSON schema of a GSD Identifier

- **Depends on:** _None_

The GSD doesn't have a finished data format yet. The GSD is experimenting primarily with an extended OSV format, various JSON-LD iterations and to a lesser degree the CVE JSON 5.0 format (by virtue of importing the existing data). 

If you want to help improve the OSV format please file an issue in the https://github.com/ossf/osv-schema project.

Please note that all data contained within the GSD (be it an ID or otherwise) is assumed to be Unicode and of no fixed length (e.g. some standards like CVE JSON have maximum length field sizes). Please keep this in mind when building tools to consume GSD data.

## Supported data formats

The GSD data files are JSON and use a simple name spacing strategy to support multiple data formats. The basic structure is a JSON object (data with "{}") that contains key/value pairs that consist of a namespace identifier (e.g. "GSD" or "OSF") and a second JSON object with the data (e.g. GSD or OSV data). This allows direct imports of existing JSON data from other formats.

| Name | Name Space ID | URL to Schema |
| ---- |---------------| --------------|
| CSAF2 | CSAF2 or csaf2 | https://github.com/oasis-tcs/csaf/blob/master/csaf_2.0/json_schema/csaf_json_schema.json |
| CVE4 | CVE4 or cve4 | https://github.com/CVEProject/cve-schema/tree/master/schema/v4.0 |
| CVE5 | CVE5 or cve5 | https://github.com/CVEProject/cve-schema/tree/master/schema/v5.0 |
| OSV | OSV or osv | https://ossf.github.io/osv-schema/ |
| GSD | GSD or gsd | NONE |

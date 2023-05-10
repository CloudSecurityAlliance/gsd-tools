# OSV GSD Schema

The GSD project primarily relies on the OSV schema for data, but we use an enhanced version of the currently released OSV schema. The reason for this is that the OSV takes time to release new versions of the schema, and in order to prevent blocking the release of data, we use the extended version which is backward compatible with the OSV schema. Using the standard OSV parser will result in warnings (e.g. some ENUM values we use are not present in OSV), but simply ignore the extended fields and attributes you will be able to process the data.

Where we use the OSV schema we will use the standard "schema_version" tag set to the appropriate version of the OSV schema. 

If we have extended data we will also add the "schema_type" and set it to "OSV-GSD", and add an "osv_gsd_schema_version" tag and set it to the appropriate version (e.g. "1.0.0").

When parsing OSV GSD data you can simply parse it as "strict" OSV data and ignore our extensions if you do not support the GSD extensions, this can be done using the "local-scripts/remove-extra-JSON-keys.py" script for example.

# OSV GSD Extensions - Completed

## severity["type": "CVSS_V2"]

Upstream: https://github.com/ossf/osv-schema/pull/87
Released in OSV schema: 1.4.0

We needed CVSS v2 data in addition to CVSS v3 data so we can import historical data.

## {"references": ["type": "DISCUSSION"]}

Upstream: https://github.com/ossf/osv-schema/pull/138
Released in OSV schema: 1.5.0

We needed a DISCUSSION reference type for discussions of the issues that do not include fixes/etc.

## {"$id": "VALUE"}

Upstream: https://github.com/ossf/osv-schema/pull/130
Released in OSV schema: 1.5.0

We need to explicitly know what type of data this is, as do downstream consumers.

## {"affected": ["ranges": ["events": ["last_affected": "VALUE"]]]}

Upstream: https://github.com/ossf/osv-schema/pull/147
Released in OSV schema: 1.5.0

For situations like the Linux Kernel, there may be a known last affected version, but no fixed version (e.g. the functionality with the vulnerability was completely removed).

## {"references": [ {"DETECTION": string,}]}

Upstream: https://github.com/ossf/osv-schema/pull/137
Released in OSV schema: 1.5.0

We needed the DETECTION type for tools and scripts that detect the vulnerability (e.g., during #log4j there were many tools released to detect the vulnerability).

## {"references": ["type": "INTRODUCED"]}

Upstream: https://github.com/ossf/osv-schema/pull/128
Added to OSV schema in: 1.5.0

We needed to be able to specify when the vulnerability was introduced, e.g., for the Linux Kernel data.

# OSV GSD Extensions - Active

## {"schema_type": "VALUE"}

Upstream: https://github.com/ossf/osv-schema/pull/134
Released in OSV-GSD schema: 1.0.0

We use the schema_type tag (in line with other standards such as CVE) so that the data is explicitly labeled instead of implicitly inferred (e.g., parse the data against various schemas to see which one it is). The default value for the GSD OSV schema is OSV-GSD, and then we use the "schema_version" value as expected with SEMVER. If this tag is set a "osv_gsd_schema_version" MUST be set as well.

## {"osv_gsd_schema_version": "VALUE"}

Upstream: N/A
Released in OSV-GSD schema: 1.0.0

We use the osv_gsd_schema_version tag (in line with other standards such as CVE) so that the data is explicitly labeled instead of implicitly inferred (e.g., parse the data against various schemas to see which one it is). There is no default value for the GSD OSV schema version, and then we use the "schema_version" value as expected with SEMVER.

## {"affected": ["ranges": ["type": "TIMESTAMP"]]}

Upstream: https://github.com/ossf/osv-schema/issues/129
Released in OSV-GSD schema: 1.0.0

Adding TIMESTAMP allows us to refer to cloud services and APIs that do not do versioning, and for vendors (such as IBM Cloud) that release affected time ranges for their vulnerabilities and updates. Please note that TIMESTAMP follows the exact same logic as SEMVER, ECOSYSTEM, and GIT (e.g. time it started being affected, time it stopped being affected).

## severity["type": "EPSS"]

Upstream: https://github.com/ossf/osv-schema/issues/144
Released in OSV-GSD schema: 1.0.0

We want EPSS data in addition to CVSS v3/v2 data so we can import exploitability data in a machine-readable format.

## {"relationships": [{"type": "string", "id": "string", "canonical_url": "string"}]}

Upstream: https://github.com/ossf/osv-schema/pull/133
Released in OSV-GSD schema: 1.0.0

We need richer relationship data, e.g., how is GSD-YEAR-INTEGER related to another GSD-YEAR-INTEGER or RHSA-YEAR-INTEGER? Is it a parent of? Child of? Caused by? etc. The values for "type" are: ALIAS, CAUSES, CAUSED_BY, COMMON_NAME, DUPLICATED_BY, DUPLICATE_OF, INCOMPLETE_FIX_FOR, INSUFFICIENT_FIX_OF, RELATED. Only the id is required.

# Files

Our current version of the OSV-GSD schema JSON lives in GitHub at: https://github.com/ossf/osv-schema/blob/main/validation/schema.json
Our current version of the OSV-GSD schema markdown lives in GitHub at: https://github.com/ossf/osv-schema/blob/main/docs/schema.md

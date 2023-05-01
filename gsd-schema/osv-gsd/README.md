# OSV GSD Schema

The GSD project primarily relies on the OSV schema for data, but we use an enhanced version of the currently released OSV schema. The reason for this is that the OSV takes time to release new versions of the schema, and in order to prevent blocking the release of data, we use the extended version which is backward compatible with the OSV schema. Using the standard OSV parser will result in warnings (e.g. some ENUM values we use are not present in OSV), but simply ignore the extended fields and attributes you will be able to process the data.

# OSV GSD Extensions

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

## {"schema_type": "VALUE"}

Upstream: https://github.com/ossf/osv-schema/pull/134

We use the schema_type tag (in line with other standards such as CVE) so that the data is explicitly labeled instead of implicitly inferred (e.g., parse the data against various schemas to see which one it is). The default value for the GSD OSV schema is OSV-GSD, and then we use the "schema_version" value as expected with SEMVER.

## {"references": ["type": "INTRODUCED"]}

Upstream: https://github.com/ossf/osv-schema/pull/128
Added to OSV schema in: 1.5.0

We needed to be able to specify when the vulnerability was introduced, e.g., for the Linux Kernel data.

## {"affected": ["ranges": ["type": "TIMESTAMP"]]}

Upstream: https://github.com/ossf/osv-schema/issues/129

Adding TIMESTAMP allows us to refer to cloud services and APIs that do not do versioning, and for vendors (such as IBM Cloud) that release affected time ranges for their vulnerabilities and updates. Please note that TIMESTAMP follows the exact same logic as SEMVER, ECOSYSTEM, and GIT (e.g. time it started being affected, time it stopped being affected).

## severity["type": "EPSS"]

Upstream: https://github.com/ossf/osv-schema/issues/144

We want EPSS data in addition to CVSS v3/v2 data so we can import exploitability data in a machine-readable format.

## {"relationships": [{"type": "string", "id": "string", "canonical_url": "string"}]}

Upstream: https://github.com/ossf/osv-schema/pull/133

We need richer relationship data, e.g., how is GSD-YEAR-INTEGER related to another GSD-YEAR-INTEGER or RHSA-YEAR-INTEGER? Is it a parent of? Child of? Caused by? etc. The values for "type" are: ALIAS, CAUSES, CAUSED_BY, COMMON_NAME, DUPLICATED_BY, DUPLICATE_OF, INCOMPLETE_FIX_FOR, INSUFFICIENT_FIX_OF, RELATED. Only the id is required.

# Files

Our version of the OSV-GSD schema JSON lives in GitHub at: https://github.com/ossf/osv-schema/blob/main/validation/schema.json
Our version of the OSV-GSD schema markdown lives in GitHub at: https://github.com/ossf/osv-schema/blob/main/docs/schema.md

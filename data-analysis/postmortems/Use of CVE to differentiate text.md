# Use of CVE ID to differentiate text describing CVE ID

A lot of CVE text descriptions (especially from Microsoft) are now largely devoid of information, so much so that they must list other CVE ID's in order to differentiate the ID's:

```
wget https://nvd.nist.gov/feeds/json/cve/1.1/nvdcve-1.1-2021.json.gz
gzip -d nvdcve-1.1-2021.json.gz
grep -A 2 "\"description_data\"" nvdcve-1.1-2021.json  | grep "\"value\""  | grep "CVE-2021-" | grep -v " REJECT " | grep "\(unique\|different\|similar\)" | sort
```
Example data:

Search for: "Storage Spaces Controller Elevation of Privilege Vulnerability" (https://nvd.nist.gov/vuln/search/results?form_type=Basic&results_type=overview&query=Storage+Spaces+Controller+Elevation+of+Privilege+Vulnerability&search_type=all&isCpeNameSearch=false)

|CVE ID|Text Description|
|------|----------------|
|CVE-2021-41345|Storage Spaces Controller Elevation of Privilege Vulnerability This CVE ID is unique from CVE-2021-26441, CVE-2021-40478, CVE-2021-40488, CVE-2021-40489.|
|CVE-2021-40489|Storage Spaces Controller Elevation of Privilege Vulnerability This CVE ID is unique from CVE-2021-26441, CVE-2021-40478, CVE-2021-40488, CVE-2021-41345.|
|CVE-2021-40488|Storage Spaces Controller Elevation of Privilege Vulnerability This CVE ID is unique from CVE-2021-26441, CVE-2021-40478, CVE-2021-40489, CVE-2021-41345.|
|CVE-2021-40478|Storage Spaces Controller Elevation of Privilege Vulnerability This CVE ID is unique from CVE-2021-26441, CVE-2021-40488, CVE-2021-40489, CVE-2021-41345.|
|CVE-2021-26441|Storage Spaces Controller Elevation of Privilege Vulnerability This CVE ID is unique from CVE-2021-40478, CVE-2021-40488, CVE-2021-40489, CVE-2021-41345.|
|CVE-2021-34536|Storage Spaces Controller Elevation of Privilege Vulnerability|
|CVE-2021-34460|Storage Spaces Controller Elevation of Privilege Vulnerability This CVE ID is unique from CVE-2021-33751, CVE-2021-34510, CVE-2021-34512, CVE-2021-34513.|
|CVE-2021-34513|Storage Spaces Controller Elevation of Privilege Vulnerability This CVE ID is unique from CVE-2021-33751, CVE-2021-34460, CVE-2021-34510, CVE-2021-34512.|
|CVE-2021-34512|Storage Spaces Controller Elevation of Privilege Vulnerability This CVE ID is unique from CVE-2021-33751, CVE-2021-34460, CVE-2021-34510, CVE-2021-34513.|
|CVE-2021-34510|Storage Spaces Controller Elevation of Privilege Vulnerability This CVE ID is unique from CVE-2021-33751, CVE-2021-34460, CVE-2021-34512, CVE-2021-34513.|
|CVE-2021-33751|Storage Spaces Controller Elevation of Privilege Vulnerability This CVE ID is unique from CVE-2021-34460, CVE-2021-34510, CVE-2021-34512, CVE-2021-34513.|
|CVE-2021-26880|Storage Spaces Controller Elevation of Privilege Vulnerability|

# Recommendations:

1. Ensure Security Identifiers have sufficient original sourcing in order to determine what they are/apply to.
2. For many Security ID's the description text doesn't matter that much

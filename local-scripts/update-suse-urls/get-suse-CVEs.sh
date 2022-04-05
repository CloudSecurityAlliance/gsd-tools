#!/bin/bash

# https://www.suse.com/security/cve/
# and convert to a list of CVEs in suse-cve.txt

wget https://www.suse.com/security/cve/

grep "^<a href=\"CVE-" index.html | cut -d"\"" -f2 | sed 's/\.html$//' > suse-cve.txt

rm -f index.html

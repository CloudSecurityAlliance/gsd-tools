# "vim is vulnerable to Heap-based Buffer Overflow" 

https://nvd.nist.gov/vuln/search/results?form_type=Basic&results_type=overview&query=vim+is+vulnerable+to+Heap-based+Buffer+Overflow&search_type=all&isCpeNameSearch=false

These CVE's all have the exact same description:

* CVE-2021-3927 - https://huntr.dev/bounties/9c2b2c82-48bb-4be9-ab8f-a48ea252d1b0/ - Oct 26th 2021
* CVE-2021-3903 - https://huntr.dev/bounties/35738a4f-55ce-446c-b836-2fb0b39625f8/ - Oct 24th 2021
* CVE-2021-3872 - https://huntr.dev/bounties/c958013b-1c09-4939-92ca-92f50aa169e8/ - Oct 7th 2021
* CVE-2021-3875 - https://huntr.dev/bounties/5cdbc168-6ba1-4bc2-ba6c-28be12166a53/ - Oct 5th 2021
* CVE-2021-3778 - https://huntr.dev/bounties/d9c17308-2c99-4f9f-a706-f7f72c24c273/ - Sep 7th 2021
* CVE-2021-3770 - https://huntr.dev/bounties/016ad2f2-07c1-4d14-a8ce-6eed10729365/ - Sep 3rd 2021

It appears someone fuzzed vim and then released the results piecemeal resul;ting in multiple CVEs rather than a single CVE for multiple issues within the same version/vulnerability type, etc. 

TODO: confirm same reporter, timelines

TODO: The CVSS scores are all different, this needs investigation.

# Recommendations:

1. Include data about related Security Identifiers and what the relationship is (e.g. parent/child/sibling?)

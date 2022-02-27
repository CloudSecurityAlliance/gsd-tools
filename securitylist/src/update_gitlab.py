#!/usr/bin/env python

import securitylist
import sys
import os

def main():

    data_path = sys.argv[1]
    securitylist.CVE.path = data_path

    gitlab = securitylist.GitLab().fetch()

    for cve_id, advisory_list in gitlab.items():
        try:
            c = securitylist.CVE(cve_id)
            c.add_data('gitlab.com', advisory_list)
            c.write()
        except:
            print(f"There was an error with record {cve_id}.")

if __name__ == "__main__":
    main()

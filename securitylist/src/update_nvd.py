#!/usr/bin/env python

import securitylist
import sys
import os

def main():

    data_path = sys.argv[1]
    securitylist.CVE.path = data_path

    start_time = None

    # Check for an updated_time file
    meta_time_file = os.path.join(data_path, "nvd_updated_time.txt")
    if os.path.exists(meta_time_file):
        with open(meta_time_file) as fh:
            start_time = fh.readline().rstrip()

    nvd = securitylist.NVD()
    nvd.get_range(start_time, None)

    print("Getting %d IDs" % nvd.total)

    for i in nvd:
        the_id = i['cve']['id']
        # We need to put these in the NVD namespace
        c = securitylist.CVE(the_id)
        c.add_data('nvd.nist.gov', i)
        c.write()

    # We need to store the end time for future use
    with open(meta_time_file, 'w') as fh:
        fh.write(nvd.get_end_time_str())
        fh.write("\n")

if __name__ == "__main__":
    main()

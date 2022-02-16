# Script for querying the CISA Known Exploited Vulnerabilities 
# and merge it with the GSD Identifier
# Initial Author : Palash Oswal
# TODO : Some snippets are duplicated across various other scripts (CVE.py/NIST.py)

#
# Invoke this script directly from gsd-database workdir
#

import requests
import json
import os


vuln_url = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"

def cve_to_gsd(cve):
    return cve.replace("CVE","GSD")

def get_filename(gsd_id):
    # The filename will look like
    # {self.path} / year / thousand_dir / {self.id}.json
    (year, just_id) = gsd_id.split('-')[1:]
    id_int = int(just_id)
    thousand_dir = "%dxxx" % int(id_int / 1000)
    the_path = os.path.join(os.getcwd(), year, thousand_dir) # Currently thinks cwd is gsd-database. TODO: Update this to take path as input.
    id_file = f"{gsd_id}.json"
    the_filename = os.path.join(the_path, id_file)
    if not os.path.exists(the_filename):
      print("The following CVE Entry does not have a GSD File - " + gsd_id)
      return ""
    return the_filename


def update_gsd_file(filename, json_blob):
    with open(filename, 'r') as fh:
      original_data=fh.read()
      fh.close()
    json_data = json.loads(original_data)
    namespace = 'cisa.gov'
    try:
      if (json_data['namespaces'][namespace]) != json_blob:
         json_data['namespaces'][namespace] = json_blob
         print(filename + " updated")
    except KeyError:
      json_data['namespaces'][namespace] = json_blob
    with open(filename, 'w') as fh:
      fh.write(json.dumps(json_data,sort_keys=True, indent=4))
      fh.close()
    return

def main():
    source_data = requests.get(url=vuln_url).json()
    for vuln in source_data["vulnerabilities"]:
       gsd_identifier = cve_to_gsd(vuln['cveID'])
       filename = get_filename(gsd_identifier)
       update_gsd_file(filename,vuln)

if __name__=="__main__":
    main()


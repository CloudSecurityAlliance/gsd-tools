# Module for querying the NVD CVE API
#

import json
import os
from pathlib import Path

class CVE:
    path = None

    def __init__(self, cve_id):
        self.id = cve_id
        self.gsd_id = "GSD" + self.id[3:]

        if os.path.exists(self.get_filename()):
            # Read the file
            with open(self.get_filename()) as fh:
                self.json = json.load(fh)
        else:
            self.json = { "namespaces": {} }

    def add_data(self, namespace, data):
        # Add data to a namespace

        self.json["namespaces"][namespace] = data

        # If the namespace is cve.org and there's no description, add one
        if namespace == 'cve.org':
            if 'GSD' not in self.json:
                self.json['GSD'] = {}

            if 'id' not in self.json['GSD']:
                    self.json['GSD']['id'] = self.gsd_id
            if 'alias' not in self.json['GSD']:
                self.json['GSD']['alias'] = self.id

            # Check for a description
            if 'description' not in self.json['GSD']:
                if '** RESERVED **' not in self.json['namespaces']['cve.org']['description']['description_data'][0]['value']:
                    self.json['GSD']['description'] = self.json['namespaces']['cve.org']['description']['description_data'][0]['value']


    def write(self):
        # Write the CVE content to a file. Returns true if the contents
        # changed and were updated

        filename = self.get_filename(create=True)

        old_data = ""
        new_data = json.dumps(self.json, sort_keys=True, indent=4)

        if os.path.exists(filename):
            with open(filename) as fh:
                # We load and re-encode the json, because something weird
                # things happen if we just try to read it directly
                old_json = json.load(fh)
                old_data = json.dumps(old_json, sort_keys=True, indent=4)

        # Only update the file if something changed
        if old_data != new_data:
            with open(filename, 'w') as fh:
                fh.write(json.dumps(self.json, sort_keys=True, indent=4))
            return True
        return False

    def get_filename(self, create=False):

        # The filename will look like
        # {self.path} / year / thousand_dir / {self.id}.json
        (year, just_id) = self.id.split('-')[1:]

        id_int = int(just_id)
        thousand_dir = "%dxxx" % int(id_int / 1000)

        the_path = os.path.join(self.path, year, thousand_dir)
        if create is True:
            Path(the_path).mkdir(parents=True, exist_ok=True)

        gsd_id = self.gsd_id

        id_file = f"{gsd_id}.json"
        the_filename = os.path.join(the_path, id_file)

        return the_filename

#!/usr/bin/env python

import sys
import os
import glob
import json

db_path = sys.argv[1]

os.chdir(db_path)

files = glob.glob('2021/*/*.json', recursive=True)

for f in files:
    filename = os.path.basename(f)
    dirname = os.path.dirname(f)

    if filename[0:2] == 'GSD':
        continue

    with open(f, 'r+') as fh:

        new_data = {}

        data = json.load(fh)

        for i in data:
            if i == 'UVI' or i == 'uvi':
                new_data['GSD'] = data[i]
            else:
                new_data[i] = data[i]

        if 'OSV' in new_data:
            old_id = new_data['OSV']['id']
            new_id = 'GSD' + old_id[3:]
            new_data['OSV']['id'] = new_id

        new_file = 'GSD' + filename[3:]
        new_filename = os.path.join(dirname, new_file)

        to_write = json.dumps(new_data, indent=2)
        to_write = to_write + "\n"

        fh.seek(0)
        fh.write(to_write)
    print(new_filename)
    os.system("git mv %s %s" % (f, new_filename))

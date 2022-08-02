#!/usr/bin/env python3

import sys
import json
import os
import re

# Take a file name to update

file = sys.argv[1]

# open, read the file, generate the json.dumps with indent=2 and close it

# TODO: get filename, if >=1000000 then indent = 2 if 4-6 digits then 4

filename = os.path.basename(file)
id_integer = filename.split("-")
id_year = id_integer[1]

tmp_integer = id_integer[2].split(".")
id_integer_raw = tmp_integer[0]

indent_size=4

if re.match("202[0-9]", id_year):
    if re.match("[0-9]{7,8}", id_integer_raw):
        indent_size=2
        print("GSD")

quit()

with open(file, "r") as f:
    data = json.load(f)
    output = json.dumps(data, indent=indent_size)
    f.close()

# open, write the file and close

with open(file, "w") as f:
    f.write(output)

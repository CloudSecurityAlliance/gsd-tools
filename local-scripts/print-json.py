#!/usr/bin/env python3

import sys
import json

# Take a file name to update

file = sys.argv[1]

# open, read the file, generate the json.dumps with indent=2 and close it

with open(file, "r") as f:
    data = json.load(f)
    output = json.dumps(data, indent=2)
    f.close()

# open, write the file and close

with open(file, "w") as f:
    f.write(output)

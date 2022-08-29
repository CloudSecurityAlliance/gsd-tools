#!/usr/bin/env python3

import sys
import json
import os
import re

# Take a file name to update

file = sys.argv[1]

# open, read the file, generate the json.dumps with indent=2 and close it

def set_file_indent(file):
    # This code breaks in 2030 and.or after we assign 1 million GSDs per year
    file_name = os.path.basename(file)
    if re.match("GSD-202[1-9]-1[0-9][0-9][0-9][0-9][0-9][0-9]", file_name):
        indent = 2
    else:
        indent = 4
    return(indent)

file_indent = set_file_indent(file)

with open(file, "r") as f:
    data = json.load(f)
    output = json.dumps(data, indent=file_indent)
    f.close()

# open, write the file and close

with open(file, "w") as f:
    f.write(output)

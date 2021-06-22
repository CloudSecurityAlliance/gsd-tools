#!/usr/bin/env python

import datetime
import pathlib
import UVI
import os

repo_name = os.environ['GH_REPO']
repo_url = "https://github.com/%s.git" % repo_name
username = os.environ['GH_USERNAME']

# Check out the repo

uvi_repo = UVI.UVIRepo(repo_url)

# Gather all the files

all_ids = uvi_repo.get_all_ids()

# Load data

for i in all_ids:
    print(i)
    the_data = uvi_repo.get_id(i)

    uvi_data = the_data["uvi"]

    # We will do something special for the kernel
    if uvi_data["vendor_name"] == "Linux" and \
        uvi_data["product_name"] == "Kernel":

        # Grab the first line
        summary = uvi_data["description"].split('\n')[0]
        the_data["OSV"]["summary"] = summary
        the_data["OSV"]["details"] = uvi_data["description"]

    else:
        # Everything not the kernel we will construct a simple summary
        vuln_type = uvi_data["vulnerability_type"]
        name = uvi_data["product_name"]
        version = uvi_data["product_version"]

        summary = f"{vuln_type} in {name} version {version}"
        the_data["OSV"]["summary"] = summary
        the_data["OSV"]["details"] = uvi_data["description"]

    the_time =  datetime.datetime.utcnow().isoformat() + "Z"
    the_data["OSV"]["modified"] = the_time

    # Write file and add to commit
    uvi_repo.update_id(i, the_data)

uvi_repo.commit("Update OSV summary")
uvi_repo.push()

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

    # If not namespace
    if "OSV" not in the_data:

        issue_data = the_data["uvi"]

        if "description" not in issue_data:
            issue_data["description"] = the_data["description"]["description_data"][0]["value"]

        if "extended_references" not in issue_data:
            # We need to add extended references to kernel issues
            if issue_data["vendor_name"] == "Linux" and \
               issue_data["product_name"] == "Kernel":
                fixed = issue_data["description"].find("by commit")
                fixed_hash = issue_data["description"][fixed+10:fixed+50]
                introduced = issue_data["description"].find("by commit", fixed+50)
                introduced_hash = issue_data["description"][introduced+10:introduced+50]
                issue_data["extended_references"] = [
                    {
                        "type": "commit",
                        "value": introduced_hash,
                        "note": "introduced"
                    },
                    {
                        "type": "commit",
                        "value": fixed_hash,
                        "note": "fixed"
                    }
                ]

        # Add the OSV data
        osv_data = uvi_repo.get_osv_json_format(i, issue_data)
        the_data["OSV"] = osv_data

        # XXX: Fix the time
        filename = uvi_repo.get_file(i)
        fpath = pathlib.Path(filename)
        # is this UTC?
        ctime = fpath.stat().st_ctime
        new_time = datetime.datetime.fromtimestamp(ctime).isoformat() + "Z"
        the_data["OSV"]["published"] = new_time

        # Write file and add to commit
        uvi_repo.update_id(i, the_data)

uvi_repo.commit("Add OSV data")
uvi_repo.push()

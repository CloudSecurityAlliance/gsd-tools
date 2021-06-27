#!/usr/bin/env python3

import git
import sys
import json
import requests
import os
import re
import sys
import logging
import time

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

import argparse

def main():
    # TODO: Use a getopt library


    parser = argparse.ArgumentParser()

    parser.add_argument('--check', '-c', action="store_true",
                        dest="check", help="Check the commits for correctness")
    parser.add_argument('--ignore', '-i', action="store_true",
                        dest="ignore", help="Ignore commit version mismatches")
    parser.add_argument('filename', type=str, nargs='*', default=None,
                        help='The kernel repo')
    args = parser.parse_args()

    git_cache = args.filename[0]
    repo = git.Repo(git_cache)

    logging.basicConfig(level=logging.INFO)

    s = requests.Session()
    retries = Retry(total=5, backoff_factor=1)
    s.mount('https://', HTTPAdapter(max_retries=retries))

    # This data looks like introduced,version,fixed,version
    for i in sys.stdin.readlines():

        line = i.rstrip().lstrip()

        if line == "":
            continue

        if not args.check:
            print(f"Parsing {line}")

        issue_data = line
        issue_array = issue_data.split(',')

        introduced_hash = issue_array[0]
        introduced_version = issue_array[1]
        fixed_hash = issue_array[2]
        fixed_version = issue_array[3]

        # For now assume this is up to date
        commit = repo.commit(issue_array[2])
        commit_message = commit.message
        commit_title = commit_message.splitlines()[0]


        # The introduced data can be missing
        if not introduced_hash == '' and not introduced_version == '':
            # Verify some things
            check_commit = repo.commit(introduced_hash)
            check_version = re.search(r'(v[0-9a-z.-]+)[\~\^]', check_commit.name_rev)

            if not args.ignore:
                if introduced_version not in check_version.groups()[0]:
                    print("There is an introduced version mismatch")
                    print(f"hash:{introduced_hash} - {introduced_version}")
                    print("Actual version: %s" % check_version.groups()[0])
                    print()

                    # Only bail if we are not checking
                    if not args.check:
                        sys.exit(1)


        check_commit = repo.commit(fixed_hash)
        check_version = re.search(r'(v\d+\.\d+\.\d+)\~', check_commit.name_rev)

        if not args.ignore:
            if fixed_version not in check_version.groups()[0]:
                print("There is a fixed version mismatch")
                print(f"hash:{fixed_hash} - {fixed_version}")
                print("Actual version: %s" % check_version.groups()[0])
                print()
                if not args.check:
                    sys.exit(1)

        # Open the issue
        json_data = {
            "vendor_name": "Linux",
            "product_name": "Kernel",
            "product_version": f"versions from {introduced_version} to before {fixed_version}",
            "vulnerability_type": "unspecified",
            "affected_component": "unspecified",
            "attack_vector": "unspecified",
            "impact": "unspecified",
            "credit": "",
            "references": [
                f"https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/commit/?id={introduced_hash}",
                f"https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/commit/?id={fixed_hash}"
            ],
            "extended_references": [
                {
                    "type": "commit",
                    "value": f"{introduced_hash}",
                    "note": "introduced"
                },
                {
                    "type": "commit",
                    "value": f"{fixed_hash}",
                    "note": "fixed"
                }
            ],
            "reporter": "joshbressers",
            "reporter_id": 1692786,
            "notes": "",
            "description": f"{commit_title}\n\nThis is an automated ID intended to aid in discovery of potential security vulnerabilities. The actual impact and attack plausibility have not yet been proven.\nThis ID is fixed in Linux Kernel version {fixed_version} by commit {fixed_hash}, it was introduced in version {introduced_version} by commit {introduced_hash}. For more details please see the references link."
        }

        # We need to delete the introduced data if it's blank
        if introduced_hash == '' and introduced_version == '':
            del(json_data["references"][0])
            del(json_data["extended_references"][0])

        json_output = json.dumps(json_data, indent=2)


        github_repo = os.environ['GH_REPO']
        auth = (os.environ['GH_USERNAME'], os.environ['GH_TOKEN'])
        body = {
            "title": "UVI Request",
            "body": f"```\n--- UVI JSON ---\n{json_output}\n--- UVI JSON ---\n```",
            "labels": ["new", "check"]
        }
        headers = {
                "accept": "application/json",
                "User-Agent": "request"
        }

        if not args.check:
            # Only do this if we're not checking

            resp = s.post(f"https://api.github.com/repos/{github_repo}/issues",
        json=body, auth=auth, headers=headers)
            try:
                resp.raise_for_status()
            except:
                print(resp)
                print(resp.text)
                exit(1)

            issue_id = resp.json()["number"]
            print(f"Filed issue #{issue_id}")

            # If we don't slow down, we hit the rate limit
            time.sleep(5)

if __name__ == "__main__":
	main()

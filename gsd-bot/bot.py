#!/usr/bin/env python3

import os
import re
import datetime
import time
import GSD

repo_name = os.environ['GH_REPO']
issues_url = "https://api.github.com/repos/%s/issues" % repo_name
repo_url = "https://github.com/%s.git" % repo_name
username = os.environ['GH_USERNAME']


def main():

    start_time = datetime.datetime.now()

    new_issues = GSD.get_new_issues(issues_url)
    can_issues = GSD.get_approved_can_issues(issues_url)

    if len(new_issues) > 0 or len(can_issues) > 0:

        # Only touch the repo if we have work to do
        gsd_repo = GSD.GSDRepo(repo_url)

        # Look for new issues
        for i in new_issues:

            if re.search('(GSD|CAN)-\d{4}-\d+', i.title):
                # There shouldn't be a GSD/CAN ID in the title, bail on this issue
                print("Found an ID in the title for issue %s" % i.id)
                continue

            if not gsd_repo.approved_user(user_name=i.creator, user_id=i.creator_id):
                print("Issue %s is not created by an approved user" % (i.id))
                continue

            print("Updating issue %s" % i.id)
            gsd_id = gsd_repo.add_gsd(i)
            i.assign_gsd(gsd_id, gsd_repo.approved_user(i.get_reporter()))

        # Now look for approved CAN issues
        for i in can_issues:
            approver = i.who_approved()
            if gsd_repo.approved_user(approver):
                # Flip this to a GSD
                gsd_repo.can_to_gsd(i)
                i.can_to_gsd()
            else:
                print("%s is unapproved for %s" % (approver, i.id))

        gsd_repo.close()

    stop_time = datetime.datetime.now()
    total_time = stop_time - start_time
    total_seconds = total_time.total_seconds()

    if total_seconds < 10:
        # Things get weird if we die too early wtih docker-compose
        time.sleep(10 - total_seconds)
    
if __name__ == "__main__":
    main()

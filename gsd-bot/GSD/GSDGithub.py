
import requests
import os
from .GSDIssue import Issue

def get_new_issues(issues_url):
    auth = (os.environ['GH_USERNAME'], os.environ['GH_TOKEN'])
    params = {
            'accept': "application/vnd.github.v3+json",
            'labels': 'new,check',
            'state': 'open'
    }

    # XXX Get the repo from the environment or something
    resp = requests.get(issues_url, auth=auth, params=params)
    resp.raise_for_status()

    issues = resp.json()

    to_return = []
    for i in issues:
        to_return.append(Issue(i))

    return to_return

def get_approved_can_issues(issues_url):
    auth = (os.environ['GH_USERNAME'], os.environ['GH_TOKEN'])
    params = {
            'accept': "application/vnd.github.v3+json",
            'labels': 'approved',
            'state': 'open'
    }

    # XXX Get the repo from the environment or something
    resp = requests.get(issues_url, auth=auth, params=params)
    resp.raise_for_status()

    issues = resp.json()

    to_return = []
    for i in issues:
        to_return.append(Issue(i))

    return to_return


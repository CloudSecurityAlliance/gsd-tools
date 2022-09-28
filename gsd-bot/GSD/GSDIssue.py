
import requests
import os
import json
import re

class Issue:
    def __init__(self, details):

        self.raw_data = details
        self.lines = details['body'].splitlines()
        self.comments_url = details['comments_url']
        self.events_url = details['events_url']
        self.url = details['url']
        self.html_url = details['html_url']
        self.title = details['title']
        self.id = details['number'];    
        self.creator = details['user']['login']
        self.creator_id = details['user']['id']
        self.auth = (os.environ['GH_USERNAME'], os.environ['GH_TOKEN'])

    def get_gsd_id(self):
        # We are going to only trust the comment from <username> for this
        # ID. It's the most trustworthy ID

        comments = self.get_comments()
        comments.reverse()
        for i in comments:
            if i['user']['login'] == os.environ['GH_USERNAME']:
                if i['body'].startswith('This issue has been assigned'):
                    match = re.search('((GSD|CAN)-\d{4}-\d+)', i['body'])
                    gsd_id = match.groups()[0]
                    return gsd_id
        return None

    def get_events(self):

        events = []
        page = 0
        while(True):
            params = {
                    'per_page': 100,
                    'page': page
            }
            resp = requests.get(self.events_url, auth=self.auth, params=params)
            resp.raise_for_status()
            if len(resp.json()) == 0:
                break
            else:
                page = page + 1
                events.extend(resp.json())

        return events

    def get_comments(self):
        comments = []
        page = 0
        while(True):
            params = {
                    'per_page': 100,
                    'page': page
            }
            resp = requests.get(self.comments_url, auth=self.auth, params=params)
            resp.raise_for_status()
            if len(resp.json()) == 0:
                break
            else:
                page = page + 1
                comments.extend(resp.json())

        return comments

    def who_approved(self):
        events = self.get_events()
        # We should reverse the list as we want to figure out who gave the last approval
        events.reverse()
        for i in events:
            # I'm pretty sure we need better logic here
            if i['event'] == 'labeled' and i['label']['name'] == 'approved':
                approver = i['actor']['login']
                approver_id = i['actor']['id']
                return "%s:%s" % (approver, approver_id)

    def get_reporter(self):
        data = self.get_gsd_json()
        the_reporter = "%s:%s" % (data['reporter'], data['reporter_id'])
        return the_reporter

    def get_gsd_json(self):
        gsd_json = ""
        found_json = False

        for l in self.lines:
            if l == "--- GSD JSON ---":
                found_json = not found_json
            elif found_json is True:
                gsd_json = gsd_json + l

        gsd_data = json.loads(gsd_json)
        return gsd_data

    def add_comment(self, comment):
        body = {
            "body": comment
        }

        headers = {
            "accept": "application/json"
        }

        resp = requests.post(self.comments_url, json=body, auth=self.auth, headers=headers)
        resp.raise_for_status()

    def can_to_gsd(self):
        can_id = self.get_gsd_id()
        # Make sure the ID starts with CAN
        if not can_id.startswith('CAN-'):
            return None

        # Get the path to the file
        year = can_id.split('-')[1]
        id_str = can_id.split('-')[2]
        gsd_id = "GSD-%s-%s" % (year, id_str)

        self.title = self.title.replace(can_id, gsd_id)
        body = {
            "title": self.title,
            "state": "closed"
        }
        headers = {
            "accept": "application/json"
        }
        resp = requests.post(self.url, json=body, auth=self.auth, headers=headers)
        resp.raise_for_status()

    def assign_gsd(self, gsd_id, approved_user = False):

        # Add a comment to the issue
        self.add_comment("This issue has been assigned %s" % gsd_id)

                # Modify the title and labels
        body = {
            "title": "[%s] %s" % (gsd_id, self.title),
            "labels": ["assigned"]
        }

        headers = {
            "accept": "application/json"
        }

        if approved_user:
            body["state"] = "closed"
        else:
            # CAN IDs get the candidate label
            body["labels"] = ["assigned", "candidate"]

        resp = requests.post(self.url, json=body, auth=self.auth, headers=headers)
        resp.raise_for_status()


import tempfile
import git
import os
import json
import datetime

class GSDRepo:
    def __init__(self, repo_url, testing=False):

        self.testing = testing
        self.tmpdir = tempfile.TemporaryDirectory()
        self.repo = git.Repo.clone_from(repo_url, self.tmpdir.name)
        allow_list_files = os.path.join(self.tmpdir.name, "allowlist.json")
        with open(allow_list_files) as json_file:
            self.allowed_users = json.loads(json_file.read())

    def approved_user(self, user='', user_name=None, user_id=None):
        if user_name is not None and user_id is not None:
            user="%s:%s" % (user_name, user_id)
        return user in self.allowed_users

    def update_id(self, the_id, the_data):

        # If we get a CAN, we want a GSD filename
        if 'CAN' in the_id:
            the_id = the_id.replace("CAN", "GSD")

        the_filename = self.get_file(the_id)

        gsd_json = json.dumps(the_data, indent=2)
        gsd_json = gsd_json + "\n"
        # save the json
        with open(the_filename, 'w') as json_file:
            json_file.write(gsd_json)
        self.repo.index.add(the_filename)

    def can_to_gsd(self, gsd_issue):

        can_id = gsd_issue.get_gsd_id()
        # Make sure the ID starts with CAN
        if not can_id.startswith('CAN-'):
            return None

        # Get the path to the file
        year = can_id.split('-')[1]
        id_str = can_id.split('-')[2]
        namespace = "%sxxx" % id_str[0:-3]
        gsd_id = "GSD-%s-%s" % (year, id_str)
        filename = "%s.json" % (gsd_id)

        can_file = os.path.join(year, namespace, filename)
        git_file = os.path.join(self.repo.working_dir, can_file)

        # Open the file
        with open(git_file) as json_file:
                # Read the json
                can_data = json.loads(json_file.read())

        # Swap the CAN to GSD
        can_data['OSV']['id'] = gsd_id

        # save the json
        self.update_id(gsd_id, can_data)

        # Commit the file
        self.repo.index.add(can_file)
        self.commit("Promoted to %s for #%s" % (gsd_id, gsd_issue.id))
        self.push()
        return gsd_id

    def add_gsd(self, gsd_issue):

        gsd_data = gsd_issue.get_gsd_json()

        # Check the allowlist
        reporter = gsd_issue.get_reporter()

        approved_user = self.approved_user(reporter)

        (gsd_id, gsd_path) = self.get_next_gsd_path(approved_user)

        new_gsd_data = self.get_gsd_json_format(gsd_id, gsd_data)
        gsd_json = json.dumps(new_gsd_data, indent=2)
        gsd_json = gsd_json + "\n"

        with open(os.path.join(self.repo.working_dir, gsd_path), 'w') as json_file:
            json_file.write(gsd_json)

        self.repo.index.add(gsd_path)
        self.commit("Add %s for %s" % (gsd_id, gsd_issue.html_url))
        self.push()

        return gsd_id

    def commit(self, message):
        # Don't commit if we're testing
        if self.testing:
            pass
        else:
            self.repo.index.commit(message)

    def push(self):
        # Don't push if we're testing
        if self.testing:
            pass
        else:
            self.repo.remotes.origin.push()

    def close(self):
        self.tmpdir.cleanup()

    def get_id(self, the_id):
        the_data = None
        id_path = self.get_file(the_id)
        with open(id_path) as fh:
            the_data = json.load(fh)
        return the_data

    def get_file(self, the_id):
        (year, id_only) = the_id.split('-')[1:3]
        block_num = int(int(id_only)/1000)
        block_path = "%dxxx" % block_num
        id_path = os.path.join(self.tmpdir.name, year, block_path, the_id + ".json")
        return id_path

    def get_all_ids(self):

        gsd_ids = []
        for root,d_names,f_names in os.walk(self.tmpdir.name):
            # Skip the .git directories
            if '.git' in root:
                continue

            for i in f_names:
                if 'GSD-' in i:
                    id_only = i.split('.')[0]
                    gsd_ids.append(id_only)
        return gsd_ids

    def get_next_gsd_path(self, approved_user = False):
        # Returns the next GSD ID and the path where it should go
        # This needs a lot more intelligence, but it'll be OK for the first pass. There are plenty of integers
        gsd_path = None
        the_gsd = None

        # Get the current year
        year = str(datetime.datetime.now().year)
        year_dir = os.path.join(self.tmpdir.name, year)

        # Make sure the year directory exists
        if not os.path.exists(year_dir):
            os.mkdir(year_dir)

        # Start looking in directory 1000xxx
        # If that's full, move to 1001xxx
        # We will consider our namespace everything up to 1999999
        for i in range(1000, 2000, 1):
            block_dir = "%sxxx" % i
            block_path = os.path.join(year_dir, block_dir)
            if not os.path.exists(block_path):
                # This is a new path with no files
                os.mkdir(block_path)
                the_gsd = "GSD-%s-%s000" % (year, i)
                gsd_path = os.path.join(block_path, "%s.json" % the_gsd)
                if not approved_user:
                    the_gsd = "CAN-%s-%s000" % (year, i)
                break

            else:
                files = os.listdir(block_path)
                files.sort()
                last_file = files[-1]
                id_num = int(last_file.split('.')[0].split('-')[2])
                next_id = id_num + 1
                if next_id % 1000 == 0:
                    # It's time to roll over, we'll pick up the ID in the next loop
                    continue

                the_gsd = "GSD-%s-%s" % (year, next_id)
                gsd_path = os.path.join(block_path, "%s.json" % the_gsd)
                if not approved_user:
                    the_gsd = "CAN-%s-%s" % (year, next_id)
                break

        return (the_gsd, gsd_path)

    def get_osv_json_format(self, gsd_id, issue_data):

        # The OSV format is nice. Find out more here
        # https://osv.dev/docs/#tag/vulnerability_schema
        the_time =  datetime.datetime.utcnow().isoformat() + "Z"

        c = {};

        c["id"] = gsd_id
        c["modified"] = the_time
        c["published"] = the_time

        # Schema version hint
        c["schema_version"] = "1.4.0"

        # Per discussion with @kurtsefried, moving this to gsd->metadata
        # c["credits"] = [{
        #     "name": issue_data["reporter"] + ':' + issue_data["reporter_id"],
        #     "contact": ["https://github.com/%s" % issue_data["reporter"]],
        #     "type": "REPORTER"
        # }]

        vuln_type = issue_data["vulnerability_type"]
        name = issue_data["product_name"]
        version = issue_data["product_version"]
        summary = f"{vuln_type} in {name} version {version}"
        c["summary"] = summary
        c["details"] = issue_data["description"]

        c["affected"] = [{
            "package": {
                "name": issue_data["product_name"],
                "ecosystem": "GSD"
            },
            # We will need to remove a version or ranges below, there can
            # be only one!
            "ranges": [{
                "type": "",
                "repo": "",
                "events": [{}, {}]
            }],
            "versions": []
        }]

        # XXX: This needs to be done in a better way long term
        if issue_data["product_name"] == "Kernel" and \
           issue_data["vendor_name"] == "Linux" and \
           issue_data["impact"] == "unspecified":

            # The kernel summary is special
            c["summary"] = issue_data["description"].split('\n')[0]

            # We are dealing with the kernel, skip references and use git
            # commits in the affected section
            c["affected"][0]["package"]["ecosystem"] = "Linux"

            c["affected"][0]["ranges"][0]["type"] = "GIT"
            c["affected"][0]["ranges"][0]["repo"] = "https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/"

            # Find the kernel fixed and introduced fields
            c["affected"][0]["ranges"][0]["events"][0]["introduced"] = "0"
            c["affected"][0]["ranges"][0]["events"][1]["limit"] = ""
            del(c["affected"][0]["versions"])

            for i in issue_data["extended_references"]:
                if i["type"] != "commit":
                    # XXX We need some exceptions
                    raise Exception("Unknown kernel reference")


                if i["note"] == "introduced":
                    c["affected"][0]["ranges"][0]["events"][0]["introduced"] = i["value"]
                elif i["note"] == "fixed":
                    c["affected"][0]["ranges"][0]["events"][1]["limit"] = i["value"]
                else:
                    raise Exception("Unknown kernel note")

            c["references"] = []
            for i in issue_data["references"]:
                c["references"].append({"type": "WEB", "url": i})

            c["affected"].append({
                "package": {
                    "name": "Kernel",
                    "ecosystem": "Linux"
                },
                "ranges": [{
                    "type": "SEMVER",
                    "repo": "https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/",
                    "events": [{"introduced": issue_data["introduced_version"]}, {"fixed": issue_data["fixed_version"]}]
                }]
            })
        else:
            # We're not looking at kernel issues
            del(c["affected"][0]["ranges"])
            c["affected"][0]["versions"] = [
                    issue_data["product_version"]
            ]
            c["references"] = []
            for i in issue_data["references"]:
                c["references"].append({"type": "WEB", "url": i})

        return c

    def get_gsd_json_format(self, gsd_id, issue_data):

        c = {}
        c["gsd"] = {}
        c["gsd"]["metadata"] = {
            "type": "concern",
            "exploitCode": "unknown",
            "remediation": "official",
            "reportConfidence": "confirmed",
            "reporter": issue_data["reporter"],
            "reporter_id": issue_data["reporter_id"]
        }
        c["gsd"]["osvSchema"] = self.get_osv_json_format(gsd_id, issue_data)
        return c


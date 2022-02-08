# Module for getting GitLab Community Advisories
#

import requests
import tarfile
import yaml
from io import BytesIO

class UnexpectedResults(Exception):
    pass

class GitLab:

    def fetch(self):
        b = BytesIO(requests.get("https://gitlab.com/gitlab-org/advisories-community/-/archive/main/advisories-community-main.tar.gz").content)
        results = {}

        with tarfile.open(fileobj=b, mode="r:gz") as t:
            for file in t:
                if file.name.endswith(".yml"):
                    extracted = t.extractfile(file.name)

                    if extracted:
                        advisory = yaml.safe_load(t.extractfile(file.name).read())
                    
                        identifiers = advisory.get("identifiers")

                        if not identifiers:
                            # The identifier field is deprecated and should be replaced by a list of identifiers; however, 
                            # some of the older advisories appear not to have the new field, so we create it from the old one
                            identifier = advisory.get("identifier")

                            if identifier:
                                advisory["identifiers"] = [identifier]
                                identifiers = ["identifiers"]

                        if identifiers:
                            for i in identifiers:
                                if i.startswith("CVE-"):
                                    if i not in results:
                                        results[i] = { "advisories": [] }

                                    results[i]["advisories"].append(advisory)
                                    break

        return results

#!/usr/bin/env python3

import json
import re

# TODO: take a command line argument of a file with new Debian URLs, check for "debian.org" and process?

#
# Process www.debian.org file and pass back all the whitelisted URLs we know how to handle
# TODO: whitelist (URL's we know how to handle), blacklist (URL's to be avoided), ignorelist (URL's we don't care about), and the greylist (unknonwn, need attention)
#
from pathlib import Path
home = str(Path.home())
config_file = home + '/.uvi/config.json'

with open(config_file) as config_data:
  uvi_config = json.load(config_data)

global_url_list = uvi_config["global"]["uvi_url_list_repo"] + "/data/www.debian.org"

#
# Does this site now use HTTPS by default (some still don't)
#
global_site_uses_https=True

#
# Read the file, lines = urls = entries in a dict
# then walk the dict and normalize stuff and write to the same dict?
# if changed/removed delete that key?
# then check if we already have the data in https://github.com/cloudsecurityalliance/uvi-url-downloads
# and the check time and so on
#

global_url_data={}

with open(global_url_list) as file:
    for line in file:
        processed_url=line.rstrip()

        # Start processing the data
        # 1) http -. https normalization if True
        # ignore ftp/etc. for know
        if global_site_uses_https == True:
            if re.match("^http:", processed_url):
                processed_url = re.sub("^http:", "https:", processed_url)

        # DSA - remove translations
        # https://www.debian.org/security/2014/dsa-2906
        # https://www.debian.org/security/2014/dsa-2906.da.html
        if re.match("^https://www\.debian\.org/security/[1-2][0-9][0-9][0-9]/dsa-[0-9]*\.[a-z][a-z]\.html$", processed_url):
            processed_url = re.sub("\.[a-z][a-z]\.html$", "", processed_url)
            global_url_data[processed_url] = ""

        # Regular DSA's we want
        # https://www.debian.org/security/2014/dsa-2906
        if re.match("^https://www\.debian\.org/security/[1-2][0-9][0-9][0-9]/dsa-[0-9]*$", processed_url):
            global_url_data[processed_url] = ""

        # DSA undated - matches all and removes translations
        # 1* removes /, /index, /index.html
        if re.match("^https://www.debian.org/security/undated/1.*", processed_url):
            processed_url = re.sub("\.[a-z][a-z]\.html$", "", processed_url)
            global_url_data[processed_url] = ""
        # DSA pre DSA - remove translations
        # https://www.debian.org/security/1997/19970417
        # https://www.debian.org/security/1997/19970325a
        if re.match("^https://www\.debian\.org/security/[1-2][0-9][0-9][0-9]/[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][a-z]*\.[a-z][a-z]\.html", processed_url):
            processed_url = re.sub("\.[a-z][a-z]\.html$", "", processed_url)
            global_url_data[processed_url] = ""

        #if re.match("^https://www.debian.org/security/[1-2][0-9][0-9][0-9]/$", processed_url):
            # list of DSA's by year, not useful since we have "date reported" in the files

        # If we don't explicitly know how to handle the URL, ignore it for now

# Debugging
for key, value in global_url_data.items():
    print(key)

# The above normalizes the Debian stuff down to 3500+ URLS from 40000+

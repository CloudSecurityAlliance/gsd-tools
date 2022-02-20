#!/usr/bin/env python3

#
# Testing URLS
# https://www.debian.org/security/2016/dsa-3710
# https://www.debian.org/security/2016/dsa-3740
# https://www.debian.org/security/2016/dsa-3657
# https://www.debian.org/security/2020/dsa-4794
# https://www.debian.org/security/2019/dsa-4573
# https://www.debian.org/security/2019/dsa-4564
# https://www.debian.org/security/2021/dsa-4936
# https://www.debian.org/security/2021/dsa-4904
# https://www.debian.org/security/2021/dsa-4902
# https://www.debian.org/security/2021/dsa-4885
#
import sys

uvi_script_version = "0.0.1"
uvi_script_name = sys.argv[0]

import hashlib
# Requires Python 3.5 or later
from pathlib import Path
import json
import datetime
import re
import calendar
import os



with open(uvi_script_name,"rb") as f:
    bytes = f.read() # read entire file as bytes
    uvi_script_hash = hashlib.sha512(bytes).hexdigest();

#
# Processa file with a list of URLs
#
global_url_list = sys.argv[1]

#
# Get the ~/.uvi/config.json and read it into uvi_config
#
from pathlib import Path
home = str(Path.home())
config_file = home + '/.uvi/config.json'
with open(config_file) as config_data:
  uvi_config = json.load(config_data)
global_uvi_url_downloads = uvi_config["global"]["uvi_url_downloads_repo"]
global_uvi_database_test = uvi_config["global"]["uvi_database_test"]
#
# Start at 20 million
#
UVI_ID = 20000000
UVI_YEAR = 2021

def UVI_ID_file_location(local_UVI_ID):
    # returns the UVI ID file location and makes the interim directories if they do not exist
    filename = "UVI-" + str(UVI_YEAR) + "-" + str(local_UVI_ID) + ".json"
    sub_directory = re.sub("[0-9][0-9][0-9]$", "xxx", str(local_UVI_ID))
    file_directory_sub = global_uvi_database_test + "/" + str(UVI_YEAR) + "/" + str(sub_directory)
    if not os.path.exists(file_directory_sub):
        os.makedirs(file_directory_sub)
    file_path = global_uvi_database_test + "/" + str(UVI_YEAR) + "/" + str(sub_directory) + "/" + filename
    return file_path

def write_UVI_ID_file(local_UVI_ID, local_UVI_ID_DATA):
    file_path_is = UVI_ID_file_location(local_UVI_ID)
    f = open(file_path_is, "w")
    f.write(json.dumps(local_UVI_ID_DATA, indent=4, sort_keys=True))
    f.close()

#
# Take a URL, SHA512, find the path to the extracted data
#

with open(global_url_list) as file:
    for line in file:

        # TODO: add check for blank line and ignore?
        # "" cf83e1357eefb8bdf1542850d66d8007d620e4050b5715dc83f4a921d36ce9ce47d0d13c5d85f2b0ff8318d2877eec2f63b931bd47417a81a538327af927da3e
        timestamp = datetime.datetime.utcnow() # <-- get time in UTC
        processed_timestamp = timestamp.isoformat("T") + "Z"
        url = line.rstrip()
        url_bytes = url.encode()
        h = hashlib.sha512()
        h.update(url_bytes)
        url_hash = h.hexdigest()
        url_hash_1 = url_hash[0:2]
        url_hash_2 = url_hash[2:4]
        url_hash_3 = url_hash[4:6]
        url_hash_4 = url_hash[6:8]

        url_directory = global_uvi_url_downloads + "/data/" + url_hash_1 + "/" + url_hash_2 + "/" + url_hash_3 + "/" + url_hash_4 + "/" + url_hash
        url_extracted_data_file = url_directory + "/extracted_data.json"

        number_of_aliases = 1
        CVE_FOUND = False

        processed_timestamp = timestamp.isoformat("T") + "Z"

        with open(url_extracted_data_file) as data_file:
            extracted_data = json.load(data_file)
            for aliases in extracted_data["uvi"][0]["extracted_data"]["aliases"]:
                if aliases["namespace"] == "cve.mitre.org":
                    if len(aliases["ids"]) == 0:
                        CVE_FOUND = False
                        UVI_DATA={
                            "UVI_ID" : UVI_ID,
                            "meta_data": {
                                "uvi_processed_timestamp": processed_timestamp,
                                "uvi_script_hash": uvi_script_hash,
                                "uvi_script_name": uvi_script_name,
                                "uvi_script_version": uvi_script_version,
                                "source" : {
                                    "uvi_url_processed": url,
                                    "meta_data": extracted_data["uvi"][0]["meta_data"]
                                }
                            },
                            "aliases" : [
                                {
                                    "namespace": "www.debian.org",
                                    "ids": extracted_data["uvi"][0]["extracted_data"]["advisory_id"]
                                }
                            ]
                        }
                        write_UVI_ID_file(UVI_ID, UVI_DATA)
                        UVI_ID = UVI_ID + 1
                    else:
                        for CVE_ID in aliases["ids"]:
                            CVE_FOUND = True
                            UVI_DATA={
                                "UVI_ID" : UVI_ID,
                                "meta_data": {
                                    "uvi_processed_timestamp": processed_timestamp,
                                    "uvi_script_hash": uvi_script_hash,
                                    "uvi_script_name": uvi_script_name,
                                    "uvi_script_version": uvi_script_version,
                                    "source" : {
                                        "uvi_url_processed": url,
                                        "meta_data": extracted_data["uvi"][0]["meta_data"]
                                    }
                                },
                                "aliases" : [
                                    {
                                        "namespace": "cve.mitre.org",
                                        "ids": CVE_ID
                                    },
                                    {
                                        "namespace": "www.debian.org",
                                        "ids": extracted_data["uvi"][0]["extracted_data"]["advisory_id"]
                                    }
                                ]
                            }
                            write_UVI_ID_file(UVI_ID, UVI_DATA)
                            UVI_ID = UVI_ID + 1



            #print(json.dumps(extracted_data, indent=4, sort_keys=True))
#            f = open(url_extracted_data_file, "w")
#            f.write(json.dumps(extracted_data, indent=4, sort_keys=True))
#            f.close()

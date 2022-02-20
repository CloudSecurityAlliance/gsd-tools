#!/usr/bin/env python3

import hashlib
# Requires Python 3.5 or later
from pathlib import Path

import requests
from requests.exceptions import RequestException
import json
import datetime
import sys
import os

uvi_script_version = "0.0.3"
uvi_script_name = sys.argv[0]

#
# Processa file with a list of URLs
#
global_url_list = sys.argv[1]


#
# Get the ~/.uvi/config.json and read it into uvi_config
#
home = str(Path.home())
config_file = home + '/.uvi/config.json'
with open(config_file) as config_data:
  uvi_config = json.load(config_data)
global_uvi_url_downloads = uvi_config["global"]["uvi_url_downloads_repo"] + "/data/"

#global_uvi_url_downloads = "/mnt/c/GitHub/uvi-url-downloads/data"

with open(global_url_list) as file:
    for line in file:
        already_seen = False
        url = line.rstrip()
        url_bytes = url.encode()
        h = hashlib.sha512()
        h.update(url_bytes)
        url_hash = h.hexdigest()
        url_hash_1 = url_hash[0:2]
        url_hash_2 = url_hash[2:4]
        url_hash_3 = url_hash[4:6]
        url_hash_4 = url_hash[6:8]

        url_directory = global_uvi_url_downloads + "/" + url_hash_1 + "/" + url_hash_2 + "/" + url_hash_3 + "/" + url_hash_4 + "/" + url_hash
        
        url_directory_raw_data=url_directory + "/raw-data"
        response_data_file = url_directory + "/response.json"

        filepath_response_data_file = Path(response_data_file)
        if filepath_response_data_file.is_file():
            already_seen = True
            print("already seen")
        else:
            Path(url_directory_raw_data).mkdir(parents=True, exist_ok=True)
            print(url)
        #
        # TODO            
        # if already_seen == True:
        #
        # Logic to check timestamp and get again if over X timestamp

        if already_seen == False:
            timestamp = datetime.datetime.utcnow() # <-- get time in UTC
            request_timestamp = timestamp.isoformat("T") + "Z"

            request_succeeded = False
            request_error = ""
            try:
              # get file
              response = requests.get(url, allow_redirects=True, timeout=10)
              request_succeeded = True
            except requests.exceptions.RequestException as request_error:  # This is the correct syntax
              get_request_error = str(request_error)
              request_succeeded = False


            # Only print a response body to the file if it worked
            if request_succeeded == True:
              #response_dict = json.loads(response.text)
              response_file = url_directory_raw_data + "/server_response.data"
              f = open(response_file, "wb")
              f.write(response.content)
              f.close()
            #
            # Request file data ALWAYS WRITE
            #
            request_data_file = url_directory + "/request.json"
            request_data = {
              "URL_requested": url,
              "TIMESTAMP": request_timestamp,
              "uvi_script_name": uvi_script_name,
              "uvi_script_version": uvi_script_version
            }
            f = open(request_data_file, "w")
            f.write(json.dumps(request_data, indent=4, sort_keys=True))
            f.close()
            #
            # Remove old txt file if exists
            #
            request_data_file_txt = url_directory + "/request.txt"
            if os.path.exists(request_data_file_txt):
              os.remove(request_data_file_txt)
            #
            # Response file data
            #
            # TODO: add logic, check if request_error is not "" and write http error otherwise right the proper file:
            #
            #response_data_file = url_directory + "/response.json"
            f = open(response_data_file, "w")

            # IF ERROR
            if request_succeeded == False:
              response_data = {
                "error": get_request_error
                }
            if request_succeeded == True:
              # IF NO ERROR
              response_data = {
                "elapsed": str(response.elapsed),
                "is_redirect": str(response.is_redirect),
                "status_code": str(response.status_code),
                "url": response.url,
                "response_file": response_file
              }
              
            f.write(json.dumps(response_data, indent=4, sort_keys=True))
            f.close()
            #
            # Remove old txt file if exists
            #
            response_data_file_txt = url_directory + "/response.txt"
            if os.path.exists(response_data_file_txt):
              os.remove(response_data_file_txt)


          

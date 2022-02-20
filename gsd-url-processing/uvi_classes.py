#!/usr/bin/env python3

import os
import json

# UVI python template files

# Config file - JSON, ~/.uvi/config.json

class uvi_user_config():

    # config = uvi_user_config()
    # config_values = uvi_user_config.read_config_file()

    def read_config_file():
        user_config_file = os.path.expanduser("~") + "/.uvi/config.json"
        if os.path.isfile(user_config_file):
            with open(user_config_file) as f:
                user_config = json.load(f)
            return(user_config)
        else:
            #
            # Remember to update this as we add things to the config file
            #
            error_msg = """
            Please create a JSON ~/.uvi/config.json config file, for example on Ubuntu/Windows host:
            {
                "uvi-url-processing_repo_dir": "/mnt/c/GitHub/uvi-url-processing",
                "uvi-url-list_repo_dir": "/mnt/c/GitHub/uvi-url-list",
                "uvi-url-downloads_repo_dir": "/mnt/c/GitHub/uvi-url-downloads",
                "uvi-database_repo_dir": "/mnt/c/GitHub/uvi-database",
                "uvi-tools_repo_dir": "/mnt/c/GitHub/uvi-tools",
                "github_username": "",
                "github_api_token": ""
            }
            """
            print(error_msg)
            print
            return(False)
    def create_config_file():
        foo = 1
    def write_config_file(key_name, data_value):
        foo = 2

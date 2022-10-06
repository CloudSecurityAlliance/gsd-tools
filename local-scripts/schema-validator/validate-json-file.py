#!/usr/bin/env python3

import sys
import json
import re
import os
from jsonschema import Draft202012Validator

# Works on GSD-YEAR-INTEGER (OSV, CVE 4.0, CVE 5.0)
# Works on CVE-YEAR-INTEGER (CVE 4.0, CVE 5.0)
# Works on GHSA's (OSV)

# Apply OSV schema to GSD {gsd: CONTENT}
# Apply CVE schema to GSD {namespaces: cve.org AND nvd.nist.gov}
# Apply CVE schema

# Read the ~/.gsdconfig file, e.g.:
#{
#	"gsd_database_path": "/home/kurt/GitHub/gsd-database/",
#	"gsd_tools_path": "/home/kurt/GitHub/gsd-tools/"
#}
def setgsdconfigGlobals():
    # Set gsdconfig globals like pathnames
    # TODO: check for trailing slash at some point
    user_homedir_path = os.path.expanduser('~')
    gsdconfig_path = user_homedir_path + "/.gsdconfig"
    global gsd_database_path
    global gsd_tools_path
    if os.path.exists(gsdconfig_path): 
        with open(gsdconfig_path, "r") as f:
            gsdconfig_data = json.load(f)
        gsd_database_path = gsdconfig_data["gsd_database_path"]
        gsd_tools_path = gsdconfig_data["gsd_tools_path"]
    else:
        print("no ~/.gsdconfig file set, please create one, see comments in this script for details")
        exit()

# Take the command line argument and figure out if it's a GSD/CVE/file path, and convert to a file path
# Valid arguments are:
# CVE-YEAR-INTEGER
# GSD-YEAR-INTEGER
# ./YEAR/INTxxx/GSD-YEAH-INTEGER.json
#
# Output is a global file path or exit if error

def convertArgumentToPath(argv1):
    if re.match("^CVE-[0-9][0-9][0-9][0-9]-[0-9][0-9][0-9][0-9]*$", argv1):
        argv1 = re.sub("^CVE-", "GSD-", argv1)
    if re.match("^GSD-[0-9][0-9][0-9][0-9]-[0-9][0-9][0-9][0-9]*$", argv1):
        gsd_id_data = argv1.split("-")
        year = gsd_id_data[1]
        integer = gsd_id_data[2]
        integerdir = re.sub("[0-9][0-9][0-9]$", "xxx", integer)
        argv1 = "./" + year + "/" + integerdir + "/" + argv1 + ".json"
        # Convert to partial path
    if re.match("^\./[0-9][0-9][0-9][0-9]/[0-9]*xxx/GSD-[0-9][0-9][0-9][0-9]-[0-9][0-9][0-9][0-9]*.json", argv1):
        argv1 = re.sub("^\./", gsd_database_path, argv1)
    global gsd_file_path
    gsd_file_path = argv1



#########################################################

def detectFileTypeByName(filename):
    if re.match("^CVE-[0-9][0-9][0-9][0-9]-[0-9]*\.json$", filename):
        return("CVE")
    elif re.match("^GSD-[0-9][0-9][0-9][0-9]-[0-9]*\.json$", filename):
        return("GSD")
    elif re.match("^GHSA-[0-9a-z][0-9a-z][0-9a-z][0-9a-z]-[0-9a-z][0-9a-z][0-9a-z][0-9a-z]-[0-9a-z][0-9a-z][0-9a-z][0-9a-z]\.json$", filename):
        return("OSV")
    else:
        print("ERROR: " + filename + " NOT RECOGNIZED")
        quit()

#########################################################

def extractDataAndSchema(filetype, data):
    # Returns an array of 0 or more entries in the form {key:name, schema:foo, process_data:data}
    # Quietly ignores anything we don't explicitly understand
    results = []
    if filetype == "GSD":
        if "gsd" in data:
            process_data = data["gsd"]

            local_results = {}
            local_results["key"] = "gsd"
            schema_type = "OSV"
            if "schema_version" in process_data:
                schema_version = process_data["schema_version"]
            else:
                # Default to latest if not specified I guess?
                schema_version = "1.3.0"
            schema = schema_type + "_" + schema_version
            local_results["schema"] = schema
            local_results["process_data"] = process_data
            results.append(local_results)
        # This needs to go away
        if "OSV" in data:
            process_data = data["OSV"]

            local_results = {}
            local_results["key"] = "OSV"
            schema_type = "OSV"
            if "schema_version" in process_data:
                schema_version = process_data["schema_version"]
            else:
                # Default to latest if not specified I guess?
                schema_version = "1.3.0"
            schema = schema_type + "_" + schema_version
            local_results["schema"] = schema
            local_results["process_data"] = process_data
            results.append(local_results)
        # This also needs to go away
        if "GSD" in data:
            process_data = data["GSD"]

            local_results = {}
            local_results["key"] = "GSD"
            schema_type = "OSV"
            if "schema_version" in process_data:
                schema_version = process_data["schema_version"]
            else:
                # Default to latest if not specified I guess?
                schema_version = "1.3.0"
            schema = schema_type + "_" + schema_version
            local_results["schema"] = schema
            local_results["process_data"] = process_data
            results.append(local_results)
        if "namespaces" in data:
            if "cve.org" in data["namespaces"]:
                process_data = data["namespaces"]["cve.org"]

                local_results = {}
                local_results["key"] = "cve.org"
                schema_type = process_data["data_type"]
                schema_version = process_data["data_version"]
                if schema_version == "4.0":
                    schema_state = process_data["CVE_data_meta"]["STATE"]
                    schema = schema_type + "_" + schema_version + "_" + schema_state
                elif schema_version == "5.0":
                    schema = schema_type + "_" + schema_version
                local_results["schema"] = schema
                local_results["process_data"] = process_data
                results.append(local_results)
                process_data = data["namespaces"]["cve.org"]

            if "nvd.nist.gov" in data["namespaces"]:
                # need to figure out how to handle all the file includes
                #
                #   File "/usr/local/lib/python3.8/dist-packages/jsonschema/validators.py", line 800, in resolve_from_url
                #   raise exceptions.RefResolutionError(exc)
                #   jsonschema.exceptions.RefResolutionError: unknown url type: '/CVE_JSON_4.0_min_1.1_beta.schema'  
                #
                # https://python-jsonschema.readthedocs.io/en/stable/faq/#how-do-i-configure-a-base-uri-for-ref-resolution-using-local-files
                # 
                #
                schema = "nvd_cve_feed_json_1.1_beta.schema"
                process_data = {}
                process_data["CVE_data_type"] = "CVE"
                process_data["CVE_data_format"] = "MITRE"
                process_data["CVE_data_version"] = "4.0"
                process_data["CVE_data_numberOfCVEs"] = "1563"
                process_data["CVE_data_timestamp"] = "2022-09-29T00:00Z"
                process_data["CVE_Items"] = []
                process_data["CVE_Items"].append(data["namespaces"]["nvd.nist.gov"])

                #process_data = data["namespaces"]["nvd.nist.gov"]
                local_results = {}
                local_results["key"] = "nvd.nist.gov-cve"
                local_results["schema"] = schema
                local_results["process_data"] = process_data
                # IGNORE THE NVD DATA FOR NOW SINCE WE NEED MULTIPLE PARSERS
                #
                # results.append(local_results)
                #

    elif filetype == "CVE":
        process_data = data

        local_results = {}
        local_results["key"] = "CVE"
        schema_type = process_data["data_type"]
        schema_version = process_data["data_version"]
        if schema_version == "4.0":
            schema_state = process_data["CVE_data_meta"]["STATE"]
            schema = schema_type + "_" + schema_version + "_" + schema_state
        elif schema_version == "5.0":
            schema = schema_type + "_" + schema_version
        local_results["schema"] = schema
        local_results["process_data"] = process_data
        results.append(local_results)

    elif filetype == "OSV":
        process_data = data

        local_results = {}
        local_results["key"] = "OSV"
        schema_type = "OSV"
        if "schema_version" in process_data:
            schema_version = process_data["schema_version"]
        else:
            # Default to latest if not specified I guess?
            schema_version = "1.3.0"
        schema = schema_type + "_" + schema_version
        local_results["schema"] = schema
        local_results["process_data"] = process_data
        results.append(local_results)
    return(results)

#########################################################

def validateJsonSchema(data):
    # data is an array of 0 or more entries in the form {key:name, schema:foo, process_data:data}
    #
    if data == []:
        print("ERROR: no data to parse")
        quit()
    print("###########################################################################")
    print("FILENAME: " + file_name)

    for item in data:
        print("########################################")
        print(item["key"])

        # Get the schema, we might not have the correct version, if so bail out
        # Also make this work from wherever we call it
        program_filepath = os.path.dirname(__file__)
        schema_file_name = "schema-" + item["schema"] + ".json"
        schema_file_location = os.path.join(program_filepath, schema_file_name)

        try:
            with open(schema_file_location) as schema_file:
                schema_data = json.load(schema_file)
        except IOError:
            print("ERROR: Schema file not found: " + schema_file_location)
            quit()

        instance_data = item["process_data"]

        # TODO: To support NVD we need to add the base URI stuff as per
        # https://python-jsonschema.readthedocs.io/en/stable/faq/#how-do-i-configure-a-base-uri-for-ref-resolution-using-local-files

        v = Draft202012Validator(schema_data)
        errors = sorted(v.iter_errors(instance_data), key=lambda e: e.path)
        if errors == []:
            print("DATA PARSED CLEAN")
        else:
            for error in errors:
                print("####################")
                print(error.message)
#                print("#####")
#                print(error.context)
#                print("#####")
#                print(error.cause)
#                print("#####")
#                print(error.instance)
#                print("#####")
#                print(error.json_path)
#                print("#####")
#                print(error.path)
#                print("#####")
#                print(error.schema)
#                print("#####")
#                print(error.schema_path)
#                print("#####")
#                print(error.validator)
#                print("#####")
#                print(error.validator_value)

if __name__ == "__main__":

    setgsdconfigGlobals()
    # gsd_database_path
    # gsd_tools_path

    convertArgumentToPath(sys.argv[1])
    # gsd_file_path

    file_name = os.path.basename(gsd_file_path)


    # GSD or CVE
    file_type = detectFileTypeByName(file_name)

    with open(gsd_file_path, "r") as f:
        file_data = json.load(f)
        f.close()

    # Get an array of schema and data, 0 or more entries
    extracted_data = extractDataAndSchema(file_type, file_data)

    # Validate the JSON data items
    validateJsonSchema(extracted_data)

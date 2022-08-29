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
                #
                # This will actually need multiple entries, e.g. the CVE data, CVSS data and so on
                # See https://nvd.nist.gov/general/News/JSON-1-1-Vulnerability-Feed-Release for reference
                #
                process_data = data["namespaces"]["nvd.nist.gov"]

                local_results = {}
                local_results["key"] = "nvd.nist.gov"
                schema_type = process_data["cve"]["data_type"]
                schema_version = process_data["cve"]["data_version"]
                if schema_version == "4.0":
                    # NVD doesn't have the state so we need to add a check for PUBLIC / REJECT based on description?
                    schema_state = "PUBLIC"
                    schema = schema_type + "_" + schema_version + "_" + schema_state
                elif schema_version == "5.0":
                    schema = schema_type + "_" + schema_version
                local_results["schema"] = schema
                local_results["process_data"] = process_data
                # IGNORE THE NVD DATA FOR NOW SINCE WE NEED MULTIPLE PARSERS
                # results.append(local_results)
                process_data = data["namespaces"]["cve.org"]

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
        schema_file_name = "schema-" + item["schema"] + ".json"
        try:
            with open(schema_file_name) as schema_file:
                schema_data = json.load(schema_file)
        except IOError:
            print("ERROR: Schema file not found: " + schema_file_name)
            quit()

        instance_data = item["process_data"]

        v = Draft202012Validator(schema_data)
        errors = sorted(v.iter_errors(instance_data), key=lambda e: e.path)
        if errors == []:
            print("DATA PARSED CLEAN")
        else:
            for error in errors:
                print("####################")
                print(error.message)
                print("#####")
                print(error.context)
                print("#####")
                print(error.cause)
                print("#####")
                print(error.instance)
                print("#####")
                print(error.json_path)
                print("#####")
                print(error.path)
                print("#####")
                print(error.schema)
                print("#####")
                print(error.schema_path)
                print("#####")
                print(error.validator)
                print("#####")
                print(error.validator_value)




if __name__ == "__main__":
    file_namepath = sys.argv[1]
    file_name = os.path.basename(file_namepath)

    # GSD or CVE
    file_type = detectFileTypeByName(file_name)

    with open(file_namepath, "r") as f:
        file_data = json.load(f)
        f.close()

    # Get an array of schema and data, 0 or more entries
    extracted_data = extractDataAndSchema(file_type, file_data)

    # Validate the JSON data items
    validateJsonSchema(extracted_data)

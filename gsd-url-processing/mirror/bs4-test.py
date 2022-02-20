#!/usr/bin/env python3


from bs4 import BeautifulSoup
import re

import requests
url = "https://www.debian.org/security/2009/dsa-1907"
req = requests.get(url)
soup = BeautifulSoup(req.text, "html.parser")
#print(soup.title)
paragraphs = soup.findAll('p')

for entry in paragraphs:
    string_data = str(entry)
    string_data = string_data.replace('\n', ' ')
    if re.match("^<p>For the .+ (.+)", string_data):
        string_data = re.sub("^<p>", "", string_data)
        string_data = re.sub("</p>$", "", string_data)

        distro = re.findall("\(.*\)", string_data)
        distro_name = re.sub("^\(", "", distro[0])
        distro_name = re.sub("\)$", "", distro_name)
        print(distro_name)

        fixed_version = re.sub(".* these problems have been fixed in version ", "", string_data)

        print(fixed_version)

        print(string_data)
        # 	😃	

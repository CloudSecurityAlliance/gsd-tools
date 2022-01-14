# Module for querying the NVD CVE API
#

import requests
import datetime
import time

class UnexpectedResults(Exception):
    pass

class NVD:

    def __init__(self):
        self.now = datetime.datetime.utcnow()
        self.total = 0
        self.index = 0
        self.nvd_url = "https://services.nvd.nist.gov/rest/json/cves/1.0"
        self.payload = {}
        self.last_update = self.now

    def __get_time__(self, ts):
        # Return the time format the API wants

        y = ts.year
        m = ts.month
        d = ts.day
        h = ts.hour
        mi = ts.minute
        s = ts.second

        return f"{y}-{m:02}-{d:02}T{h:02}:{mi:02}:{s:02}:000 UTC-00:00"
        #return f"{y}-{m:02}-{d:02}T{h:02}:{mi:02}:{s:02}:000+00:00"

    def get_end_time_str(self):

        ts = self.end_time

        y = ts.year
        m = ts.month
        d = ts.day
        h = ts.hour
        mi = ts.minute
        s = ts.second

        return f"{y}-{m:02}-{d:02}T{h:02}:{mi:02}:{s:02}:000"

    def get_range(self, start, end):

        if start is None:
            self.start_time = datetime.datetime.fromisoformat("1990-01-01T00:00:00:000")
        else:
            self.start_time = datetime.datetime.fromisoformat(start)

        if end is None:
            self.end_time = self.now
        else:
            self.end_time = datetime.datetime.fromisoformat(end)


        # We can only query at most 120 days at a time, 110 keeps us safe
        time_diff = self.end_time - self.start_time
        if time_diff.days > 110:
            self.end_time = self.start_time + datetime.timedelta(days=110)

        self.get_page(0)

        self.total = self.data["totalResults"]
        self.page_size = self.data["resultsPerPage"]
        self.page = 0

    def get_page(self, page):

        # We don't want to hit this API too fast
        if (datetime.datetime.utcnow() - self.last_update).seconds < 5:
            time.sleep(4)

        if page > 0:
            self.index = self.page_size * page
        else:
            self.index = 0

        self.payload = {
            "startIndex": self.index,
            "resultsPerPage": 500,
            "modStartDate": self.__get_time__(self.start_time),
            "modEndDate": self.__get_time__(self.end_time)
        }

        response = requests.get(self.nvd_url, params=self.payload)
        response.raise_for_status()
        self.data = response.json()

    def __iter__(self):
        self.iter_n = 0
        self.iter_current = 0
        return self

    def __next__(self):

        if self.iter_n == self.total:
                raise StopIteration

        if self.iter_current == len(self.data["result"]["CVE_Items"]):
            # Time to paginate
            self.iter_current = 0
            self.page = self.page + 1
            self.get_page(self.page)

        to_return = self.data["result"]["CVE_Items"][self.iter_current]
        self.iter_n = self.iter_n + 1
        self.iter_current = self.iter_current + 1
        return to_return

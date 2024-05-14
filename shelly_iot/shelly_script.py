#! /usr/bin/env python3

from datetime import datetime, timedelta
from math import ceil
import sys
import time

import requests

shelly_url = "http://192.168.1.101/status"

def sleep_to_10s(r):
    if r.ok:
        status_timestamp = r.json()["unixtime"]
        now = datetime.fromtimestamp(status_timestamp)
        wait_seconds = ceil((now.second+1)/10)*10 - now.second # +1 ensures wait at least a second
        time.sleep(wait_seconds)

def main_loop():
    outfile = None
    try:
        r = requests.get(shelly_url, timeout=0.1)
    except requests.exceptions.Timeout:
        time.sleep(10)
        return

    if r.ok:
        now = datetime.fromtimestamp(r.json()["unixtime"])
        print(now)
        filename = "shelly3em_" + now.strftime("%Y%m%d_%H") + ".jsonl"
        if outfile is None or outfile.name != filename:
            if outfile is not None:
                outfile.close()
            outfile = open(filename, "a")
        outfile.write(r.text)
        outfile.write("\n")
        sleep_to_10s(r)
    else:
        time.sleep(10)
# align with 10s increments to start
if __name__ == "__main__":
    r = requests.get(shelly_url, timeout=0.1)
    if not r.ok:
        print("Couldn't get result from shelly3em", file=sys.stderr)
        sys.exit(-1)
    sleep_to_10s(r)
    while(True):
        main_loop()


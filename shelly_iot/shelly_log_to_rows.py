#!/usr/bin/env python3
"""
cat *.jsonl | python3 ../shelly_log_to_rows.py | sqlite-utils insert --nl shelly3em.db logpoints -     
"""

import json
import sys

def extract_rows(infile, outfile):
    for line in infile:
        try:
            data = json.loads(line)
            timestamp = data["unixtime"]
            localtime = data["time"]
            for i, emeter in enumerate(data["emeters"]):
                out = dict(timestamp=timestamp, meter=i+1)
                out.update(**emeter)
                out.update(localtime=localtime)
                json.dump(out, outfile)
                print("", file=outfile)
        except json.JSONDecodeError:
            print("Error", line)

if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == "--rows":
        extract_rows(sys.stdin, sys.stdout)
    elif cmd == "--aggregate":
        #aggregate


#!/usr/bin/env python3
import re
import sys
import json
from datetime import datetime

LOG_RE = re.compile(
    r'^(?P<ip>\d{1,3}(?:\.\d{1,3}){3}) - - '
    r'\[(?P<time>[^\]]+)\] '
    r'"(?P<method>\S+)\s+(?P<path>\S+)\s+(?P<proto>[^"]+)" '
    r'200 (?P<size>\d+|-) '
    r'"(?P<referer>[^"]*)" "(?P<ua>[^"]*)"$'
)

TIME_FMT = "%d/%b/%Y:%H:%M:%S %z"  # example: 04/Oct/2025:20:01:23 +0000

def parse_line(line: str):
    m = LOG_RE.match(line.strip())
    if not m:
        return None
    d = m.groupdict()

    d['size'] = int(d['size']) if d['size'] != '-' else None

    # try to parse time
    try:
        d['time'] = datetime.strptime(d['time'], TIME_FMT)
    except Exception:
        # leave raw string if parsing fails
        pass

    return d

def parse_stream(f):
    for lineno, line in enumerate(f, 1):
        parsed = parse_line(line)
        if parsed:
            yield parsed

if __name__ == "__main__":
    src = sys.stdin

    for rec in parse_stream(src):
        print(json.dumps(rec, default=str, ensure_ascii=False))

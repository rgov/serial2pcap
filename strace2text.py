#!/usr/bin/env python3
import argparse
import datetime
import re
import sys


pattern = re.compile(r'''
    ^(?:([\d:.]+)\s+)?     # timestamp
    (read|write)\(         # system call
    (\d+)(?:<[^>]+>)?,\s+  # file descriptor (optionally with path, -y)
    "([^"]+)"              # data
''', re.VERBOSE)


parser = argparse.ArgumentParser()
parser.add_argument('--fd', type=int, default=3)
args = parser.parse_args()


for line in sys.stdin:
    match = pattern.match(line)
    if not match:
        continue
    ts, op, fd, data = match.groups()
    fd = int(fd)
    data = bytes.fromhex(data.replace('\\x', ''))

    if op not in ('read', 'write'):
        continue
    if fd != args.fd:
        continue

    print('I' if op == 'read' else 'O', end='')
    if ts is not None:
        ts = datetime.datetime.strptime(ts, '%H:%M:%S.%f' if '.' in ts else
                                            '%H:%M:%S')
        print(f' {ts.time().isoformat()}', end='')
    print()

    for i in range(0, len(data), 16):
        print(f'{i:06x} {data[i:i+16].hex(sep=" ", bytes_per_sep=1)}')
    print(f'{len(data):06x}')
    print()

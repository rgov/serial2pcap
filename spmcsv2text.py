#!/usr/bin/env python3
import csv
import datetime
import sys


# Because the 'Data (chars)' column contains binary data, we may hit decoding
# errors when reading.
sys.stdin.reconfigure(errors='replace')


reader = csv.DictReader(sys.stdin, delimiter=';')
for row in reader:
    if row['Direction'] != 'UP':
        continue

    ts = datetime.datetime.strptime(row['Time'], "%d/%m/%Y %H:%M:%S")
    data = bytes.fromhex(row.get('Data', ''))

    if row['Function'] == 'IRP_MJ_READ':
        direction = 'I'
    elif row['Function'] == 'IRP_MJ_WRITE':
        direction = 'O'
    else:
        continue

    print(f'{direction} {ts.isoformat()}')
    for i in range(0, len(data), 16):
        print(f'{i:06x} {data[i:i+16].hex(sep=" ", bytes_per_sep=1)}')
    print(f'{len(data):06x}')
    print()

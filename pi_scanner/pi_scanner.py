#!/usr/bin/env python3

import asyncio
import json
from bleak import BleakScanner

# This is not SO functional BTW
last_read = dict()

def diference(a, b):
    map = {}
    for x in b:
        map[x] = True
    diff = []
    for x in a:
        if x not in map:
            diff.append(x)
    return diff

async def run():
    devices = await BleakScanner.discover()
    addresess = []
    for d in devices:
        address = d.address
        rssi = d.rssi
        uuid = ''
        if (rssi >= -70):
            addresess.append(address)
            if (address in last_read):
                last_read[address] = rssi
            else:
                last_read.update({address: rssi})
    records = diference(addresess, last_read.keys())
    for record in records:
        del last_read[record]
    return records


#!/usr/bin/env python3

import asyncio
import json
from bleak import BleakScanner

async def run():
    devices = await BleakScanner.discover()
    records = []
    for d in devices:
        address = d.address
        rssi = d.rssi
        uuid = d.uuid
        records.append((address, rssi, uuid))
    return records

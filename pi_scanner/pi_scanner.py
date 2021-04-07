#!/usr/bin/env python3

import asyncio
from bleak import BleakScanner
import pi_sender

address_list = [
    "FF:FF:44:46:5F:47",
    "FF:FF:C0:16:47:9A",
    "FF:FF:FF:F0:D8:C4"
]

async def run():
    devices = await BleakScanner.discover()
    for d in devices:
        address = d.address
        rssi = d.rssi
        for idx, value in enumerate(address_list):
            if value == address:
                print(address, rssi)
                pi_sender.send_to(idx + 1, int(rssi))

loop = asyncio.get_event_loop()
while True: 
    loop.run_until_complete(run())
    pass
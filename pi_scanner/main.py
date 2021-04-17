#!/usr/bin/env python3

import config
import json
from mqtt_client import MQTTClient
import pi_scanner

async def run(client):
    records = await pi_scanner.run(client)
    for record in records:
        message = {
            'mac_address': record[0],
            'rssi': record[1],
            'uuid': record[2]
        }
        client.publish("/devices/{}/events".format(config.device_id), json.dumps(message), qos=0)

def main():
    client = MQTTClient(
        project_id=config.project_id,
        cloud_region=config.cloud_region,
        registry_id=config.registry_id,
        device_id=config.device_id,
        private_key_file=config.private_key_file,
        algorithm=config.jwt_algorithm,
        ca_certs=config.ssl_ca_certs,
        mqtt_bridge_hostname=config.mqtt_bridge_hostname,
        mqtt_bridge_port=config.mqtt_bridge_port
    )
    client.loop()
    loop = asyncio.get_event_loop()
    while True: 
        loop.run_until_complete(run(client))

if __name__ == '__main__':
    main()

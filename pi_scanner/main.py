#!/usr/bin/env python3

import config
import json
from mqtt_client import MQTTClient

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
    message = {
        'mac_address': 'FF:FF:44:46:5F:47',
        'uuid': '123456789',
        'rssi': -10
    }
    client.loop()
    client.publish("/devices/{}/events".format(config.device_id), json.dumps(message), qos=0)
    while True:
        pass

if __name__ == '__main__':
    main()
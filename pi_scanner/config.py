#!/usr/bin/env python3

import os

PROJECT_ID_ENV = 'PROJECT_ID'
CLOUD_REGION_ENV = 'CLOUD_REGION'
REGISTRY_ID_ENV = 'REGISTRY_ID'
DEVICE_ID_ENV = 'DEVICE_ID'
PRIVATE_KEY_PATH_ENV = 'PRIVATE_KEY_PATH'
JWT_ALGORITHM_ENV = 'JWT_ALGORITHM'
SSL_CA_CERTS_ENV = 'SSL_CA_CERTS'
MQTT_BRIDGE_HOSTNAME_ENV = 'MQTT_BRIDGE_HOSTNAME'
MQTT_BRIDGE_PORT_ENV = 'MQTT_BRIDGE_PORT'

project_id = os.getenv(PROJECT_ID_ENV)
cloud_region = os.getenv(CLOUD_REGION_ENV)
registry_id = os.getenv(REGISTRY_ID_ENV)
device_id = os.getenv(DEVICE_ID_ENV)
private_key_file = os.getenv(PRIVATE_KEY_PATH_ENV)
jwt_algorithm = os.getenv(JWT_ALGORITHM_ENV)
ssl_ca_certs = os.getenv(SSL_CA_CERTS_ENV)
mqtt_bridge_hostname = os.getenv(MQTT_BRIDGE_HOSTNAME_ENV)
mqtt_bridge_port = os.getenv(MQTT_BRIDGE_PORT_ENV)

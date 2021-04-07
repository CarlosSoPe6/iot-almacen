#!/usr/bin/env python3
import datetime
import logging
import ssl
import jwt
import paho.mqtt.client as mqtt

logging.getLogger("googleapiclient.discovery_cache").setLevel(logging.CRITICAL)
MAXIMUM_BACKOFF_TIME = 32

def error_str(rc):
    return "{}: {}".format(rc, mqtt.error_string(rc))

class MQTTClient:

    def build_client_id(project_id, cloud_region, registry_id, device_id):
        return "projects/{}/locations/{}/registries/{}/devices/{}".format(
            project_id, cloud_region, registry_id, device_id
        )

    def __init__(
        self,
        project_id,
        cloud_region,
        registry_id,
        device_id,
        private_key_file,
        algorithm,
        ca_certs,
        mqtt_bridge_hostname,
        mqtt_bridge_port,
    ):
        self.__should_backoff = False
        self.__minimum_backoff_time = 1
        self.__iat = datetime.datetime.utcnow
        client_id = MQTTClient.build_client_id(project_id, cloud_region, registry_id, device_id)
        password_token = self.__autenticate(project_id, private_key_file, algorithm)
        print("Device client_id is '{}'".format(client_id))
        self.__client = mqtt.Client(client_id=client_id)
        # With Google Cloud IoT Core, the username field is ignored, and the
        # password field is used to transmit a JWT to authorize the device.
        self.__client.username_pw_set(
            username="unused", password=password_token
        )
        self.__client.tls_set(ca_certs=ca_certs, tls_version=ssl.PROTOCOL_TLSv1_2)
        self.__client.on_connect = self.__on_connect
        self.__client.on_publish = self.__on_publish
        self.__client.on_disconnect = self.__on_disconnect
        self.__client.on_message = self.__on_message
        self.__client.connect(mqtt_bridge_hostname, int(mqtt_bridge_port))  
        pass

    def __autenticate(self, project_id, private_key_file, algorithm):
        token = {
            'iat': datetime.datetime.utcnow(),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'aud': project_id
        }
        with open(private_key_file) as f:
            private_key = f.read()
        return jwt.encode(token, private_key, algorithm=algorithm)
    
    def __on_connect(self, unused_client, unused_userdata, unused_flags, rc):
        print("on_connect", mqtt.connack_string(rc))
        self.__should_backoff = False
        self.__minimum_backoff_time = 1

    def __on_disconnect(self, unused_client, unused_userdata, rc):
        print("on_disconnect", error_str(rc))
        self.__should_backoff = True

    def __on_publish(self, unused_client, unused_userdata, unused_mid):
        pass

    def __on_message(self, unused_client, unused_userdata, message):
        payload = str(message.payload.decode("utf-8"))
        print(
            "Received message '{}' on topic '{}' with Qos {}".format(
                payload, message.topic, str(message.qos)
            )
        )
        pass

    def subscribe(self, topic, callback):
        pass

    def publish(self, topic, payload, qos=0):
        print(topic, payload)
        self.__client.publish(topic, payload, qos=qos)
        pass

    def loop(self):
        self.__client.loop()

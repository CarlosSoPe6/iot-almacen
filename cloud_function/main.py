import base64
import json

def hello_pubsub(event, context):
    deviceId = event['attributes']['deviceId']
    deviceRegistryId = event['attributes']['deviceRegistryId']
    message = json.loads(base64.b64decode(event['data']).decode('utf-8'))
    print("--------- TEST ---------")
    print(deviceId)
    print(deviceRegistryId)
    print(message)

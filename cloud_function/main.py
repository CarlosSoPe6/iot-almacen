import base64
import datetime
import firebase_admin
import json
import os
from firebase_admin import credentials, firestore

firestore_credentials_path = os.getenv('FIREBASE_CREDENTIALS_FILE_PATH')

if firestore_credentials_path != None:
    cred = credentials.Certificate(firestore_credentials_path)
    default_app = firebase_admin.initialize_app(cred)
    pass
db = firestore.client()

def event_beacons(event, context):
    device_id = event['attributes']['deviceId']
    registry_id = event['attributes']['deviceRegistryId']
    messages = json.loads(base64.b64decode(event['data']).decode('utf-8'))
    now = datetime.datetime.utcnow()
    update_devicce(device_id, registry_id, now)
    for msg in messages:
        update_becon(device_id, msg, now)

def update_becon(device_id, message, now):
    collection = db.collection('beacons')
    document = collection.document(message['macAddress'])
    document.update({
        'lastRead': now,
        'rssi': message['rssi']
    })

def update_devicce(device_id, registry, now):
    collection = db.collection('dispositivos')
    document = collection.document('rpi-00')
    document.update({
        'lastRead': now
    })


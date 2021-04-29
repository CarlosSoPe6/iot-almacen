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
        

def insert_log(beacon, snap_id, now):
    collection = db.collection('registros')
    log_id = f"{now}_{snap_id}"
    collection.document(log_id).set({
        'beacon': beacon,
        'timestamp': now
    })

def update_becon(device_id, message, now):
    collection = db.collection('beacons')
    snap = collection.where('macAddress', '==', message['macAddress']).get()[0]
    snap_id = snap.id
    snap_dict = snap.to_dict()
    document = collection.document(snap_id)
    document.update({
        'isActive': not snap_dict['isActive'],
        'lastRead': now,
        'rssi': message['rssi']
    })
    insert_log(f"/beacons/{snap_id}", snap_id, now)

def update_devicce(device_id, registry, now):
    collection = db.collection('dispositivos')
    document = collection.document(device_id)
    document.update({
        'lastRead': now
    })

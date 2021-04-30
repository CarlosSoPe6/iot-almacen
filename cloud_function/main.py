import base64
import datetime
import json
import os
from firebase_admin import initialize_app, credentials, firestore

firestore_credentials_path = os.getenv('FIREBASE_CREDENTIALS_FILE_PATH')

if firestore_credentials_path != None:
    cred = credentials.Certificate(firestore_credentials_path)
    default_app = initialize_app(cred)
    pass
else:
    initialize_app()

db = firestore.client()

def hello_pubsub(event, context):
    device_id = event['attributes']['deviceId']
    registry_id = event['attributes']['deviceRegistryId']
    msg = json.loads(base64.b64decode(event['data']).decode('utf-8'))
    now = datetime.datetime.utcnow()
    print(msg)
    update_devicce(device_id, registry_id, now)
    update_becon(device_id, msg, now)
        

def insert_log(beacon, producto, snap_id, now):
    registros = db.collection('registros')
    log_id = f"{now}_{snap_id}"
    registros.document(log_id).set({
        'beacon': beacon,
        'producto': producto,
        'timestamp': now
    })

def update_becon(device_id, message, now):
    collection = db.collection('beacons')
    beacon_snap = collection.where('macAddress', '==', message['mac_address']).get()
    if len(beacon_snap) == 0:
        return
    producto_snap = db.collection('productos').where('BeaconID', '==', message['mac_address']).get()
    if len(producto_snap) == 0:
        return
    beacon_snap = beacon_snap[0]
    beacon_snap_id = beacon_snap.id
    beacon_snap_dict = beacon_snap.to_dict()
    producto_snap = producto_snap[0]
    producto_snap_id = producto_snap.id
    beacon = collection.document(beacon_snap_id)
    producto = db.collection('productos').document(producto_snap_id)
    beacon.update({
        'isActive': not beacon_snap_dict['isActive'],
        'lastRead': now,
        'rssi': message['rssi']
    })
    insert_log(beacon, producto, beacon_snap_id, now)

def update_devicce(device_id, registry, now):
    collection = db.collection('dispositivos')
    document = collection.document(device_id)
    document.update({
        'lastRead': now
    })

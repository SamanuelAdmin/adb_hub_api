import os.path
import random

import uvicorn
import sys
from fastapi import FastAPI

from addons.connector import AdbConnector
from addons.schemes import *
from routers import *

app = FastAPI()

print("Connecting to Adb...")
adbConnector = AdbConnector()
print("Connected. Loading devices...")
adbConnector.loadAllDevices()
print(f"Loaded {adbConnector.loadDevicesCount} devices.")
print("Init done.")

# uuid generator
UUID_PATH = os.path.join(os.path.dirname(__file__), 'uuid.txt')
currentUUID = ''

if not os.path.exists(UUID_PATH):
    with open(UUID_PATH, 'w') as f:
        # generate UUID (8 bytes)
        currentUUID = ''.join( str(random.choice('1234567890abcdef')) for _ in range(8) )
        f.write( currentUUID )
        print('UUID generated.')
else:
    with open(UUID_PATH) as f:
        currentUUID = f.readline().strip()

print(f'Loaded UUID: {currentUUID}')


'''
ROADMAP

/all -> all serials
/all/count -> count of devices
/all/load -> ??? load/reload all devices
/all/id -> Get hub id (uuid, 8 bytes)
/device/{serial} -> use this device
/device/{serial}/connect -> connect/load device
/device/{serial}/disconnect -> disconnect device
'''

allRouter.HUB_UUID = currentUUID

app.include_router(allRouter)
app.include_router(deviceRouter)
app.include_router(fileRouter)


if __name__ == '__main__':
    if len(sys.argv) == 3:
        uvicorn.run(app, host=sys.argv[1], port=int(sys.argv[2]))
    else: uvicorn.run(app, host='0.0.0.0', port=8000)
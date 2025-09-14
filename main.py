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

'''
/all -> all serials
/all/count -> count of devices
/all/load -> ??? load/reload all devices
/device/{serial} -> use this device
/device/{serial}/connect -> connect/load device
/device/{serial}/disconnect -> disconnect device
'''

app.include_router(allRouter)
app.include_router(deviceRouter)
app.include_router(fileRouter)


if __name__ == '__main__':
    if len(sys.argv) == 3:
        uvicorn.run(app, host=sys.argv[1], port=int(sys.argv[2]))
    else: uvicorn.run(app, host='0.0.0.0', port=8000)
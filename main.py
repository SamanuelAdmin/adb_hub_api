import uvicorn
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


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
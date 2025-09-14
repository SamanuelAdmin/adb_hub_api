import os
import adbutils
from adbutils import adb
from typing import Optional, ClassVar, Self
from uuid import UUID

if __name__ == "__main__": from exception import *
else: from .exception import *


class DeviceConnector:
    def __init__(self, device: adbutils.AdbDevice):
        self._device = device

    @property
    def device(self) -> adbutils.AdbDevice: return self._device

    def command(self, adbCommand: str) -> adbutils.ShellReturn:
        result = self._device.shell(adbCommand)
        return result

    def getFile(self, filePath: str) -> str:
        tempPathToFile = os.path.join(os.getcwd(), os.path.basename(filePath))
        self._device.sync.pull(filePath, os.path.join(os.getcwd(), tempPathToFile))
        return tempPathToFile


class AdbConnector:
    __instance: ClassVar[Optional[Self]] = None
    __connection: adbutils.AdbClient

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(AdbConnector, cls).__new__(cls)
        return cls.__instance


    def __init__(self, server=('127.0.0.1', 5037)):
        self.serverDetails = server
        self.__connection = adbutils.AdbClient(
            host=self.serverDetails[0], port=self.serverDetails[1],
        )

        self._devices: dict[str, adbutils.AdbDevice] = {}

    def __del__(self): pass

    @property
    def allSerials(self) -> list[str]:
        return list(self._devices.keys())

    @property
    def allDevices(self) -> list[adbutils.AdbDevice]:
        return list(self._devices.values())

    @property
    def loadDevicesCount(self): return len(list(self._devices.keys()))

    def loadDevice(self, serial: str) -> None:
        self._devices[serial] = adb.device(serial="33ff22xx")

    def loadAllDevices(self):
        for device in adb.device_list():
            self.loadDevice(device.serial)


    def device(self, serial: Optional[str]) -> DeviceConnector:
        currentDevice: adbutils.AdbDevice = self._devices.get(serial)
        if not currentDevice: raise DeviceNotFound(serial)

        return DeviceConnector( currentDevice )
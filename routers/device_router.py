from fastapi import APIRouter

from addons.connector import AdbConnector
from addons.connector.exception import DeviceNotFound
from addons.schemes import *

deviceRouter = APIRouter(prefix='/device')
adbConnector = AdbConnector()


@deviceRouter.post("/{serial}")
def adbCommand(serial: str, command: Command):
    try:
        device = adbConnector.device(serial)
    except DeviceNotFound:
        return StandardResponse(
            status=False, result=f'Device {serial} not found.'
        )

    result = device.command(command)
    return StandardResponse(
        status=True, result=result
    )
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

    splitedCommand = command.command.split(' ')

    if splitedCommand[0] == "adb_pull":
        pathToRemote = ' '.join(splitedCommand[1:])
        result = device.getFile(pathToRemote)
    else:
        result = device.command(command.command)

    return StandardResponse(
        status=True, result=result
    )
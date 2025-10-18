import threading
from fastapi import APIRouter
import os
import shlex

from addons.connector import AdbConnector, DeviceConnector
from addons.connector.exception import DeviceNotFound
from addons.schemes import *

deviceRouter = APIRouter(prefix='/device')
adbConnector = AdbConnector()


class Processor:
    def __init__(self, device: DeviceConnector):
        self._device = device

    def _pullProc(self, command: list[str]) -> tuple[bool, str]:
        return (
            True, self._device.getFile(
                ' '.join(command[1:])
            )
        )

    def _pushProc(self, command: str, splitCommand: list[str]) -> tuple[bool, str]:
        if '"' in command:
            _, localPath, remotePath = shlex.split(command)
        else:
            localPath = splitCommand[1]
            remotePath = ' '.join(splitCommand[2:])

        if not os.path.exists(localPath):
            return (False, f'File not found on local system.')

        return (True, f'File sent successfully.') \
            if self._device.sendFile(localPath, remotePath) \
            else (False, f'Sending file failed.')


    def process(self, command: Command) -> tuple[bool, str]:
        command: str = command.command
        splitCommand = command.split(' ')

        if splitCommand[0] in ("adb_pull", "pull"):
            return self._pullProc(splitCommand)
        elif splitCommand[0] in ("adb_push", "push"):
            return self._pushProc(command, splitCommand)

        return True, str(self._device.command(command))



@deviceRouter.post("/{serial}")
def adbCommand(serial: str, command: Command) -> StandardResponse:
    try: device = adbConnector.device(serial)
    except DeviceNotFound:
        return StandardResponse(
            status=False, result=f'Device {serial} not found.'
        )

    processor = Processor(device)
    if command.daemon:
        threading.Thread(target=processor.process, args=(command,)).start()
        result: tuple[bool, str] = (True, 'Processing...')
    else:
        result: tuple[bool, str] = processor.process(command)

    return StandardResponse(
        status=result[0], result=result[1]
    )
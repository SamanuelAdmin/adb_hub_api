from fastapi import APIRouter

from addons.connector import AdbConnector
from addons.schemes import *

allRouter = APIRouter(prefix='/all')
adbConnector = AdbConnector()


@allRouter.get("/all")
async def root() -> StandardResponse:
    return StandardResponse(
        status=True,
        result=adbConnector.allSerials,
    )

@allRouter.get("/count")
async def root() -> StandardResponse:
    return StandardResponse(
        status=True,
        result=adbConnector.loadDevicesCount,
    )
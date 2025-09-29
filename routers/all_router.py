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

@allRouter.get("/id")
async def root() -> StandardResponse:
    UUID = allRouter.HUB_UUID if hasattr(allRouter, 'HUB_UUID') else None

    return StandardResponse(
        status=True,
        result=UUID
    )
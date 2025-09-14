import os

from fastapi import APIRouter
from fastapi.responses import FileResponse

from addons.schemes import FilePath

fileRouter = APIRouter(prefix="/file")

TEMP_FILE_DIR_NAME = "temp"

@fileRouter.get("/get")
async def main(filePath: FilePath):
    realPath = os.path.basename(filePath.filename)
    fullFilePath = os.path.join(os.getcwd(), TEMP_FILE_DIR_NAME, realPath)
    if not os.path.exists(fullFilePath): return {'success': False, 'message': 'File not found'}

    return FileResponse(fullFilePath)
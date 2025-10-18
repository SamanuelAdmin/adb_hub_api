from pydantic import BaseModel
from typing import Any


class StandardResponse(BaseModel):
    status: bool
    result: Any

class Command(BaseModel):
    command: str
    daemon: bool=False

class FilePath(BaseModel):
    filename: str
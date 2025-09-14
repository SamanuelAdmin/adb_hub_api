from pydantic import BaseModel
from typing import Any


class StandardResponse(BaseModel):
    status: bool
    result: Any

class Command(BaseModel):
    command: str

class FilePath(BaseModel):
    filename: str
class DeviceNotFound(Exception):
    def __init__(self, serial: str) -> None:
        self.serial = serial

    def __str__(self) -> str:
        print(f'Device with serial {self.serial} not found.')
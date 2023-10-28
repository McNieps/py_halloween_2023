# App
class InvalidFileFormatError(Exception):
    def __init__(self,
                 message: str) -> None:

        self.message = message


# Environment
class InvalidLocationKwargsError(Exception):
    def __init__(self,
                 message: str) -> None:

        self.message = message


# Instance
class InvalidInstanceError(Exception):
    def __init__(self,
                 message: str) -> None:

        self.message = message

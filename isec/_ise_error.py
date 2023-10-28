# App
class InvalidFileFormatError(Exception):
    def __init__(self, message):
        self.message = message


# Environment
class InvalidLocationKwargsError(Exception):
    def __init__(self, message):
        self.message = message


# Instance
class InvalidInstanceError(Exception):
    def __init__(self, message):
        self.message = message

class CustomException(Exception):
    def __init__(self, message=""):
        self.message = message
        super().__init__(self.message)


class FileNotFound(CustomException):
    def __init__(self, file_name):
        self.message = f"File {file_name} is not found!"
        super().__init__(self.message)

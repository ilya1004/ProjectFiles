
class ExceptionUnauthorized(Exception):
    def __init__(self, message: str):
        self.message = message


class ExceptionNoUser(Exception):
    def __init__(self, message: str):
        self.message = message

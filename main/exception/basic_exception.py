class BasicException(Exception):
    def __init__(self, message: str = None):
        self.message = message if message else "An exception was raised"
        super().__init__(self.message)

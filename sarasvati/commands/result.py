class CommandLineResult:
    pass

class ErrorCommandLineResult(CommandLineResult):
    def __init__(self, message: str):
        super().__init__()
        self.message = message


class MessageCommandLineResult(CommandLineResult):
    def __init__(self, message: str):
        super().__init__()
        self.message = message

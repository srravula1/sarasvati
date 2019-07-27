class CommandException(Exception):
    def __init__(self, message):
        self.message = message


class CommandResult:
    def __init__(self, message: str=None, data=None):
        self.message = message
        self.data = data


class Command:
    def do(self) -> CommandResult:
        pass

    def undo(self) -> CommandResult:
        pass

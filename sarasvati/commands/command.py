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


class CommandArguments:
    def __init__(self, value):
        self.__value = value

    def get(self, name):
        return self.__value.get(name, None)

    def __getattr__(self, item):
        return self.__value.get(item, None)
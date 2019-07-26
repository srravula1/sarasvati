
from yapsy.IPlugin import IPlugin as YapsyPlugin


class Plugin(YapsyPlugin):
    def __init__(self):
        super().__init__()

    def activate(self):
        super().activate()

    def deactivate(self):
        super().deactivate()


class ApplicationPlugin(Plugin):
    def __init__(self):
        super().__init__()

    def activate(self):
        super().activate()

    def deactivate(self):
        super().deactivate()


class CommandLinePlugin(Plugin):
    def __init__(self):
        super().__init__()

    def execute(self, prompt: str):
        pass

    def register(self, command: str, handler):
        pass


class CommandsPlugin(Plugin):
    def __init__(self):
        super().__init__()

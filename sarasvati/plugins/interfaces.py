from typing import List

from yapsy.IPlugin import IPlugin as YapsyPlugin


class Plugin(YapsyPlugin):
    def __init__(self):
        super().__init__()
        self._api = None
        self._config = None

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


class CommandInfo:
    def __init__(self, command, description, handler):
        self.command = command
        self.description = description
        self.handler = handler


class CommandsPlugin(Plugin):
    def __init__(self):
        super().__init__()

    def get_commands(self):
        pass


class ComponentsPlugin(Plugin):
    def __init__(self):
        super().__init__()

    def get_components(self):
        pass


class StoragePlugin(Plugin):
    def __init__(self):
        super().__init__()

    def get_storages(self):
        pass


class ScreenPlugin(Plugin):
    pass


class CommandHookPlugin(Plugin):
    def get_hooks(self):
        pass

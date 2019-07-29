
from yapsy.IPlugin import IPlugin as YapsyPlugin


class Plugin(YapsyPlugin):
    def __init__(self):
        super().__init__()
        self._api = None

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

    def register(self, name: str, handler: callable):
        plugin = self._api.plugins.get(category="CommandLine")
        plugin.register(name, handler)

    def unregister(self, name: str):
        pass


class ComponentsPlugin(Plugin):
    def __init__(self):
        super().__init__()

    def register(self, name: str, component: type, serializer: "ComponentSerializer") -> None:
        self._api.components.register(name, component)
        self._api.serializers.register(name, serializer)

    def unregister(self, name: str) -> None:
        self._api.components.unregister(name)
        self._api.serializers.unregister(name)


class StoragePlugin(Plugin):
    def __init__(self):
        super().__init__()

    def open(self):
        pass

from sarasvati.brain.components import ComponentsManager
from sarasvati.config import ConfigManager
from sarasvati.packages import PackagesManager
from sarasvati.plugins import (ApplicationPlugin, CommandLinePlugin,
                               CommandsPlugin, ComponentsPlugin,
                               PluginsManager)


class Sarasvati:
    def __init__(self):
        # Config manager
        self.__config = ConfigManager("config.yml")
        self.__config.open()

        # Packages manager
        self.packages = PackagesManager(
            self.__config.packages.repositories,
            self.__config.packages.path)

        # Plugins manager
        self.plugins = PluginsManager(
            api=self,
            categories={
                "Application": ApplicationPlugin,
                "CommandLine": CommandLinePlugin,
                "Commands": CommandsPlugin,
                "Components": ComponentsPlugin
            })

        # Components
        self.components = ComponentsManager(
            api=self
        )

from sarasvati.packages import PackagesManager
from sarasvati.plugins import PluginsManager, ApplicationPlugin, CommandLinePlugin, CommandsPlugin


class Sarasvati:
    def __init__(self):
        self.plugins = PluginsManager(
            api=self,
            categories={
                "Application": ApplicationPlugin,
                "CommandLine": CommandLinePlugin,
                "Commands": CommandsPlugin
            })
    
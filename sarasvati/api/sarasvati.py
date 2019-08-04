import os
import platform
import subprocess

from sarasvati.brain.manager import BrainManager
from sarasvati.config import ConfigManager
from sarasvati.packages import PackagesManager
from sarasvati.plugins import (ApplicationPlugin, CommandLinePlugin,
                               CommandsPlugin, ComponentsPlugin,
                               PluginsManager, StoragePlugin)

class Sarasvati:
    def __init__(self):
        # Config manager
        self.config = ConfigManager("config.yml")
        self.config.open()

        # Packages manager
        self.packages = PackagesManager(
            self.config.packages.repositories,
            self.config.packages.path)

        # Plugins manager
        self.plugins = PluginsManager(
            api=self,
            categories={
                "Application": ApplicationPlugin,
                "CommandLine": CommandLinePlugin,
                "Commands": CommandsPlugin,
                "Components": ComponentsPlugin,
                "Storage": StoragePlugin
            })

        # Brain manager
        self.brains = BrainManager(api=self)

    def open_path(self, path):
        if platform.system() == "Windows":
            os.startfile(path)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])

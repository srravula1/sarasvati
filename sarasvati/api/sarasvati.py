import os
import platform
import subprocess

from sarasvati.brain.manager import BrainManager
from sarasvati.config import ConfigManager
from sarasvati.core.event import Event
from sarasvati.packages import PackagesManager
from sarasvati.plugins import (ApplicationPlugin, CommandHookPlugin,
                               CommandLinePlugin, CommandsPlugin,
                               ComponentsPlugin, PluginsManager, ScreenPlugin,
                               StoragePlugin)


class Sarasvati:
    def __init__(self):
        # events
        self.before_start = Event()

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
                "Storage": StoragePlugin,
                "Screen": ScreenPlugin,
                "CommandHook": CommandHookPlugin
            })
        
        # Load all the plugins
        self.plugins.update()

        # Brain manager
        self.brains = BrainManager(api=self)

    def open_path(self, path):
        if platform.system() == "Windows":
            os.startfile(path)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])

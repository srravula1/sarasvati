from yaml import safe_load as yaml_load

from sarasvati.packages import PackagesManager
from sarasvati.plugins import PluginsManager, ApplicationPlugin, CommandLinePlugin, CommandsPlugin


class Sarasvati:
    def __init__(self):
        # reading configuraion files
        with open("config.yml", "r") as ymlfile:
            cfg = yaml_load(ymlfile)

        # init packages repository
        packages_path = cfg["packages"]["path"]
        repositories_url = cfg["packages"]["repositories"]

        self.packages = PackagesManager(repositories_url, packages_path)
        self.plugins = PluginsManager(
            api=self,
            categories={
                "Application": ApplicationPlugin,
                "CommandLine": CommandLinePlugin,
                "Commands": CommandsPlugin
            })
    
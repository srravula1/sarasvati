from typing import List

from requests import get as requests_get
from yaml.scanner import ScannerError
from yaml import safe_load as yaml_load

from .fetcher import PluginFetcher
from .meta import PluginMeta
from .exception import PluginsException

PluginID = str

class PluginsRepository:
    def __init__(self, path, urls: List[str]):
        self.__urls = urls
        self.__cache = {}
        self.__fetcher = PluginFetcher(path)

    def update(self):
        for url in self.__urls:
            data = self.__fetch_repository(url)
            self.__cache.update(data)
        self.__cache = {k: PluginMeta(k, v["name"], v["url"]) for k, v in self.__cache.items()}
        print(self.__cache)
        
    def install(self, pid: PluginID):
        # get plugin info
        plugin_data = self.__cache.get(pid)
        if not plugin_data:
            raise Exception(f"Unable to install plugin {pid}")

        # download file
        self.__fetcher.fetch(plugin_data)

    def uninstall(self, pid: PluginID):
        pass

    @staticmethod
    def __fetch_repository(url: str) -> dict:
        response = requests_get(url)
        if not response.ok:
            raise Exception(f"Unable to fetch repository: {response.status_code} {response.reason}")
        try:
            return yaml_load(response.text)
        except ScannerError as ex:
            raise PluginsException("Repository file is broken. Not a valid YAML file.")

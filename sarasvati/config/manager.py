from munch import DefaultMunch
from yaml import safe_dump, safe_load


class ConfigManager:
    def __init__(self, path: str):
        self.__path = path
        self.__config = {}

    def open(self):
        with open(self.__path, "r") as ymlfile:
            self.__config = safe_load(ymlfile)
            self.__config = DefaultMunch.fromDict(self.__config)

    def save(self):
        with open(self.__path, "w") as ymlfile:
            safe_dump(self.__config, ymlfile)

    def __getattr__(self, name: str):
        return self.__config[name]

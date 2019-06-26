class PackageInfo:
    def __init__(self, key: str, name: str, url: str):
        self.__key = key
        self.__name = name
        self.__url = url

    @property
    def key(self):
        return self.__key

    @property
    def url(self):
        return self.__url
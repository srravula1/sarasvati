from sarasvati.brain.cache import BrainStorageCache
from sarasvati.storage.serialization import Serializer
from sarasvati.brain.brain import Brain


class BrainManager:
    def __init__(self, api):
        self.__api = api
        self.__active = None

    def open(self, path):
        storage = self.__api.plugins.get(category="Storage").open(path)
        serializer = Serializer(self.__api.components)
        cache = BrainStorageCache(storage, serializer)
        self.__active = Brain(cache, self.__api.components)

        return self.__active

    @property
    def active(self):
        return self.__active

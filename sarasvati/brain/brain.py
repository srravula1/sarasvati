from sarasvati.brain.cache import BrainStorageCache
from sarasvati.storage.serialization import Serializer


class Brain:
    def __init__(self, storage):
        self.__storage = storage

    def save_thought(self, thought):
        self.__storage.update(thought)

    def create_thought(self, title: str, description: str = None, key: str = None):
        thought = self.__storage.create()
        
        # set key if provided
        if key:
           thought.identity.key = key

        # set definition in provided
        if title or description:
            thought.definition.title = title
            thought.definition.description = description

        # save and return
        # thought.save()
        self.__storage.add(thought)
        return thought

    def delete_thought(self, thought):
        self.__storage.delete(thought)

    def find_thoughts(self, query):
        return self.__storage.find(query)

    def activate_thought(self):
        pass


class BrainManager:
    def __init__(self, api):
        self.__api = api
        self.__active = None

    def open(self, path):
        storage = self.__api.plugins.get(category="Storage").open(path)
        serializer = Serializer(self.__api.components)
        cache = BrainStorageCache(self.__api.components, storage, serializer)

        self.__active = Brain(cache)
        return self.__active

    @property
    def active(self):
        return self.__active

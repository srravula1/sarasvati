from abc import ABCMeta, abstractmethod

from sarasvati.brain.models import Thought
from sarasvati.brain.serialization import Serializer
from sarasvati.storage import Storage


class ThoughtCreator(metaclass=ABCMeta):
    """Create a Thought."""

    @abstractmethod
    def create(self) -> Thought:
        """Creates a new Thought."""
        pass


class ThoughtsStorage:
    """
    Caching storage of thoughts. Gets raw data from the database,
    deserializes and returns a Thought.
    """

    def __init__(self, storage: Storage, serializer: Serializer, creator: ThoughtCreator):
        """
        Initializes new instance of the ThoughtsStorage class.

        Arguments:
            storage {Storage} -- Raw storage to get data from.
            serializer {Serializer} -- Serializer to parse raw data into Thoughts.
            creator {ThoughtCreator} -- Create dummy thoughts which will be loaded later.
        """
        self.__storage = storage
        self.__serializer = serializer
        self.__creator = creator
        self.__cache = Cache()


    def get(self, key: str) -> Thought:
        """
        Returns Thought by specified key.
        
        Arguments:
            key {str} -- Key.
        
        Returns:
            Thought -- Thought.
        """
        is_cached = self.__cache.has(key)
        is_loaded = not self.__cache.is_lazy(key)
        
        # return thought from cache
        if is_cached and is_loaded:
            return self.__cache.get(key)

        # get lazy thought or create a new one
        thought = self.__cache.get(key) if is_cached else self.__creator.create()

        # deserialize thought
        data = self.__storage.get(key)
        self.__serializer.deserialize(thought, data)
        self.__cache.add(thought, lazy=False)

        return thought

    def add(self, thought):
        if not thought.identity.key:
            raise Exception("No idenity provided")
        data = self.__serializer.serialize(thought)
        self.__storage.add(data)
        self.__cache.add(thought)

    def find(self, query):
        result = []

        data = self.__storage.find(query)

        for record in data:
            key = record["identity"]["key"]
            thought = self.__cache.get(key)
            deser = thought is None or self.__cache.is_lazy(key)

            # todo remove any lazines
            if not thought:
                print("new: ", key)
                thought = self.__creator.create() # Thought(self.__brain)
                self.__cache.add_lazy(thought, key)

            if deser:
                print("deser: ", record)
                self.__serializer.deserialize(thought, record)
                self.__cache.add(thought, False)
            result.append(thought)

        print("find result", result)
        return result

    def update(self, thought):
        data = self.__serializer.serialize(thought)
        self.__storage.update(thought.identity.key, data)

    def remove(self, thought):
        return self.__storage.remove(thought)

    @property
    def cache(self):
        return self.__cache


class Cache:
    """
    Database cache.
    """

    def __init__(self):
        """
        Initializes new instance of the Cache class.
        """
        self.__cache = {}
        self.__lazy = []

    def add_lazy(self, thought, key):
        self.__cache[key] = thought
        if key not in self.__lazy:
            self.__lazy.append(key)

    def add(self, thought, lazy=False):
        self.__cache[thought.identity.key] = thought
        if lazy:
            self.__lazy.append(thought.identity.key)
        elif not lazy and thought.identity.key in self.__lazy:
            self.__lazy.remove(thought.identity.key)

    def get(self, key):
        return self.__cache.get(key, None)

    def has(self, key):
        return key in self.__cache

    def is_lazy(self, key):
        return key in self.__lazy

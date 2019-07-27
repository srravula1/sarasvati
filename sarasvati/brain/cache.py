from sarasvati.brain.models import Thought
from sarasvati.storage.storage import Storage


class BrainStorageCache:
    """
    Storage manager.
    """

    def __init__(self, components_manager, storage, serializer):
        self.__components_manager = components_manager
        self.__storage = storage
        self.__cache = Cache()
        self.__serializer = serializer

    def create(self):
        if not self.__components_manager.is_registered("identity"):
            raise Exception("Unable to create thought: 'identity' component is not registered.")

        # create thought, and add identity component to be sure key
        # is generated
        identity = self.__components_manager.create_component("identity")
        return Thought(self.__components_manager, components=[identity])

    def get(self, key, load_linked=True):
        # in cache and loaded
        if self.__cache.has(key) and not self.__cache.is_lazy(key):
            cached = self.__cache.get(key)
            if load_linked:
                for child in cached.links.all:
                    self.get(child.identity.key, load_linked=False)
            return cached

        # in cache but lazy
        if self.__cache.has(key):
            thought = self.__cache.get(key)
        else:
            thought = Thought(self.__components_manager)
            # self.__cache.add_lazy(thought, key)

        # thought = Thought() if not self.__cache.has(key) else self.__cache.get(key)
        data = self.__storage.get(key)
        self.__serializer.deserialize(thought, data)  # + options
        self.__cache.add(thought, lazy=False)

        if load_linked:
            for child in thought.links.all:
                self.get(child.identity.key, load_linked=False)

        return thought

    def add(self, thought):
        data = self.__serializer.serialize(thought)
        self.__storage.add(data)

    def find(self, query):
        result = []

        data = self.__storage.find(query)

        for record in data:
            key = record["identity"]["key"]
            thought = self.__cache.get(key)
            deser = thought is None or self.__cache.is_lazy(key)

            if not thought:
                print("new: ", key)
                thought = Thought(self.__components_manager)
                self.__cache.add_lazy(thought, key)

            if deser:
                print("deser: ", record)
                self.__serializer.deserialize(thought, record)
                self.__cache.add(thought, False)
            result.append(thought)

        # for r in result:
        #     for r2 in r.links.all_linked:
        #         self.get(r2.key, load_linked=False)
        #     # if self.__cache.has(key) and not self.__cache.is_lazy(key):
        #     #     result.append(self.__cache.get(key))
        #     # else:
        #     #     thought = Thought(self.__components_manager)
        #     #     thought = self.__serializer.deserialize(thought, record)
        #     #     result.append(thought)

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
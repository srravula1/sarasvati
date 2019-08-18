
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

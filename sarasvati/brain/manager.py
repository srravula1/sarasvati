from sarasvati.brain.brain import Brain


class BrainManager:
    def __init__(self, api):
        self.__api = api
        self.__active = None

    def open(self, path):
        storage = self.__api.plugins.get(category="Storage").open(path)
        self.__active = Brain(storage, self.__api.components)
        return self.__active

    @property
    def active(self):
        return self.__active

from sarasvati.brain.models import Thought

from sarasvati.brain.models import Component, Thought

class Brain:
    def __init__(self, storage, factory):
        self.__storage = storage
        self.__factory = factory

    @property
    def factory(self):
        return self.__factory

    def save_thought(self, thought: Thought):
        self.__storage.update(thought)

    def create_thought(self, title: str, description: str = None, key: str = None):        
        thought = Thought(self)

        # set key if provided
        if key:
           thought.identity.key = key

        # set definition in provided
        if title or description:
            thought.definition.title = title
            thought.definition.description = description

        # save and return
        self.__storage.add(thought)
        return thought

    def delete_thought(self, thought: Thought):
        self.__storage.remove(thought)

    def find_thoughts(self, query: dict):
        return self.__storage.find(query)

    def activate_thought(self):
        pass

from sarasvati.brain.brain import Brain
from sarasvati.brain.cache import BrainStorageCache
from sarasvati.brain.models import Component, Thought
from sarasvati.brain.serialization import SerializationManager, Serializer


class BrainManager:
    def __init__(self, api):
        self.__api = api
        self.__active = None

    def open(self, path):
        factory = ThoughtFactory()

        storage = self.__api.plugins.get(category="Storage").open(path)
        storage = BrainStorageCache(factory, storage, Serializer(self.__api.serializers, self.__api.components))
        brain = Brain(storage, factory)

        factory.brain = brain
        factory.components = self.__api.components

        self.__active = brain
        return self.__active

    @property
    def active(self):
        return self.__active


class ThoughtFactory:
    def __init__(self):
        self.brain = None
        self.components = None

    def create(self):
        return Thought(self.brain)

    def create_component(self, name: str) -> Component:
        return self.components.create_component(name)

    def attach_component(self, thought: Thought, component_name: str) -> Component:
        component_instance = self.components.create_component(component_name)
        thought.add_component(component_instance)
        return component_instance
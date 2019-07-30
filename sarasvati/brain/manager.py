from sarasvati.brain.brain import Brain
from sarasvati.brain.cache import ThoughtsStorage, ThoughtCreator
from sarasvati.brain.models import Component, Thought
from sarasvati.brain.serialization import SerializationManager, Serializer


class BrainManager:
    def __init__(self, api):
        self.__api = api
        self.__active = None

    def open(self, path):
        # factory = ThoughtsFactory()

        # open plain storage
        plugin = self.__api.plugins.get(category="Storage")
        storage = plugin.open(path)

        # serializer to convert raw data into obects
        serializer = Serializer(
            self.__api.serializers,
            self.__api.components)
        
        # cache to prevent loading and deserializing objects twice
        # lazy creator is used to create lazy linked thoughts which
        # will be loaded later
        creator = BrainThoughtCreator()
        storage = ThoughtsStorage(storage, serializer, creator)
        
        factory = ThoughtsFactory(components=self.__api.components)
        brain = Brain(storage, factory)
        
        factory.brain = brain
        creator.brain = brain

        # factory.brain = brain
        # factory.components = self.__api.components

        self.__active = brain
        return self.__active

    @property
    def active(self):
        return self.__active


class BrainThoughtCreator(ThoughtCreator):
    def __init__(self, brain=None):
        self.brain = brain
    def create(self):
        return Thought(self.brain)


class ThoughtsFactory:
    def __init__(self, brain=None, components=None):
        self.brain = brain
        self.components = components

    def create(self):
        if not self.brain:
            raise Exception("No brain is set to a factory")
        return Thought(self.brain)

    def create_component(self, name: str) -> Component:
        return self.components.create_component(name)

    def attach_component(self, thought: Thought, component_name: str) -> Component:
        component_instance = self.components.create_component(component_name)
        thought.add_component(component_instance)
        return component_instance
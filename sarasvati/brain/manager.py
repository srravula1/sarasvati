from inspect import signature

from sarasvati.brain.brain import Brain
from sarasvati.brain.models import Component, Thought
from sarasvati.brain.serialization import SerializationManager, Serializer
from sarasvati.brain.storage import ThoughtCreator, ThoughtsStorage

from sarasvati.brain.components import ComponentsManager
from sarasvati.brain.serialization import SerializationManager

class BrainManager:
    def __init__(self, api):
        self.__api = api
        self.__active = None

    def open(self, path):
        # factory = ThoughtsFactory()

        # open plain storage
        plugin = self.__api.plugins.get(category="Storage")
        storage = plugin.open(path)

        serialization_api = SerializerApi()
        components = ComponentsManager(api=serialization_api)
        serialization = SerializationManager()
        for components_plugin in self.__api.plugins.find(category="Components"):
            print(components_plugin)
            for component in components_plugin.get_components():
                components.register(component[0], component[1])
                if "api" in signature(component[2].__init__).parameters:
                    serialization.register(component[0], component[2](serialization_api))
                else:
                    serialization.register(component[0], component[2]())
    
        # serializer to convert raw data into obects
        serializer = Serializer(serialization, components)
        
        # cache to prevent loading and deserializing objects twice
        # lazy creator is used to create lazy linked thoughts which
        # will be loaded later
        creator = BrainThoughtCreator()
        storage = ThoughtsStorage(storage, serializer, creator)
        
        factory = ThoughtsFactory(components=components)
        brain = Brain(storage, factory)
        
        factory.brain = brain
        creator.brain = brain
        serialization_api.brain = brain
        serialization_api.storage = storage

        # factory.brain = brain
        # factory.components = self.__api.components

        self.__active = brain
        return self.__active

    @property
    def active(self):
        return self.__active


class SerializerApi:
    def __init__(self, brain=None):
        self.brain = brain
        self.storage = None

    def get_thought(self, key):
        return self.storage.get(key)

    def get_cached_thought(self, key):
        return self.storage.cache.get(key)

    def create_lazy_thought(self, key):
        thought = Thought(self.brain)
        thought.identity.key = key
        thought.title = "<Lazy>"
        self.storage.cache.add(thought, lazy=True)
        return thought


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

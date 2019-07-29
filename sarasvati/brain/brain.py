from sarasvati.brain import IBrain
from sarasvati.brain.cache import BrainStorageCache
from sarasvati.brain.components import ComponentsManager
from sarasvati.brain.models import Component, Thought
from sarasvati.brain.serialization import Serializer
from sarasvati.storage import Storage


class Brain(IBrain):
    def __init__(self, storage: Storage, components: ComponentsManager):
        self.__components = components
        self.__storage = BrainStorageCache(self, storage, Serializer(components))

    def create_component(self, name: str) -> Component:
        return self.__components.create_component(name)

    def attach_component(self, thought: Thought, component_name: str) -> Component:
        component_instance = self.__components.create_component(component_name)
        thought.add_component(component_instance)
        return component_instance

    def save_thought(self, thought: Thought):
        self.__storage.update(thought)

    def create_thought(self, title: str, description: str = None, key: str = None):
        if not self.__components.is_registered("identity"):
            raise Exception("Unable to create thought: 'identity' component is not registered.")
        identity = self.__components.create_component("identity")
        thought = Thought(self, components=[identity])

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

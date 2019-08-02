from inspect import signature
from itertools import chain
from urllib.parse import urlparse

from sarasvati.brain.components import ComponentsManager
from sarasvati.brain.models import Component, Thought
from sarasvati.brain.serialization import SerializationManager, Serializer
from sarasvati.brain.storage import ThoughtCreator, ThoughtsStorage


class Brain:
    def __init__(self, api, path: str):
        self.__active_thought = None

        self.__api = api
        self.__components = self.__open_components_manager()
        self.__serialization = self.__open_serialization_manager()
        self.__storage = ThoughtsStorage(
            self.__open_storage(path), 
            Serializer(self.__serialization, self.__components),
            BrainThoughtCreator(self))

    @property
    def active_thought(self):
        return self.__active_thought

    @property
    def storage(self):
        return self.__storage

    def create_component(self, name: str) -> Component:
        return self.__components.create_component(name)

    def attach_component(self, thought: Thought, component_name: str) -> Component:
        component_instance = self.__components.create_component(component_name)
        thought.add_component(component_instance)
        return component_instance

    def save_thought(self, thought: Thought):
        self.__storage.update(thought)

    def create_thought(self, title: str, description: str = None, key: str = None, link=None):
        thought = Thought(self)

        # set key if provided
        if key:
           thought.identity.key = key

        # set definition in provided
        if title or description:
            thought.definition.title = title
            thought.definition.description = description

        # set link if provided
        if link:
            __opposite = {"child": "parent", "parent": "child", "reference": "reference"}
            thought.links.add(link[0], __opposite[link[1]])
            link[0].links.add(thought, link[1])
            link[0].save()

        # save and return
        self.__storage.add(thought)
        return thought

    def delete_thought(self, thought: Thought):
        self.__storage.remove(thought)

    def find_thoughts(self, query: dict):
        return self.__storage.find(query)

    def activate_thought(self, value):
        self.__active_thought = value

    def __get_components(self):
        component_plugins = self.__api.plugins.find(category="Components")
        return list(chain.from_iterable(map(
            lambda x: x.get_components(), 
            component_plugins
        )))

    def __get_storages(self):
        storages_plugins = self.__api.plugins.find(category="Storage")
        return list(chain.from_iterable(map(
            lambda x: x.get_storages(), 
            storages_plugins
        )))

    def __open_storage(self, path: str):
        uri = urlparse(path)
        if not uri.netloc:
            raise ValueError("Protocol is not defined")

        for storage in self.__get_storages():
            if uri.scheme == storage[0]:
                return storage[1](uri.netloc + uri.path)
        raise Exception(f"Unable to finde storage for '{uri.scheme}' protocol")

    def __open_components_manager(self):
        components_manager = ComponentsManager(api=BrainApi(self))
        for component in self.__get_components():
            components_manager.register(component[0], component[1])
        return components_manager

    def __open_serialization_manager(self):
        serialization_manager = SerializationManager(api=BrainApi(self))
        for component in self.__get_components():
            serialization_manager.register(component[0], component[2])
        return serialization_manager


class BrainThoughtCreator(ThoughtCreator):
    def __init__(self, brain=None):
        self.brain = brain

    def create(self):
        return Thought(self.brain)


class BrainApi:
    def __init__(self, brain=None):
        self.brain = brain

    def get_thought(self, key):
        return self.brain.storage.get(key)

    def get_cached_thought(self, key):
        return self.brain.storage.cache.get(key)

    def create_lazy_thought(self, key):
        thought = Thought(self.brain)
        thought.identity.key = key
        thought.title = "<Lazy>"
        self.brain.storage.cache.add(thought, lazy=True)
        return thought

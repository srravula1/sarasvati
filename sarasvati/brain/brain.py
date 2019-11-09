from itertools import chain

from sarasvati.brain.components import (ComponentsInfoProvider,
                                        ComponentsManager)
from sarasvati.brain.models import Component, Thought
from sarasvati.brain.serialization import SerializationManager, Serializer
from sarasvati.brain.storage import ThoughtCreator, ThoughtsStorage
from sarasvati.storage import DataStorage, MediaStorage


class Brain:
    """Brain is a storage of thoughts.."""

    def __init__(self, name: str, cip: ComponentsInfoProvider,
                 data_storage: DataStorage, media_storage: MediaStorage):
        """
        Initializes a new instance of the Brain class.

        Atguments:
            name {str} -- Name of a brain.
            cip {ComponentsInfoProvider} -- ComponentInfo provider.
            data_storage {DataStorage} -- Data storage.
            media_storage {MediaStorage} -- Media storage.
        """
        brain_api = BrainApi(self)

        self.__name = name
        self.__active_thought = None
        self.__components = ComponentsManager(cip, api=brain_api)
        self.__serialization = SerializationManager(cip, api=brain_api)
        self.__data_storage = ThoughtsStorage(
            data_storage,
            Serializer(self.__serialization, self.__components),
            BrainThoughtCreator(self))
        self.__media_storage = media_storage

    @property
    def name(self):
        """Returns name of a brain."""
        return self.__name

    @property
    def components(self):
        return self.__components

    @property
    def active_thought(self):
        return self.__active_thought

    @property
    def storage(self):
        return self.__data_storage

    @property
    def media_storage(self):
        return self.__media_storage

    def create_component(self, name: str) -> Component:
        return self.__components.create_component(name)

    def attach_component(self, thought: Thought, component_name: str) -> Component:
        component_instance = self.__components.create_component(component_name)
        thought.add_component(component_instance)
        return component_instance

    def save_thought(self, thought: Thought):
        self.__data_storage.update(thought)

    def create_thought(self, title: str, description: str = None, key: str = None, link=None):
        thought = Thought(self)

        # set key if provided
        if key:
            thought.identity.key = key

        self.__data_storage.add(thought)

        # set definition in provided
        if title or description:
            thought.definition.title = title
            thought.definition.description = description

        # set link if provided
        if link:
            __opposite = {"child": "parent",
                          "parent": "child", "reference": "reference"}
            thought.links.add(link[0], __opposite[link[1]])
            link[0].links.add(thought, link[1])
            link[0].save()

        # save and return
        thought.save()
        return thought

    def delete_thought(self, thought: Thought):
        self.__data_storage.remove(thought)

    def find_thoughts(self, query: dict):
        return self.__data_storage.find(query)

    def activate_thought(self, value):
        self.__active_thought = value


class PluginsComponentsInfoProvider(ComponentsInfoProvider):
    def __init__(self, plugins_manager):
        self.__plugins_manager = plugins_manager

    def load_components(self):
        component_plugins = self.__plugins_manager.find(category="Components")
        all_components = list(chain.from_iterable(map(
            lambda x: x.get_components(),
            component_plugins
        )))
        return {ci.name: ci for ci in all_components}


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

    def is_component_registered(self, name):
        return self.brain.components.is_registered(name)

    @property
    def media(self):
        return self.brain.media_storage

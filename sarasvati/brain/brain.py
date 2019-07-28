from sarasvati.brain.cache import BrainStorageCache
from sarasvati.brain.components import ComponentsManager
from sarasvati.brain.models import Thought
from sarasvati.storage.serialization import Serializer
from sarasvati.storage.storage import Storage


class Brain:
    def __init__(self, storage: Storage, components: ComponentsManager):
        self.__components = components
        self.__storage = BrainStorageCache(self, storage, Serializer(components))

    def create_component(self, name):
        return self.__components.create_component(name)

    def attach_component(self, thought, component_name):
        if not thought.has_component(component_name):
            component_instance = self.__components.create_component(component_name)
            thought.add_component(component_instance)
            return component_instance

    def save_thought(self, thought):
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

    def delete_thought(self, thought):
        self.__storage.remove(thought)

    def find_thoughts(self, query):
        return self.__storage.find(query)

    def activate_thought(self):
        pass

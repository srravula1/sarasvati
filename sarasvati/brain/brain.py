from sarasvati.storage.serialization import Serializer
from sarasvati.brain.cache import BrainStorageCache
from sarasvati.brain.models import Thought


class Brain:
    def __init__(self, components, storage):
        self.__storage = storage
        self.__components = components
        self.__serializer = Serializer(self.__components)
        self.__cache = BrainStorageCache(self, self.__storage, self.__serializer)
    
    @property
    def components(self):
        return self.__components

    @property
    def storage(self):
        return self.__storage

    def create_thought(self, title: str, description: str = None, key: str = None):
        # identity component is required, check it's presence first
        if not self.__components.is_registered("identity"):
            raise Exception("Unable to create thought: 'identity' component is not registered.")

        # create thought, and add identity component to be sure key
        # is generated
        identity = self.__components.create_component("identity")
        thought = Thought(self, components=[identity])

        # set key if provided
        if key:
           thought.identity.key = key

        # set definition in provided
        if title or description:
           thought.definition.title = title
           thought.definition.description = description

        # link thought
        #if link:
        #    link_to = link[0]
        #    link_type = link[1]
        #    opposite = {"child": "parent", "parent": "child", "reference": "reference"}.get(link_type)
        #    thought.links.add(link_to, opposite)
        #    link_to.links.add(thought, link_type)

        # return result
        self.__storage.add(self.__serializer.serialize(thought))
        return thought

    def delete_thought(self):
        pass

    def find_thoughts(self, query):
        return self.__cache.find(query)

    def activate_thought(self):
        pass


class BrainManager:
    def __init__(self, api):
        self.__api = api
        self.__active = None

    def open(self, path):
        storage = self.__api.plugins.get(category="Storage").open(path)
        self.__active = Brain(self.__api.components, storage)
        return self.__active

    @property
    def active(self):
        return self.__active

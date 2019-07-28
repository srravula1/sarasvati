from sarasvati.brain.models import Thought



class Brain:
    def __init__(self, storage, components_manager):
        self.__components_manager = components_manager
        self.__storage = storage
        self.__storage.set_materializer(lambda: Thought(self))

    def create_component(self, name):
        return self.__components_manager.create_component(name)

    def attach_component(self, thought, component_name):
        if not thought.has_component(component_name):
            component_instance = self.__components_manager.create_component(component_name)
            thought.add_component(component_instance)
            return component_instance

    def save_thought(self, thought):
        self.__storage.update(thought)

    def create_thought(self, title: str, description: str = None, key: str = None):
        if not self.__components_manager.is_registered("identity"):
            raise Exception("Unable to create thought: 'identity' component is not registered.")
        identity = self.__components_manager.create_component("identity")
        thought = Thought(self, components=[identity])

        # set key if provided
        if key:
           thought.identity.key = key

        # set definition in provided
        if title or description:
            thought.definition.title = title
            thought.definition.description = description

        # save and return
        # thought.save()
        self.__storage.add(thought)
        return thought

    def delete_thought(self, thought):
        self.__storage.delete(thought)

    def find_thoughts(self, query):
        return self.__storage.find(query)

    def activate_thought(self):
        pass

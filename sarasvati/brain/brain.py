from abc import ABCMeta, abstractmethod


class Composite(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, components=None):
        """
        Initializes new instance of the Composite class.
        :type components: list
        :param components: Components to create composite from.
        """
        self.__components = {}

        if components is not None:
            self.add_components(components)

    def has_component(self, component_name):
        """
        Returns true if component already added, otherwise false
        :rtype: bool
        :type component_name: str
        :param component_name: Name of the component
        :return: True if component already added, otherwise false
        """
        return component_name in self.__components.keys()

    def add_component(self, component):
        """
        Adds specified component
        :type component: Component
        :param component: Component to add
        """
        if self.has_component(component.name):
            raise Exception("Component '" + component.name + "' already exist")
        self.__components[component.name] = component
        if hasattr(component, "on_added"):
            component.on_added(self)

    def add_components(self, components):
        """
        Adds specified list of components
        :type components: List[Component]
        :param components: Array of components
        """
        for component in components:
            self.add_component(component)

    def get_component(self, name):
        """
        Returns component using specified name. Raises exception if no component found.
        :type name: str
        :param name: Name of the component
        :return: Component
        """
        if name not in self.__components.keys():
            raise Exception("Component '{}' not found for '{}'"
                            .format(name, str(self.__class__.__name__)))

        return self.__components[name]

    @property
    def components(self):
        """
        Returns list of components
        :return: Components
        """
        return self.__components.values()

    def __getattr__(self, item):
        return self.get_component(item)


class Thought(Composite):
    def __init__(self, brain):
        super().__init__()
        self.__brain = brain

    @property
    def key(self):
        return self.identity.key

    @property
    def title(self):
        """Gets title of thought."""
        return self.definition.title

    @title.setter
    def title(self, value):
        """Sets title of thought."""
        self.definition.title = value

    @property
    def description(self):
        """Gets short description of thought."""
        return self.definition.description

    @description.setter
    def description(self, value):
        """Sets description of thought."""
        self.definition.description = value

    def save(self):
        self.__brain.storage.update(self)

    def delete(self):
        self.__brain.storage.delete(self)

    def __getattr__(self, component_name):
        if self.has_component(component_name):
            return self.get_component(component_name)
        else:
            component_instance = self.__brain.components.create_component(component_name)
            self.add_component(component_instance)
            return component_instance

    def __repr__(self):
        return "<{}>".format(self.definition.title)


class Brain:
    def __init__(self, components, storage):
        self.__storage = storage
        self.__components = components
    
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

        # create thought, and add identity component
        # identity = self.__components.create_component("identity")
        thought = Thought(self)

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
        # self.__storage.add()

        #print(thought, thought.key, thought.title)
        #thought.save()
        return thought

    def delete_thought(self):
        pass

    def find_thoughts(self):
        pass

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

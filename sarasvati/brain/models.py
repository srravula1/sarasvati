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
    def __init__(self, brain, components=[]):
        super().__init__(components=components)
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
        self.__brain.save_thought(self)

    def delete(self):
        self.__brain.delete_thought(self)

    def __getattr__(self, component_name):
        if self.has_component(component_name):
            return self.get_component(component_name)
        else:
            return self.__brain.attach_component(self, component_name)
            
    def __repr__(self):
        return "<{}>".format(self.definition.title)
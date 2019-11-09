from abc import ABCMeta, abstractmethod
from typing import List


class Component(metaclass=ABCMeta):
    """Provides interface for a custom component."""

    @abstractmethod
    def __init__(self, name: str):
        """
        Initializes new instance of the Component class.

        Arguments:
            name {str} -- Name of a component.
        """
        self.__component_name = name

    @property
    def name(self) -> str:
        """
        Returns name of a component.

        Returns:
            str -- Name of a component.
        """
        return self.__component_name


class Composite(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, components: List[Component] = None):
        """
        Initializes new instance of a Composite class.

        Keyword Arguments:
            components {List[Component]} -- List of a components to build composite with. (default: {None})
        """
        self.__components = {}
        if components is not None:
            self.add_components(components)

    def has_component(self, component_name: str) -> bool:
        """
        Checks if composite has a component.

        Arguments:
            component_name {str} -- Name of a component.

        Returns:
            bool -- True if composite has a component.
        """
        return component_name in self.__components.keys()

    def add_component(self, component: Component):
        """
        Add component to the composite.

        Arguments:
            component {Component} -- Component.

        Raises:
            TypeError: Raises if component not an instance of a Component class.
            Exception: Raises if component already exist.
        """
        if not isinstance(component, Component):
            class_name = type(component).__name__
            raise TypeError(
                f"Component '{class_name}' should be subclass of Component")
        if self.has_component(component.name):
            raise Exception(f"Component '{component.name}' already exist")
        self.__components[component.name] = component
        if hasattr(component, "on_added"):
            component.on_added(self)

    def add_components(self, components: List[Component]):
        """
        Adds list of components to the composite.

        Arguments:
            components {List[Component]} -- [description]
        """
        for component in components:
            self.add_component(component)

    def get_component(self, name: str) -> Component:
        """
        Returns component using specified name

        Arguments:
            name {str} -- Name of a component.

        Raises:
            Exception: If no component found.

        Returns:
            Component -- Component.
        """
        if name not in self.__components.keys():
            raise Exception("Component '{}' not found for '{}'"
                            .format(name, str(self.__class__.__name__)))

        return self.__components[name]

    def delete_component(self, name: str):
        # todo: check for presence
        del self.__components[name]

    @property
    def components(self) -> List[Component]:
        """
        Returns list of components.

        Returns:
            List[Component] -- List of components
        """
        return list(self.__components.values())

    def __getattr__(self, item: str) -> Component:
        return self.get_component(item)


class Thought(Composite):
    def __init__(self, brain, components=[]):
        super().__init__(components=components)
        self.__brain = brain

    @property
    def brain(self):
        return self.__brain

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

    def activate(self):
        self.__brain.activate_thought(self)

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

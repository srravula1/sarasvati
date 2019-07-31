from inspect import signature
from typing import List, Type

from sarasvati.brain.models import Component


class ComponentsManager:
    """
    Components manager.
    """

    def __init__(self, api=None):
        """
        Initialize new instance of the ComponentsManager class.
        """
        self.__components = {}
        self.__api = api

    @property
    def all(self) -> List[Component]:
        """
        Get list of all components registered.
        :return: List of registered components.
        """
        return list(map(lambda x: x.component, self.__components.values()))

    def get_component(self, name: str) -> Type[Component]:
        """
        Get component class.
        :param name: Name of a component.
        :return: Class of a component.
        """
        if name not in self.__components:
            raise Exception("The '{}' component is not registered.".format(name))
        return self.__components[name]

    def create_component(self, name: str) -> Component:
        """
        Create new instance of a component using specified name.
        :param name: Name of a component.
        :return: Instance of a component.
        """
        component_class = self.get_component(name)
        if "api" in signature(component_class.__init__).parameters:
            return component_class(api=self.__api)
        return component_class()

    def register(self, name: str, component: type) -> None:
        """
        Register new component.
        :param name: Name of a component.
        :param component: Class of a component.
        :param serializer: Serializer instance.
        """
        if not issubclass(component, Component):
            raise ValueError("The 'component' argument should be subclass of Component class.")
        if name in self.__components:
            raise Exception("Component '{}' already registered.".format(name))

        self.__components[name] = component

    def unregister(self, name: str) -> None:
        """
        Unregister component
        :param name: Name of a component to unregister.
        """
        if name not in self.__components:
            raise Exception("Component '{}' is not registered".format(name))

        del self.__components[name]

    def is_registered(self, name: str) -> bool:
        """
        Return true if component with specified name registered.
        :param name: Name of the component.
        :return: True if component registered, otherwise False.
        """
        return name in self.__components

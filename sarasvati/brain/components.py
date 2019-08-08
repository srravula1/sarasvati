from inspect import signature
from typing import List, Type

from sarasvati.brain.models import Component

class ComponentInfo:
    def __init__(self, name, component, serializer, data=None):
        self.name = name
        self.component = component
        self.serializer = serializer
        self.data = data


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

    def get_component_info(self, name: str) -> ComponentInfo:
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
        component_info = self.get_component_info(name)
        component_class = component_info.component
        
        handler_args = list(signature(component_class.__init__).parameters)
        handler_params = {
            "api": self.__api,
            **(component_info.data or {})
        }
        filtered_args = {k: v for k, v in handler_params.items() if k in handler_args}
        
        return component_class(**filtered_args)

    def register(self, component_info: ComponentInfo) -> None:
        """
        Register new component.
        :param name: Name of a component.
        :param component: Class of a component.
        :param serializer: Serializer instance.
        """
        if not isinstance(component_info, ComponentInfo):
            raise ValueError("The 'component_info' argument should be an instance of ComponentInfo class.")
        if not issubclass(component_info.component, Component):
            raise ValueError("The 'component_info.component' argument should be subclass of Component class.")
        if component_info.name in self.__components:
            raise Exception(f"Component '{component_info.name}' already registered.")

        self.__components[component_info.name] = component_info

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

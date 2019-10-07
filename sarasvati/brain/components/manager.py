from inspect import signature

from sarasvati.brain.models import Component
from sarasvati.brain.components.info import ComponentInfo
from sarasvati.brain.components.provider import ComponentsInfoProvider


class ComponentsManager:
    """
    Components manager.
    """

    def __init__(self, provider: ComponentsInfoProvider, api=None):
        """
        Initialize new instance of the ComponentsManager class.
        """
        self.__api = api
        self.__provider = provider

    def get_component_info(self, name: str) -> ComponentInfo:
        """
        Get component class.
        :param name: Name of a component.
        :return: Class of a component.
        """
        components = self.__provider.load_components()
        if name not in components:
            raise Exception(f"The '{name}' component is not registered.")
        return components[name]

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

    def is_registered(self, name: str) -> bool:
        """
        Return true if component with specified name registered.
        :param name: Name of the component.
        :return: True if component registered, otherwise False.
        """
        components = self.__provider.load_components()
        return name in components

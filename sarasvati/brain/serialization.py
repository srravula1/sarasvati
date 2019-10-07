from abc import ABCMeta, abstractmethod
from inspect import signature

from sarasvati.brain.components import ComponentsProvider


class ComponentSerializer(metaclass=ABCMeta):
    """
    Serializes and deserializes specified component into/from a dictionary.
    """

    @abstractmethod
    def serialize(self, component: "Component") -> dict:
        """
        Serializes component into dictionary.
        :param component: Component to serialize
        """

    @abstractmethod
    def deserialize(self, data: dict, component: "Component"):
        """
        Deserialize component from dictionary
        :param data: Data to deserialize from.
        :param component: Component to deserialize to.
        """


class SerializationManager:
    """Creates serializers on demand using specified provider."""

    def __init__(self, provider: ComponentsProvider, api=None):
        self.__provider = provider
        self.__api = api

    def get_serializer(self, name: str) -> ComponentSerializer:
        """
        Get serializer for specified component.
        :param name: Name of a component.
        :return: Serializer.
        """
        comopnents_info = self.__provider.load_components()
        if name not in comopnents_info:
            raise Exception(f"The '{name}' component is not registered.")

        serializer = comopnents_info[name].serializer
        if "api" in signature(serializer.__init__).parameters:
            return serializer(self.__api)
        else:
            return serializer()

    def is_registered(self, name: str) -> bool:
        """
        Return True if component with specified name registered.
        :param name: Name of the component.
        :return: True if component registered, otherwise False.
        """
        components_info = self.__provider.load_components()
        return name in components_info


class Serializer:
    def __init__(self, serializers, components):
        """Initializes new instance of the Serializer class."""
        self.__serializers = serializers
        self.__components = components

    def serialize(self, model):
        """
        Serializes object into dictionary
        :rtype: dict
        :type model: Type[Composite]
        :param model: Model to serialize
        :return: Dictionary
        """
        result = {}
        for component in model.components:
            serializer = self.__serializer(component.name)
            data = serializer.serialize(component)
            if data:
                result[component.name] = data
        return result

    def deserialize(self, model, data):
        """
        Deserialize dictionary into model
        :type model: Type[Composite]
        :type data: dict
        :param model: Model to deserialize to
        :param data: Data to deserialize from
        :return: Deserialized model
        """
        for key in data.keys():
            component_data = data[key]
            serializer = self.__serializer(key)

            if model.has_component(key):
                component = model.get_component(key)
            else:  # create new component if not exist
                component = self.__components.create_component(key)
                model.add_component(component)

            serializer.deserialize(component_data, component)

        return model

    def __serializer(self, name):
        """Returns serializer by specified name"""
        serializer = self.__serializers.get_serializer(name)
        if not serializer:
            raise Exception("No serializer found for '{}'".format(name))
        return serializer

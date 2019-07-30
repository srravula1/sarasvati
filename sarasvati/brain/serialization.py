from abc import ABCMeta, abstractmethod


class ComponentSerializer(metaclass=ABCMeta):
    @abstractmethod
    def serialize(self, component: "Component") -> dict:
        """
        Serializes component into dictionary.
        :param component: Component to serialize
        """
        pass

    @abstractmethod
    def deserialize(self, data: dict, component: "Component"):
        """
        Deserialize component from dictionary
        :param data: Data to deserialize from.
        :param component: Component to deserialize to.
        """
        pass


class SerializationManager:    
    def __init__(self):
        self.__serializers = {}

    def get_serializer(self, name: str) -> ComponentSerializer:
        """
        Get serializer for specified component.
        :param name: Name of a component.
        :return: Serializer.
        """
        if name not in self.__serializers:
            raise Exception("The '{}' component is not registered.".format(name))
        return self.__serializers[name]

    def register(self, name: str, serializer: ComponentSerializer) -> None:
        """
        Register new component.
        :param name: Name of a component.
        :param component: Class of a component.
        :param serializer: Serializer instance.
        """
        if not isinstance(serializer, ComponentSerializer):
            raise ValueError("The 'serializer' argument should be instance of ComponentSerializer class.")
        if name in self.__serializers:
            raise Exception("Serializer '{}' already registered.".format(name))

        self.__serializers[name] = serializer

    def unregister(self, name: str) -> None:
        """
        Unregister component
        :param name: Name of a component to unregister.
        """
        if name not in self.__serializers:
            raise Exception("Serializer '{}' is not registered".format(name))

        del self.__serializers[name]

    def is_registered(self, name: str) -> bool:
        """
        Return true if component with specified name registered.
        :param name: Name of the component.
        :return: True if component registered, otherwise False.
        """
        return name in self.__serializers


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
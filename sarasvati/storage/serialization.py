class Serializer:
    def __init__(self, components):
        """Initializes new instance of the Serializer class."""
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
        serializer = self.__components.get_serializer(name)
        if not serializer:
            raise Exception("No serializer found for '{}'".format(name))
        return serializer
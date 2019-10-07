from typing import Type

from sarasvati.brain.models import Component


class ComponentInfo:
    """
    Provides information about component of a Thought.
    """

    def __init__(self, name: str, component: Type[Component], serializer: "ComponentSerializer", data: dict = None):
        self.name = name
        self.component = component
        self.serializer = serializer
        self.data = data

from abc import ABCMeta, abstractmethod
from typing import Dict

from sarasvati.brain.components.info import ComponentInfo


class ComponentsInfoProvider(metaclass=ABCMeta):
    @abstractmethod
    def load_components(self) -> Dict[str, ComponentInfo]:
        pass

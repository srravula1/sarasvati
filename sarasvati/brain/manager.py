"""
Top level API to manage brains.
"""

from itertools import chain
from typing import Dict, Optional

from sarasvati.brain.brain import Brain
from sarasvati.brain.components import ComponentInfo, ComponentsInfoProvider
from sarasvati.storage import DataStorage, MediaStorage
from sarasvati.storage.helpers import open_storage


class BrainManager:
    """Manager of a brains."""

    def __init__(self, api):
        """
        Initializes new instance of the BrainManager class.

        Arguments:
            api {Sarasvati} -- Api
        """
        self.__api = api
        self.__active = None

    def open(self, path: str, create: bool = False) -> Brain:
        """
        Opens new brain at specified path.

        Arguments:
            path {str} -- Path to the brain.

        Returns:
            Brain -- Brain.
        """
        components_provider = PluginsComponentsInfoProvider(self.__api.plugins)
        data_storage = open_storage(self.__api, path, DataStorage, create)
        media_storage = open_storage(self.__api, path, MediaStorage, create)
        name = path.split("/")[-1]

        self.__active = Brain(name, components_provider,
                              data_storage, media_storage)
        return self.__active

    @property
    def active(self) -> Optional[Brain]:
        """
        Returns active brain.

        Returns:
            Brain -- Brain.
        """
        return self.__active


class PluginsComponentsInfoProvider(ComponentsInfoProvider):
    """Provides information about componets taken from plugins."""

    def __init__(self, plugins_manager):
        self.__plugins_manager = plugins_manager

    def load_components(self) -> Dict[str, ComponentInfo]:
        component_plugins = self.__plugins_manager.find(category="Components")
        all_components = list(chain.from_iterable(map(
            lambda x: x.get_components(),
            component_plugins
        )))
        return {ci.name: ci for ci in all_components}

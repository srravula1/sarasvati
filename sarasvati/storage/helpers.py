"""Provides helpers to find or open storages."""

from itertools import chain
from typing import List, Union

from sarasvati.storage import DataStorage, MediaStorage


def get_storages(api) -> List[Union[DataStorage, MediaStorage]]:
    """Returns list of registered storages."""
    # TODO: Return list of StorageRegistrationInfo
    storages_plugins = api.plugins.find(category="Storage")
    return list(chain.from_iterable(map(
        lambda x: x.get_storages(),
        storages_plugins
    )))


def open_storage(api, path: str, storage_class: type, create: bool = False):
    err = "Unable to open storage."
    scheme, path = path.split("://")

    # protocol and path are required to find proper storage
    if not scheme:
        raise ValueError(f"{err} Protocol is not defined in '{path}'")
    if not path:
        raise ValueError(f"{err} Path is not defined in '{path}'")

    # find storage based on specified protocol and class
    storages = list(filter(
        lambda s: s[0] == scheme and issubclass(s[1], storage_class),
        get_storages(api)))

    # there should be one storage for specified protocol
    if len(storages) > 1:
        raise Exception(f"{err} Too many storages for '{scheme}' protocol.")
    elif storages == 0:
        raise Exception(f"{err} No storage for the '{scheme}' protocol registered.")

    # instatiate the storage
    storage = storages[0]
    root_path = storage[2].get("root_path", "")
    return storage[1](root_path + path, create)

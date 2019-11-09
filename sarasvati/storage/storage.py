"""
Define classes if storage to keep data in.
"""

from abc import ABCMeta, abstractmethod
from collections import namedtuple
from typing import List


StorageInfo = namedtuple("StorageInfo", ["scheme", "type", "data"])


class DataStorage(metaclass=ABCMeta):
    """
    Abstract storage.
    """

    @abstractmethod
    def get(self, key: str) -> dict:
        """
        Get thought by specified key.
        :param key: Key.
        :return: Thought
        """

    @abstractmethod
    def add(self, data: dict) -> None:
        """
        Add thought to the storage.
        :param data: Thought data.
        """

    @abstractmethod
    def update(self, key: str, data: dict) -> None:
        """
        Add thought to the storage.
        :param key: Key of record to update.
        :param data: Thought data.
        """

    @abstractmethod
    def remove(self, key: str) -> None:
        """
        Remove thought from the storage.
        :param key: Key of thought to remove.
        """

    @abstractmethod
    def find(self, query: dict) -> List[dict]:
        """
        Return list of thought that match the specified query.
        :param query: Query.
        :return: List of thoughts data that match the specified query
        """


class MediaStorage(metaclass=ABCMeta):
    """
    Abstract media storage.
    """

    # File management

    @abstractmethod
    def is_file_exists(self, path: str) -> bool:
        """Check existence of a file at specified path."""

    @abstractmethod
    def read_file(self, path: str) -> str:
        """Read a whole content of a file at a specified path."""

    @abstractmethod
    def write_file(self, path: str, content: str) -> str:
        """Write content to a file at the specified path."""

    @abstractmethod
    def delete_file(self, path: str):
        """Delete file at the specified path."""

    # Folders management

    @abstractmethod
    def is_path_exists(self, path: str) -> bool:
        """Check existence of a folder at specified path."""

    @abstractmethod
    def create_folder(self, path: str):
        """Create folder at the specified path."""

    @abstractmethod
    def delete_folder(self, path: str):
        """Delete folder at the specified path."""

    @abstractmethod
    def rename_folder(self, path: str, new_path: str):
        """Rename folder."""

    @abstractmethod
    def open(self, path: str):
        """Open specific path using systems defaults."""

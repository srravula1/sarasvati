from abc import ABCMeta, abstractmethod
from typing import List


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
        pass

    @abstractmethod
    def add(self, data: dict) -> None:
        """
        Add thought to the storage.
        :param data: Thought data.
        """
        pass

    @abstractmethod
    def update(self, key: str, data: dict) -> None:
        """
        Add thought to the storage.
        :param key: Key of record to update.
        :param data: Thought data.
        """
        pass

    @abstractmethod
    def remove(self, key: str) -> None:
        """
        Remove thought from the storage.
        :param key: Key of thought to remove.
        """
        pass

    @abstractmethod
    def find(self, query: dict) -> List[dict]:
        """
        Return list of thought that match the specified query.
        :param query: Query.
        :return: List of thoughts data that match the specified query
        """
        pass


class MediaStorage(metaclass=ABCMeta):
    """
    Abstract media storage.
    """

    @abstractmethod
    def create_folder(self, path: str):
        pass

    @abstractmethod
    def open(self, path: str):
        pass

    @abstractmethod
    def delete_folder(self, path: str):
        pass

    @abstractmethod
    def rename_folder(self, path: str, new_path: str):
        pass


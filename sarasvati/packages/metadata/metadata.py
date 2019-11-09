from abc import ABCMeta, abstractmethod
from typing import Dict

from sarasvati.packages.package import Package


class IMetadataLoader(metaclass=ABCMeta):
    @abstractmethod
    def load(self, url: str) -> str:
        """
        Loada packages metadata from specified url.

        Arguments:
            url {str} -- URL to load metadata from.

        Returns:
            str -- Metadata.
        """


class IMetadataParser(metaclass=ABCMeta):
    @abstractmethod
    def parse(self, data: str) -> Dict[str, Package]:
        """
        Parses packages metadata and returns packages keyed by package id.

        Arguments:
            data {str} -- Metadata

        Returns:
            Dict[str, Package] -- Packages keyed by id.
        """

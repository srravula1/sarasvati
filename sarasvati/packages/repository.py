from typing import Type
from sarasvati.packages import Package, PackageId, PackagesException

from .metadata import IMetadataLoader, IMetadataParser


class Repository:
    """Packages repository."""

    def __init__(self, url: str, loader: Type[IMetadataLoader], parser: Type[IMetadataParser]):
        self.__url = url
        self.__loader = loader()
        self.__parser = parser()
        self.__packages = {}

    @property
    def packages(self):
        return list(self.__packages.values())

    def update(self):
        metadata = self.__loader.load(self.__url)
        packages = self.__parser.parse(metadata)
        self.__packages = packages

    def find_package(self, packageId: PackageId):
        return self.__packages.get(packageId, None)

    def get_package(self, packageId: PackageId):
        if not self.has_package(packageId):
            raise PackagesException(f"No package {packageId} found")
        return self.find_package(packageId)

    def has_package(self, packageId: PackageId):
        return packageId in self.__packages

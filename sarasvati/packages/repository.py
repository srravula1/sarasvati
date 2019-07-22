from sarasvati.packages import Package, PackageId, PackagesException

from .metadata import IMetadataLoader, IMetadataParser


class Repository:
    """Packages repository."""

    def __init__(self, url: str, loader: IMetadataLoader, parser: IMetadataParser):
        self.__loader = loader(url)
        self.__parser = parser()
        self.__packages = {}

    def update(self):
        metadata = self.__loader.load()
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

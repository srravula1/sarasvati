from logging import getLogger

from requests import get as requests_get
from yaml import safe_load as yaml_load
from yaml.scanner import ScannerError

from sarasvati.packages.exceptions import PackagesException
from sarasvati.packages.package import Package, PackageId


class Repository:
    """Packages repository."""

    def __init__(self, url: str):
        self.__url = url
        self.__packages = {}
        self.__log = getLogger("repository")

    def update(self):
        self.__log.info("Fetching repository %s", self.__url)
        meta_data = self.__fetch_metadata(self.__url)
        self.__packages.update(meta_data)
        
        # convert dict to named tuples
        # note: keys order is important
        self.__packages = {
            k: Package(k, v["name"], v["url"], v["author"]) 
            for k, v in self.__packages.items()
        }

    def get_package(self, packageId: PackageId):
        if packageId not in self.__packages:
            raise PackagesException(f"No package {packageId} found")
        return self.__packages[packageId]
        
    def has_package(self, packageId: PackageId):
        return packageId in self.__packages

    @staticmethod
    def __fetch_metadata(url: str) -> dict:
        response = requests_get(url)
        if not response.ok:
            raise PackagesException(f"Unable to fetch repository: {response.status_code} {response.reason}")
        try:
            return yaml_load(response.text)
        except ScannerError as ex:
            raise PackagesException("Repository file is broken. Not a valid YAML file.")

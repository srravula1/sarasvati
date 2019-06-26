from typing import List

from requests import get as requests_get
from yaml.scanner import ScannerError
from yaml import safe_load as yaml_load

from .fetcher import PackageFetcher
from .meta import PackageInfo
from .exception import RepositoryException

PackageId = str

class PackagesRepository:
    def __init__(self, path, urls: List[str]):
        self.__path = path
        self.__urls = urls
        self.__cache = {}
        self.__fetcher = PackageFetcher()

    def update(self):
        for url in self.__urls:
            data = self.__fetch_repository(url)
            self.__cache.update(data)
        self.__cache = {k: PackageInfo(k, v["name"], v["url"]) for k, v in self.__cache.items()}
        print(self.__cache)
        
    def fetch(self, pid: PackageId):
        # get package info
        package_info = self.__cache.get(pid)
        if not package_info:
            raise RepositoryException(f"Unable to fetch package {pid}")

        # download file
        self.__fetcher.fetch(package_info, self.__path)

    def remove(self, pid: PackageId):
        pass

    @staticmethod
    def __fetch_repository(url: str) -> dict:
        response = requests_get(url)
        if not response.ok:
            raise RepositoryException(f"Unable to fetch repository: {response.status_code} {response.reason}")
        try:
            return yaml_load(response.text)
        except ScannerError as ex:
            raise RepositoryException("Repository file is broken. Not a valid YAML file.")

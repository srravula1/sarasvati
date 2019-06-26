from collections import namedtuple
from logging import getLogger
from os.path import join
from typing import List

from download_and_extract import Fetcher, FetcherException
from requests import get as requests_get
from yaml import safe_load as yaml_load
from yaml.scanner import ScannerError

PackageId = str
PackageInfo = namedtuple("PackageInfo", ["key", "name", "url", "author"])

class PackagesRepository:
    def __init__(self, path, urls: List[str]):
        self.__path = path
        self.__urls = urls
        self.__cache = {}
        self.__fetcher = PackageFetcher()
        self.__log = getLogger("repository")

    def update(self):
        # fetch all the repositories and merge it into one cache
        for url in self.__urls:
            self.__log.info("Fetching repository %s", url)
            data = self.__fetch_repository(url)
            self.__cache.update(data)
        
        # convert dict to named tuples
        # note: keys order is important
        self.__log.info("Packages in repository: %d", len(self.__cache.keys()))
        self.__cache = {
            k: PackageInfo(k, v["name"], v["url"], v["author"]) 
            for k, v in self.__cache.items()
        }
        
    def fetch(self, pid: PackageId):
        # get package info
        package_info = self.__cache.get(pid)
        if not package_info:
            raise RepositoryException(f"Package {pid} doesn't exist")

        # download file
        self.__log.info("Fetching package %s", package_info.key)
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


class PackageFetcher:
    """Fetches and extracts package using specified url."""

    def __init__(self):
        """Initializes new instance of the PackagesFetcher class."""
        self.__fetcher = Fetcher()

    def fetch(self, meta: PackageInfo, to: str):
        """
        Fetch packege using meta and download to specified folder.
        
        Arguments:
            meta {PackageInfo} -- Package meta.
            to {str} -- Path to extrack package.
        
        Raises:
            RepositoryException: Error.
        """
        try:
            self.__fetcher.fetch(meta.url, join(to, meta.key))
        except FetcherException as ex:
            msg = ex.args[0]
            raise RepositoryException(msg)


class RepositoryException(BaseException):
    pass

from typing import List
from itertools import chain

from sarasvati.packages import PackageId, PackagesException
from sarasvati.packages.fetcher import PackageFetcher
from sarasvati.packages.metadata import HttpMetadataLoader, YamlMetadataParser
from sarasvati.packages.repository import Repository


class PackagesManager:
    def __init__(self, urls: List[str], path: str):
        self.__repositories = self.__create_repos_from_urls(urls)
        self.__fetcher = PackageFetcher(path)

    @property
    def packages(self):
        return list(chain.from_iterable(map(lambda r: r.packages, self.__repositories)))

    @property
    def repositories(self):
        return self.__repositories

    def update(self):
        for repository in self.__repositories:
            repository.update()

    def add(self, packageId: PackageId):
        candidates = map(
            lambda r: r.find_package(packageId),
            self.__repositories)
        candidates = list(filter(None, candidates))  # remove empty results

        if len(candidates) > 1:
            raise PackagesException("Too many candidates to install")

        self.__fetcher.fetch(candidates[0])

    def remove(self, packageId: PackageId):
        pass

    def find(self, packageId: PackageId):
        pass

    @staticmethod
    def __create_repos_from_urls(urls: List[str]):
        return list(map(lambda x: Repository(x, 
            loader=HttpMetadataLoader, 
            parser=YamlMetadataParser), urls))

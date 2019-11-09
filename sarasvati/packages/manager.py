from itertools import chain
from typing import List

from .exceptions import PackagesException
from .fetcher import PackageFetcher
from .metadata import HttpMetadataLoader, YamlMetadataParser
from .package import PackageId
from .repository import Repository


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
        # find packages in every repository
        candidates = map(
            lambda r: r.find_package(packageId),
            self.__repositories)

        # remove empty results
        # (it returns None if nothing found in repository)
        candidates = [c for c in candidates if c is not None]

        # check for errors:
        # - unable to install package with same ID from different repositories
        # - unable to install pakckage if nothing found
        if not candidates:
            raise PackagesException(f"No '{packageId}' package found")
        if len(candidates) > 1:
            raise PackagesException(
                f"Too many candidates to install for '{packageId}'")

        # fetch packages from repository
        self.__fetcher.fetch(candidates[0])

    def remove(self, packageId: PackageId):
        raise NotImplementedError()

    def find(self, packageId: PackageId):
        raise NotImplementedError()

    @staticmethod
    def __create_repos_from_urls(urls: List[str]):
        return list(map(lambda x: Repository(x,
                                             loader=HttpMetadataLoader,
                                             parser=YamlMetadataParser), urls))

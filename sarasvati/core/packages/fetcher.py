from os.path import join

from download_and_extract import Fetcher, FetcherException

from .exception import RepositoryException
from .meta import PackageInfo


class PackageFetcher():
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

from typing import List

from yaml import safe_load as yaml_load
from yaml.scanner import ScannerError

from sarasvati.packages import Package
from sarasvati.packages.exceptions import PackagesException
from sarasvati.packages.metadata.metadata import IMetadataParser


class YamlMetadataParser(IMetadataParser):
    def parse(self, data: str) -> List[Package]:
        # parse yaml file
        try:
            data = yaml_load(data)
        except ScannerError as ex:
            raise PackagesException(f"Invalid YAML file: {ex.problem}")
    
        # string is a valid yaml, but we are expecting list of packages
        if not isinstance(data, dict):
            raise PackagesException("Metadata is not a dictionary")

        # convert dictionary into Package objects
        return {
            k: Package(k, v["name"], v["url"], v["author"]) 
            for k, v in data.items()
        }

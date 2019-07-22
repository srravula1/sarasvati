from sarasvati.packages.package import Package


class IMetadataLoader:
    def load(self) -> str:
        pass


class IMetadataParser:
    def parse(self, data: str):
        pass

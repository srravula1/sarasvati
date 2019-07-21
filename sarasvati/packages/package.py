from collections import namedtuple

PackageId = str
Package = namedtuple("Package", ["key", "name", "url", "author"])

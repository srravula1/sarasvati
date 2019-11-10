from typing import Any, Callable, List
from uuid import uuid4

from pytest import fixture

from sarasvati.api.sarasvati import Sarasvati

Processor = Callable[[List[str]], Any]


@fixture
def api():
    return Sarasvati()


@fixture
def brain(api: Sarasvati):
    return api.brains.open("local://tests/test_" + uuid4().hex, create=True)


@fixture
def script(api: Sarasvati) -> Processor:
    def _script(commands: List[str]):
        cli = api.plugins.get(category="CommandLine")
        for line in commands:
            cli.execute(line)
    return _script

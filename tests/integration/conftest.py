from typing import Any, Callable, List, Union
from uuid import uuid4

from pytest import fixture

from sarasvati.api.sarasvati import Sarasvati

Processor = Callable[[Union[str, List[str]]], Any]


@fixture
def api():
    return Sarasvati()


@fixture
def brain(api: Sarasvati):
    return api.brains.open("local://tests/test_" + uuid4().hex, create=True)


@fixture
def execute(api: Sarasvati) -> Processor:
    def _script(commands: Union[List[str], str]):
        result = None
        cli = api.plugins.get(category="CommandLine")
        if isinstance(commands, str):
            commands = [commands]
        for line in commands:
            result = cli.execute(line)
        return result
    return _script

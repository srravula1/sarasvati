from pytest import mark
from typing import Any, Callable, List, Union

from sarasvati.brain.brain import Brain

Processor = Callable[[Union[str, List[str]]], Any]


def test_identity_component(brain: Brain, execute: Processor):
    thought = execute("/create-thought Root key:root").data
    assert thought.identity.key == "root"


def test_definition_title(brain: Brain, execute: Processor):
    thought = execute(
        "/create-thought title:Here is a title").data
    assert thought.definition.title == "Here is a title"


@mark.skip(reason="Unable to set description from command line")
def test_definition_description(brain: Brain, execute: Processor):
    thought = execute(
        "/create-thought Root desc:Description").data
    assert thought.definition.description == "Description"

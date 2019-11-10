
from typing import Any, Callable, List, Union

from pytest import mark, raises

from sarasvati.api.sarasvati import Sarasvati
from sarasvati.brain.brain import Brain
from sarasvati.commands.command import CommandException

Processor = Callable[[Union[str, List[str]]], Any]


def test_no_active_brain_at_start(api: Sarasvati):
    assert api.brains.active is None


def test_open_brain_without_storage(api: Sarasvati):
    with raises(ValueError) as ex:
        api.brains.open("default")

    assert ex.value.args[0] == "Path to brain should be in format <storage>://<path>"
    assert api.brains.active is None


def test_open_brain_with_local_storage(api: Sarasvati):
    api.brains.open("local://tests/default", create=True)
    assert api.brains.active is not None


def test_open_brain_set_name(api: Sarasvati):
    api.brains.open("local://tests/default", create=True)
    assert api.brains.active.name == "default"


def test_activate_thought(brain: Brain, execute: Processor):
    execute(["/create-thought Root",
             "/activate-thought Root"])
    assert brain.active_thought is not None
    assert brain.active_thought.title == "Root"


def test_activate_thought_what_doesnt_exist(brain: Brain, execute: Processor):
    with raises(CommandException) as ex:
        execute(["/activate-thought Root"])
    assert brain.active_thought is None
    assert ex.value.args[0] == "Nothing found"


def test_create_child_thought(brain: Brain, execute: Processor):
    root = execute(["/create-thought Root",
                    "/activate-thought Root"]).data
    child = execute("/create-thought Child as:child").data
    assert child.title == "Child"
    assert root in child.links.parents
    assert child in root.links.children
    assert len(child.links.all) == 1


def test_create_parent_thought(brain: Brain, execute: Processor):
    root = execute(["/create-thought Root",
                    "/activate-thought Root"]).data
    parent = execute("/create-thought Parent as:parent").data
    assert parent in root.links.parents
    assert root in parent.links.children


def test_create_reference_thought(brain: Brain, execute: Processor):
    root = execute(["/create-thought Root",
                    "/activate-thought Root"]).data
    reference = execute("/create-thought Reference as:reference").data
    assert reference in root.links.references
    assert root in reference.links.references


def test_create_thought_without_title(brain: Brain, execute: Processor):
    with raises(CommandException) as ex:
        execute("/create-thought")
    assert ex.value.args[0] == "No title provided"


@mark.parametrize("command", ["/create-parent", "/create-reference", "/create-child"])
def test_create_thoughts_without_title(command: str, brain: Brain, execute: Processor):
    execute(["/create-thought Root", "/activate-thought Root"])
    with raises(CommandException) as ex:
        execute(command)
    assert ex.value.args[0] == "No title provided"


@mark.parametrize("command", ["/create-parent", "/create-reference", "/create-child"])
def test_create_thoughts_requires_active_thought(command: str, brain: Brain, execute: Processor):
    with raises(CommandException) as ex:
        execute(command)
    assert ex.value.args[0] == "No active thought"

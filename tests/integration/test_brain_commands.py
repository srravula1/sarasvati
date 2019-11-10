
from typing import Any, Callable, List

from pytest import raises

from sarasvati.api.sarasvati import Sarasvati
from sarasvati.brain.brain import Brain
from sarasvati.commands.command import CommandException

Processor = Callable[[List[str]], Any]


def test_no_active_brain_at_start(api: Sarasvati):
    assert api.brains.active is None


def test_open_brain_without_storage(api: Sarasvati):
    with raises(ValueError) as ex:
        api.brains.open("default")

    assert ex.value.args[0] == "Path to brain should be in format <storage>://<path>"
    assert api.brains.active is None


def test_open_brain_with_local_storage(api: Sarasvati):
    api.brains.open("local://default")
    assert api.brains.active is not None


def test_open_brain_set_name(api: Sarasvati):
    api.brains.open("local://default")
    assert api.brains.active.name == "default"


def test_activate_thought(brain: Brain, script: Processor):
    script(["/create-thought Root",
            "/activate-thought Root"])
    assert brain.active_thought is not None
    assert brain.active_thought.title == "Root"


def test_activate_thought_what_doesnt_exist(brain: Brain, script: Processor):
    with raises(CommandException) as ex:
        script(["/activate-thought Root"])
    assert brain.active_thought is None
    assert ex.value.args[0] == "Nothing found"

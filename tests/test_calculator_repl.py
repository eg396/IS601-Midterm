## test_calculator_repl.py
## IS601 Midterm
## Evan Garvey

import builtins
from types import SimpleNamespace
from unittest.mock import MagicMock, patch
import pytest

from app.calculator_repl import calculator_repl
from app.calculator import Calculator
from app.exceptions import ValidationError
import app.calculator_repl as cr

    ## By far my least favorite file in this project.
    ## A monstrosity of unit tests that extends far beyond the lines they could have been efficiently reduced to.
    ## I'm sorry.

def test_repl_exit_with_save_error(capsys):
    # Mock input to simulate the user typing "exit" immediately
    inputs = ["exit"]
    input_mock = lambda _: inputs.pop(0)

    # Patch Calculator and its methods
    with patch("app.calculator_repl.Calculator") as MockCalculator:
        instance = MockCalculator.return_value
        instance.config.history_file = "mock_file.csv"
        instance.save_history.side_effect = Exception("mock save error")
        instance.add_observer = MagicMock()

        with patch.object(builtins, "input", side_effect=input_mock):
            calculator_repl()

        # Capture printed output
        captured = capsys.readouterr()
        assert "Error saving history: mock save error" in captured.out
        assert "Goodbye!" in captured.out

def test_repl_history_empty(capsys):
    # Simulate user typing "history" then "exit"
    inputs = ["history", "exit"]
    input_mock = lambda _: inputs.pop(0)

    with patch("app.calculator_repl.Calculator") as MockCalculator:
        instance = MockCalculator.return_value
        instance.config.history_file = "mock_file.csv"
        instance.show_history.return_value = []  # Simulate empty history
        instance.save_history = MagicMock()
        instance.add_observer = MagicMock()

        with patch.object(builtins, "input", side_effect=input_mock):
            calculator_repl()

        captured = capsys.readouterr()
        assert "History is empty." in captured.out
        assert "Goodbye!" in captured.out

def test_repl_history_nonempty(capsys):
    # Simulate user typing "history" then "exit"
    inputs = ["history", "exit"]
    input_mock = lambda _: inputs.pop(0)

    with patch("app.calculator_repl.Calculator") as MockCalculator:
        instance = MockCalculator.return_value
        instance.config.history_file = "mock_file.csv"
        # Simulate non‐empty history
        instance.show_history.return_value = ["add (2, 3) = 5", "mul (4, 5) = 20"]
        instance.save_history = MagicMock()
        instance.add_observer = MagicMock()

        with patch.object(builtins, "input", side_effect=input_mock):
            calculator_repl()

        captured = capsys.readouterr()
        # Should print the header
        assert "\nHistory:" in captured.out
        # And each entry numbered
        assert "1. add (2, 3) = 5" in captured.out
        assert "2. mul (4, 5) = 20" in captured.out
        assert "Goodbye!" in captured.out

def test_repl_clear_history(capsys):
    # Simulate user typing "clear" then "exit"
    inputs = ["clear", "exit"]
    input_mock = lambda _: inputs.pop(0)

    with patch("app.calculator_repl.Calculator") as MockCalculator:
        instance = MockCalculator.return_value

        # clear_history should be called
        instance.clear_history = MagicMock()
        # Other methods needed for REPL
        instance.save_history = MagicMock()
        instance.add_observer = MagicMock()

        with patch.object(builtins, "input", side_effect=input_mock):
            calculator_repl()

        captured = capsys.readouterr()
        # Ensure clear_history was invoked
        instance.clear_history.assert_called_once()
        # And that the REPL printed the confirmation
        assert "History cleared." in captured.out
        assert "Goodbye!" in captured.out

def test_repl_undo_no_history(capsys):
    # Simulate user typing "undo" then "exit"
    inputs = ["undo", "exit"]
    input_mock = lambda _: inputs.pop(0)

    with patch("app.calculator_repl.Calculator") as MockCalculator:
        instance = MockCalculator.return_value
        instance.undo.return_value = False
        instance.save_history = MagicMock()
        instance.add_observer = MagicMock()

        with patch.object(builtins, "input", side_effect=input_mock):
            calculator_repl()

        captured = capsys.readouterr()
        # The REPL should print the "no history" message
        assert "No calculations to undo." in captured.out
        assert "Goodbye!" in captured.out

def test_repl_undo_with_history(capsys):
    # Simulate user typing "undo" then "exit"
    inputs = ["undo", "exit"]
    input_mock = lambda _: inputs.pop(0)

    with patch("app.calculator_repl.Calculator") as MockCalculator:
        instance = MockCalculator.return_value
        instance.undo.return_value = True
        instance.save_history = MagicMock()
        instance.add_observer = MagicMock()

        with patch.object(builtins, "input", side_effect=input_mock):
            calculator_repl()

        captured = capsys.readouterr()
        # The REPL should print the "last calculation undone" message
        assert "Last calculation undone." in captured.out
        assert "Goodbye!" in captured.out

def test_repl_redo_no_history(capsys):
    # Simulate user typing "redo" then "exit"
    inputs = ["redo", "exit"]
    input_mock = lambda _: inputs.pop(0)

    with patch("app.calculator_repl.Calculator") as MockCalculator:
        instance = MockCalculator.return_value
        instance.redo.return_value = False
        instance.save_history = MagicMock()
        instance.add_observer = MagicMock()

        with patch.object(builtins, "input", side_effect=input_mock):
            calculator_repl()

        captured = capsys.readouterr()
        # Should hit the "no calculations to redo" branch
        assert "No calculations to redo." in captured.out
        assert "Goodbye!" in captured.out

def test_repl_redo_with_history(capsys):
    # Simulate user typing "redo" then "exit"
    inputs = ["redo", "exit"]
    input_mock = lambda _: inputs.pop(0)

    with patch("app.calculator_repl.Calculator") as MockCalculator:
        instance = MockCalculator.return_value
        instance.redo.return_value = True
        instance.save_history = MagicMock()
        instance.add_observer = MagicMock()

        with patch.object(builtins, "input", side_effect=input_mock):
            calculator_repl()

        captured = capsys.readouterr()
        # Should hit the "last calculation redone" branch
        assert "Last calculation redone." in captured.out
        assert "Goodbye!" in captured.out

def test_repl_save_success(capsys):
    # Simulate user typing "save" then "exit"
    inputs = ["save", "exit"]
    input_mock = lambda _: inputs.pop(0)

    with patch("app.calculator_repl.Calculator") as MockCalculator:
        instance = MockCalculator.return_value
        # save_history succeeds
        instance.save_history = MagicMock()
        instance.add_observer = MagicMock()

        with patch.object(builtins, "input", side_effect=input_mock):
            calculator_repl()

        captured = capsys.readouterr()
        # The REPL should print the success message
        assert "History saved to file successfully." in captured.out
        assert "Goodbye!" in captured.out

def test_repl_save_error(capsys):
    # Simulate user typing "save" then "exit"
    inputs = ["save", "exit"]
    input_mock = lambda _: inputs.pop(0)

    with patch("app.calculator_repl.Calculator") as MockCalculator:
        instance = MockCalculator.return_value
        # Make save_history raise
        instance.save_history.side_effect = Exception("mock save failure")
        instance.add_observer = MagicMock()

        with patch.object(builtins, "input", side_effect=input_mock):
            calculator_repl()

        captured = capsys.readouterr()
        # The REPL should print the error message
        assert "Error saving history: mock save failure" in captured.out
        assert "Goodbye!" in captured.out

def test_repl_load_success(capsys):
    # Simulate user typing "load" then "exit"
    inputs = ["load", "exit"]
    input_mock = lambda _: inputs.pop(0)

    with patch("app.calculator_repl.Calculator") as MockCalculator:
        inst = MockCalculator.return_value
        # load_history succeeds
        inst.load_history = MagicMock()
        inst.save_history = MagicMock()
        inst.add_observer = MagicMock()

        with patch.object(builtins, "input", side_effect=input_mock):
            calculator_repl()

        out = capsys.readouterr().out
        assert "History loaded from file successfully." in out
        assert "Goodbye!" in out

def test_repl_load_error(capsys):
    # Simulate user typing "load" then "exit"
    inputs = ["load", "exit"]
    input_mock = lambda _: inputs.pop(0)

    with patch("app.calculator_repl.Calculator") as MockCalculator:
        inst = MockCalculator.return_value
        # load_history raises
        inst.load_history.side_effect = Exception("mock load error")
        inst.save_history = MagicMock()
        inst.add_observer = MagicMock()

        with patch.object(builtins, "input", side_effect=input_mock):
            calculator_repl()

        out = capsys.readouterr().out
        assert "Error loading history: mock load error" in out
        assert "Goodbye!" in out

class CancelStr(str):
    @property
    def lower(self):
        return "cancel"
    
def test_repl_calculation_cancel_num1(capsys):
    # Simulate: command="add", num1="(cancel)", then exit
    inputs = ["add", CancelStr("anything"), "exit"]
    input_mock = lambda _: inputs.pop(0)

    with patch("app.calculator_repl.Calculator") as MockCalc, \
         patch("app.calculator_repl.OperationFactory") as MockFactory:
        inst = MockCalc.return_value
        inst.add_observer = MagicMock()
        inst.save_history = MagicMock()
        # Ensure OperationFactory.create won't be used after cancel
        MockFactory.create.return_value = MagicMock()

        with patch.object(builtins, "input", side_effect=input_mock):
            calculator_repl()

        captured = capsys.readouterr()
        assert "Calculation cancelled." in captured.out
        assert "Goodbye!" in captured.out

def test_repl_calculation_cancel_num2(capsys):
    # Simulate: command="add", valid num1, then cancel at num2, then exit
    inputs = ["add", "2", CancelStr("ignored"), "exit"]
    input_mock = lambda _: inputs.pop(0)

    with patch("app.calculator_repl.Calculator") as MockCalc, \
         patch("app.calculator_repl.OperationFactory") as MockFactory:
        inst = MockCalc.return_value
        inst.add_observer = MagicMock()
        inst.save_history = MagicMock()
        MockFactory.create.return_value = MagicMock()

        with patch.object(builtins, "input", side_effect=input_mock):
            calculator_repl()

        captured = capsys.readouterr()
        assert "Calculation cancelled." in captured.out
        assert "Goodbye!" in captured.out

def test_repl_calculation_validation_error(capsys):
    # Simulate "add", invalid input causing ValidationError, then exit
    inputs = ["add", "foo", "2", "exit"]
    input_mock = lambda _: inputs.pop(0)

    with patch("app.calculator_repl.Calculator") as MockCalc, \
         patch("app.calculator_repl.OperationFactory") as MockFactory:
        inst = MockCalc.return_value
        inst.add_observer = MagicMock()
        inst.save_history = MagicMock()
        inst.show_history = MagicMock(return_value=[])
        # simulate perform_operation raising ValidationError
        inst.perform_operation.side_effect = ValidationError("bad input")

        MockFactory.create.return_value = MagicMock()

        with patch.object(builtins, "input", side_effect=input_mock):
            calculator_repl()

        out = capsys.readouterr().out
        assert "Error: bad input" in out
        assert "Goodbye!" in out


def test_repl_calculation_unexpected_error(capsys):
    # Simulate "add", valid first number, valid second number,
    # but perform_operation raises a generic Exception
    inputs = ["add", "1", "2", "exit"]
    input_mock = lambda _: inputs.pop(0)

    with patch("app.calculator_repl.Calculator") as MockCalc, \
         patch("app.calculator_repl.OperationFactory") as MockFactory:
        inst = MockCalc.return_value
        inst.add_observer = MagicMock()
        inst.save_history = MagicMock()
        inst.show_history = MagicMock(return_value=[])
        # simulate perform_operation raising a generic exception
        inst.perform_operation.side_effect = Exception("boom")

        MockFactory.create.return_value = MagicMock()

        with patch.object(builtins, "input", side_effect=input_mock):
            calculator_repl()

        out = capsys.readouterr().out
        assert "Unexpected error: boom" in out
        assert "Goodbye!" in out

def test_repl_unknown_command(capsys):
    # Simulate: unknown command then exit
    inputs = ["foobar", "exit"]
    input_mock = lambda _: inputs.pop(0)

    with patch("app.calculator_repl.Calculator") as MockCalc:
        inst = MockCalc.return_value
        inst.save_history = MagicMock()
        inst.add_observer = MagicMock()

        with patch.object(builtins, "input", side_effect=input_mock):
            calculator_repl()

        out = capsys.readouterr().out
        assert "Unknown command: foobar. type 'help' for commands." in out
        assert "Goodbye!" in out


def test_repl_keyboard_interrupt(capsys):
    # First input() raises KeyboardInterrupt, then 'exit'
    def side_effect(prompt):
        # on first call, raise; then return 'exit'
        if side_effect.called:
            return "exit"
        side_effect.called = True
        raise KeyboardInterrupt()
    side_effect.called = False

    with patch("app.calculator_repl.Calculator") as MockCalc:
        inst = MockCalc.return_value
        inst.save_history = MagicMock()
        inst.add_observer = MagicMock()

        with patch.object(builtins, "input", side_effect=side_effect):
            calculator_repl()

        out = capsys.readouterr().out
        assert "Operation cancelled: KeyboardInterrupt detected." in out
        assert "Goodbye!" in out


def test_repl_eof_error(capsys):
    # First input() raises EOFError — REPL should print the message and exit loop
    inputs = []
    def side_effect(prompt):
        raise EOFError()

    with patch("app.calculator_repl.Calculator") as MockCalc:
        inst = MockCalc.return_value
        inst.save_history = MagicMock()
        inst.add_observer = MagicMock()

        with patch.object(builtins, "input", side_effect=side_effect):
            calculator_repl()

        out = capsys.readouterr().out
        assert "EOFError detected: terminating program..." in out
        # Should not print Goodbye here, since exit path is different
        assert "Goodbye!" not in out


def test_repl_clear_raises_generic_error(capsys):
    # Simulate user typing "clear" then "exit", but clear_history raises an unexpected Exception
    inputs = ["clear", "exit"]
    input_mock = lambda _: inputs.pop(0)

    with patch("app.calculator_repl.Calculator") as MockCalc:
        inst = MockCalc.return_value
        # Make clear_history throw a generic exception
        inst.clear_history.side_effect = Exception("clear boom")
        inst.save_history = MagicMock()
        inst.add_observer = MagicMock()

        with patch.object(builtins, "input", side_effect=input_mock):
            calculator_repl()

    out = capsys.readouterr().out
    # Should catch the generic exception and print it
    assert "Error: clear boom" in out
    assert "Goodbye!" in out


class FakeInitError(Exception):
    pass

def test_repl_fatal_error_during_init(monkeypatch, capsys):
    # 1) Create a dummy Calculator with the methods/attrs we need
    dummy = SimpleNamespace()
    dummy.config = SimpleNamespace(history_file="dummy.csv")
    dummy.add_observer = lambda obs: None
    dummy._send_message = lambda level, msg: None  # no-op

    # 2) Patch Calculator() to return our dummy
    monkeypatch.setattr(cr, "Calculator", lambda *a, **k: dummy)

    # 3) Patch AutoSaveObserver to throw, simulating a failure in setup
    monkeypatch.setattr(cr, "AutoSaveObserver",
                        lambda path: (_ for _ in ()).throw(FakeInitError("autosave init boom")))

    # 4) Run and assert
    with pytest.raises(FakeInitError):
        cr.calculator_repl()

    out = capsys.readouterr().out
    assert "Fatal error during initialization: autosave init boom" in out
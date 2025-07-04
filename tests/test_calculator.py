import datetime
import os
from pathlib import Path
import tempfile
from unittest import mock
import pandas as pd
from app.calculation import Calculation
from app.logger import CalculationLogger
import pytest
from unittest.mock import MagicMock, Mock, patch, PropertyMock
from decimal import Decimal
from tempfile import TemporaryDirectory
from app.calculator import Calculator
from app.calculator_repl import calculator_repl
from app.calculator_config import CalculatorConfig
from app.exceptions import OperationError, ValidationError
from app.history import LoggingObserver, AutoSaveObserver
from app.operations import Addition, OperationFactory

@pytest.fixture
def calculator():
    with TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        config = CalculatorConfig(root_dir=temp_path)

        with patch.object(CalculatorConfig, 'log_dir', new_callable=PropertyMock) as mock_log_dir, \
             patch.object(CalculatorConfig, 'log_file', new_callable=PropertyMock) as mock_log_file, \
             patch.object(CalculatorConfig, 'history_dir', new_callable=PropertyMock) as mock_history_dir, \
             patch.object(CalculatorConfig, 'history_file', new_callable=PropertyMock) as mock_history_file:
            
            mock_log_dir.return_value = temp_path / "logs"
            mock_log_file.return_value = temp_path / "logs/calculator.log"
            mock_history_dir.return_value = temp_path / "history"
            mock_history_file.return_value = temp_path / "history/calculator_history.csv"
            
            yield Calculator(config=config)

def test_calculator_initialization(calculator):
    assert calculator.history == []
    assert calculator.undo_stack == []
    assert calculator.redo_stack == []
    assert calculator.operation_strategy is None

@patch('app.logger.CalculationLogger.log_info')
def test_logging_setup(mock_log_info):
    calc = Calculator(CalculatorConfig())
    mock_log_info.assert_any_call(mock.ANY)

def test_add_observer(calculator):
    observer = LoggingObserver(CalculationLogger())
    calculator.add_observer(observer)
    assert observer in calculator.observers

def test_remove_observer(calculator):
    observer = LoggingObserver(CalculationLogger())
    calculator.add_observer(observer)
    calculator.remove_observer(observer)
    assert observer not in calculator.observers

def test_set_operation(calculator):
    operation = OperationFactory.create('add')
    calculator.set_operation(operation)
    assert calculator.operation_strategy == operation

def test_perform_operation_addition(calculator):
    operation = OperationFactory.create('add')
    calculator.set_operation(operation)

    try:
        result = calculator.perform_operation(2, 3)
    except Exception as e:
        print("Exception during perform_operation:", e)
        raise

    print("Result:", result)
    assert result == Decimal('5')

def test_perform_operation_validation_error(calculator):
    calculator.set_operation(OperationFactory.create('add'))
    with pytest.raises(ValidationError):
        calculator.perform_operation('invalid', 3)

def test_perform_operation_operation_error(calculator):
    with pytest.raises(OperationError, match="No operation set"):
        calculator.perform_operation(2, 3)

def test_undo(calculator):
    operation = OperationFactory.create('add')
    calculator.set_operation(operation)
    calculator.perform_operation(2, 3)
    calculator.undo()
    assert calculator.history == []

def test_redo(calculator):
    operation = OperationFactory.create('add')
    calculator.set_operation(operation)
    calculator.perform_operation(2, 3)
    calculator.undo()
    calculator.redo()
    assert len(calculator.history) == 1

@patch('app.calculator.pd.DataFrame.to_csv')
def test_save_history(mock_to_csv, calculator):
    operation = OperationFactory.create('add')
    calculator.set_operation(operation)
    calculator.perform_operation(2, 3)
    calculator.save_history()
    mock_to_csv.assert_called_once()

@patch('app.calculator.pd.read_csv')
@patch('app.calculator.Path.exists', return_value=True)
def test_load_history(mock_exists, mock_read_csv, calculator):
    mock_read_csv.return_value = pd.DataFrame({
        'operation': ['add'],
        'num1': ['2'],
        'num2': ['3'],
        'result': ['5'],
        'timestamp': [datetime.datetime.now().isoformat()]
    })

    try:
        calculator.load_history()

        assert len(calculator.history) == 1
        assert calculator.history[0].operation == "add"
        assert calculator.history[0].num1 == Decimal("2")
        assert calculator.history[0].num2 == Decimal("3")
        assert calculator.history[0].result == Decimal("5")
    except OperationError:
        pytest.fail("Loading history failed due to OperationError")

def test_clear_history(calculator):
    operation = OperationFactory.create('add')
    calculator.set_operation(operation)
    calculator.perform_operation(2, 3)
    calculator.clear_history()
    assert calculator.history == []
    assert calculator.undo_stack == []
    assert calculator.redo_stack == []

@patch('builtins.input', side_effect=['exit'])
@patch('builtins.print')
def test_calculator_repl_exit(mock_print, mock_input):
    with patch('app.calculator.Calculator.save_history') as mock_save_history:
        mock_save_history.return_value = None  
        calculator_repl()
        mock_save_history.assert_called_once()
        mock_print.assert_any_call("History saved to file successfully.")
        mock_print.assert_any_call("Goodbye!")

@patch('builtins.input', side_effect=['help', 'exit'])
@patch('builtins.print')
def test_calculator_repl_help(mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("\nAvailable commands:")

@patch('builtins.input', side_effect=['add', '2', '3', 'exit'])
@patch('builtins.print')
def test_calculator_repl_addition(mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("Result: 5")


def test_calculator_init_load_history_failure_raises():
    with patch.object(Calculator, 'load_history', side_effect=Exception("Load failure")):
        with pytest.raises(Exception, match="Load failure"):
            Calculator()


def test_setup_logging_error(capsys):
    # Mock os.makedirs to raise an OSError
    with patch('os.makedirs', side_effect=OSError("mocked makedirs failure")):
        calc = Calculator.__new__(Calculator)

        class DummyConfig:
            log_dir = Path("/tmp/logs")
            log_file = Path("/tmp/logs/log.txt")
        calc.config = DummyConfig()

        with pytest.raises(OSError, match="mocked makedirs failure"):

            calc._setup_logging()

        captured = capsys.readouterr()

        assert "Error setting up logging: mocked makedirs failure" in captured.out

def test_perform_operation_history_pop_minimal():
    calc = Calculator()
    calc.config.max_history = 2
    calc.operation_strategy = Addition()
    
    # Fill history with max allowed
    calc.history = [
        Calculation(operation="add", num1=Decimal(1), num2=Decimal(1)),
        Calculation(operation="add", num1=Decimal(2), num2=Decimal(2)),
    ]

    calc.perform_operation("3", "3")

    # The history length should not exceed max_history
    assert len(calc.history) == 2

def test_perform_operation_raises_and_catches(monkeypatch):
    calc = Calculator()
    calc.operation_strategy = MagicMock()
    
    # Make execute raise an Exception
    calc.operation_strategy.execute.side_effect = Exception("Forced failure")
    
    # Patch _send_message to monitor calls
    sent_messages = []
    calc._send_message = lambda level, msg: sent_messages.append((level, msg))
    
    with pytest.raises(Exception, match="Forced failure"):
        calc.perform_operation("1", "1")
    
    # Confirm _send_message was called with level 40 and message contains "Operation Failed"
    assert any(level == 40 and "Operation Failed" in msg for level, msg in sent_messages)


def test_save_history_empty(monkeypatch):
    calc = Calculator()
    calc.history = []  # Empty history triggers else block

    messages = []
    calc._send_message = lambda level, msg: messages.append((level, msg))

    monkeypatch.setenv("CALCULATOR_HISTORY_FILE", "test_history_empty.csv")

    calc.save_history()

    assert any("Empty history saved" in msg for level, msg in messages)


def test_save_history_raises(monkeypatch):
    calc = Calculator()
    calc.history = [
        Calculation(operation="add", num1=Decimal(1), num2=Decimal(1)),
        Calculation(operation="add", num1=Decimal(2), num2=Decimal(2)),
    ]

    messages = []
    calc._send_message = lambda level, msg: messages.append((level, msg))

    with patch("pandas.DataFrame.to_csv", side_effect=Exception("mocked to_csv failure")):
        with pytest.raises(OperationError, match="Error saving history: mocked to_csv failure"):
            calc.save_history()

    assert any("Error saving history: mocked to_csv failure" in msg for level, msg in messages)

def test_load_empty_history_file():

    # Patch Path.exists globally to always return True
    with patch('pathlib.Path.exists', return_value=True):
        # Patch pd.read_csv to return an empty DataFrame
        with patch('pandas.read_csv', return_value=pd.DataFrame()):

            calc = Calculator()
            messages = []
            calc._send_message = lambda level, msg: messages.append((level, msg))

            calc.load_history()

            assert any("Loaded empty history file" in msg for level, msg in messages)
            assert calc.history == []

def test_load_history_raises_operation_error():
    with patch('pathlib.Path.exists', return_value=True), \
         patch('pandas.read_csv', side_effect=Exception("mocked read_csv failure")):

        # Catch the OperationError raised from __init__ when load_history is called
        with pytest.raises(OperationError, match="Error loading history: mocked read_csv failure"):
            Calculator()

def test_get_history_dataframe_simple():
    calc = Calculator()

    # Create minimal Calculation mocks with needed attributes as strings
    class SimpleCalc:
        def __init__(self, operation, num1, num2, result, timestamp):
            self.operation = operation
            self.num1 = num1
            self.num2 = num2
            self.result = result
            self.timestamp = timestamp

    # Add two simple Calculation-like objects to history
    calc.history = [
        SimpleCalc('add', '2', '3', '5', '2025-07-04T12:00:00'),
        SimpleCalc('mul', '4', '5', '20', '2025-07-04T12:01:00')
    ]

    df = calc.get_history_dataframe()

    # Basic assertions
    assert len(df) == 2
    assert set(df.columns) == {'operation', 'num1', 'num2', 'result', 'timestamp'}
    assert df.iloc[0]['operation'] == 'add'
    assert df.iloc[1]['result'] == '20'

def test_show_history():
    calc = Calculator()

    # Create simple Calculation-like objects
    class SimpleCalc:
        def __init__(self, operation, num1, num2, result):
            self.operation = operation
            self.num1 = num1
            self.num2 = num2
            self.result = result

    calc.history = [
        SimpleCalc("add", 2, 3, 5),
        SimpleCalc("mul", 4, 5, 20),
    ]

    expected = [
        "add (2m 3) = 5",
        "mul (4m 5) = 20",
    ]

    assert calc.show_history() == expected

def test_undo_returns_false_when_empty():
    calc = Calculator()
    calc.undo_stack.clear()  # make sure undo_stack is empty
    assert calc.undo() is False

def test_redo_returns_false_when_empty():
    calc = Calculator()
    calc.redo_stack.clear()  # make sure redo_stack is empty
    assert calc.redo() is False
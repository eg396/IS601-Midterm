from pathlib import Path
import tempfile
from app.logger import CalculationLogger
import pytest
from unittest.mock import Mock, call, patch
from app.calculation import Calculation
from app.history import LoggingObserver, AutoSaveObserver
from app.calculator import Calculator
from app.calculator_config import CalculatorConfig

calculation_mock = Mock(spec=Calculation)
calculation_mock.operation = "addition"
calculation_mock.num1 = 5
calculation_mock.num2 = 3
calculation_mock.result = 8
calculation_mock.timestamp = "2021-01-01 00:00:00"
test_logger = CalculationLogger()

@patch.object(CalculationLogger, '_log')
def test_logging_observer_logs_calculation(logging_info_mock):

    observer = LoggingObserver(test_logger)
    observer.update(calculation_mock)
    logging_info_mock.assert_called_once_with(
        20, 'History updated: addition, (5, 3) = 8'
    )

def test_logging_observer_no_calculation():

    observer = LoggingObserver(test_logger)
    with pytest.raises(AttributeError):
        observer.update(None)


@patch('pandas.DataFrame.to_csv')
def test_autosave_observer_triggers_save(mock_to_csv):
    observer = AutoSaveObserver("fake_path.csv")

    calc_mock = Mock(spec=Calculation)
    calc_mock.operation = "add"
    calc_mock.num1 = 1
    calc_mock.num2 = 2
    calc_mock.result = 3
    calc_mock.timestamp = "2024-07-03T12:00:00"

    observer.update(calc_mock)

    mock_to_csv.assert_called_once()

@patch("pandas.DataFrame.to_csv")
def test_autosave_observer_triggers_save(mock_to_csv):
    observer = AutoSaveObserver("test_autosave.csv")

    calculation_mock = Mock(spec=Calculation)
    calculation_mock.operation = "add"
    calculation_mock.num1 = 1
    calculation_mock.num2 = 2
    calculation_mock.result = 3
    calculation_mock.timestamp = "2024-01-01T00:00:00Z"

    observer.update(calculation_mock)

    mock_to_csv.assert_called_once_with("test_autosave.csv", index=False)

@patch("pandas.DataFrame.to_csv")
def test_autosave_observer_does_not_trigger_save_when_disabled(mock_to_csv):

    observer = AutoSaveObserver("dummy_path.csv")  # Not actually used because we patch

    # Set up a mock Calculation
    calculation_mock = Mock(spec=Calculation)
    calculation_mock.operation = "subtract"
    calculation_mock.num1 = 5
    calculation_mock.num2 = 3
    calculation_mock.result = 2
    calculation_mock.timestamp = "2024-01-01T00:00:00Z"

    observer.calculator = Mock()
    observer.calculator.config = Mock()
    observer.calculator.config.auto_save = False
    observer.update(calculation_mock)

    mock_to_csv.assert_called_once_with("dummy_path.csv", index=False)

def test_autosave_observer_invalid_calculator():
    with pytest.raises(TypeError):
        AutoSaveObserver(None)  

def test_autosave_observer_no_calculation():

    calculator_mock = Mock(spec=Calculator)
    calculator_mock.config = Mock(spec=CalculatorConfig)
    calculator_mock.config.auto_save = True
    observer = AutoSaveObserver(calculator_mock)
    with pytest.raises(AttributeError):
        observer.update(None) 

def test_update_message_suite():

    logger_mock = Mock()
    observer = LoggingObserver(logger_mock)

    observer.update_message(20, 'History updated: addition, (5, 3) = 8')
    observer.update_message(30, 'Warning: This is a warning message')
    observer.update_message(40, 'Error: This is an error message')
    observer.update_message(50030, 'Unknown log level: 50030')

    logger_mock.log_info.assert_called_once_with('History updated: addition, (5, 3) = 8')
    logger_mock.log_warning.assert_called_once_with('Warning: This is a warning message')
    logger_mock.log_error.assert_has_calls([
        call('Error: This is an error message'),
        call('Invalid level: 50030')
    ])
    assert logger_mock.log_error.call_count == 2

def test_autosave_observer_writes_csv():
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:
        observer = AutoSaveObserver(tmp.name)

        calc_mock = Mock(spec=Calculation)
        calc_mock.operation = "add"
        calc_mock.num1 = 1
        calc_mock.num2 = 2
        calc_mock.result = 3
        calc_mock.timestamp = "2024-07-04T00:00:00"

        observer.update(calc_mock)

        tmp_path = Path(tmp.name)
        assert tmp_path.exists()
        content = tmp_path.read_text()
        assert "add" in content
        assert "1" in content
        assert "2" in content
        assert "3" in content

    tmp_path.unlink()  # Remove temp file after test
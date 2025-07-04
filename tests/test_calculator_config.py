## test_calculator_config.py
## IS 601 Midterm
## Evan Garvey

from decimal import Decimal
from numbers import Number
import os
from pathlib import Path
from typing import Optional
import pytest

from app.calculator_config import CalculatorConfig
from app.exceptions import ConfigurationError

os.environ['CALCULATOR_MAX_HISTORY'] = '1000'
os.environ['CALCULATOR_AUTO_SAVE'] = 'false'
os.environ['CALCULATOR_PRECISION'] = '8'
os.environ['CALCULATOR_MAX_INPUT_VAL'] = '1000'
os.environ['CALCULATOR_DEFAULT_ENCODING'] = 'utf-16'
os.environ['CALCULATOR_LOG_DIR'] = './test_logs'
os.environ['CALCULATOR_HISTORY_DIR'] = './test_history'
os.environ['CALCULATOR_HISTORY_FILE'] = './test_history/test_history.csv'
os.environ['CALCULATOR_LOG_FILE'] = './test_logs/test_log.log'

def clear_env_vars(*args):
    
    for var in args:
        os.environ.pop(var, None)

def test_default_configuration():

    config = CalculatorConfig()
    assert config.max_history == 1000
    assert config.auto_save is False
    assert config.precision == 8
    assert config.max_input_val == Decimal("1000")
    assert config.default_encoding == 'utf-16'
    assert config.log_dir == Path('./test_logs').resolve()
    assert config.history_dir == Path('./test_history').resolve()
    assert config.history_file == Path('./test_history/test_history.csv').resolve()
    assert config.log_file == Path('./test_logs/test_log.log').resolve()

def test_custom_configuration():

    config = CalculatorConfig(
        max_history=300,
        auto_save=True,
        precision=5,
        max_input_val=Decimal("500"),
        default_encoding="ascii"
    )

    assert config.max_history == 300
    assert config.auto_save is True
    assert config.precision == 5
    assert config.max_input_val == Decimal("500")
    assert config.default_encoding == "ascii"

def test_directory_properties():

    clear_env_vars('CALCULATOR_LOG_DIR', 'CALCULATOR_HISTORY_DIR')
    config = CalculatorConfig(root_dir=Path('/custom_base_dir'))
    assert config.log_dir == Path('/custom_base_dir/logs').resolve()
    assert config.history_dir == Path('/custom_base_dir/history').resolve()

def test_file_properties():

    clear_env_vars('CALCULATOR_HISTORY_FILE', 'CALCULATOR_LOG_FILE')
    config = CalculatorConfig(root_dir=Path('/custom_base_dir'))
    assert config.history_file == Path('/custom_base_dir/history/calculator_history.csv').resolve()
    assert config.log_file == Path('/custom_base_dir/logs/calculator.log').resolve()

def test_invalid_max_history_size():

    with pytest.raises(ConfigurationError, match="Max history must be greater than 0"):
        config = CalculatorConfig(max_history=-1)
        config.validate()

def test_invalid_precision():

    with pytest.raises(ConfigurationError, match="Precision must be greater than 0"):
        config = CalculatorConfig(precision=-1)
        config.validate()

def test_invalid_max_input_value():
    
    with pytest.raises(ConfigurationError, match="Max input value must be greater than 0"):
        config = CalculatorConfig(max_input_val=Decimal("-1"))
        config.validate()

def test_auto_save_env_var_true():

    os.environ['CALCULATOR_AUTO_SAVE'] = 'true'
    config = CalculatorConfig(auto_save=None)
    assert config.auto_save is True

def test_auto_save_env_var_one():

    os.environ['CALCULATOR_AUTO_SAVE'] = '1'
    config = CalculatorConfig(auto_save=None)
    assert config.auto_save is True

def test_auto_save_env_var_false():

    os.environ['CALCULATOR_AUTO_SAVE'] = 'false'
    config = CalculatorConfig(auto_save=None)
    assert config.auto_save is False

def test_auto_save_env_var_zero():

    os.environ['CALCULATOR_AUTO_SAVE'] = '0'
    config = CalculatorConfig(auto_save=None)
    assert config.auto_save is False

def test_environment_overrides():

    config = CalculatorConfig()
    assert config.max_history == 1000
    assert config.auto_save is False
    assert config.precision == 8
    assert config.max_input_val == Decimal("1000")
    assert config.default_encoding == 'utf-16'

def test_default_fallbacks():

    clear_env_vars(
        'CALCULATOR_MAX_HISTORY', 'CALCULATOR_AUTO_SAVE', 'CALCULATOR_PRECISION',
        'CALCULATOR_MAX_INPUT_VAL', 'CALCULATOR_DEFAULT_ENCODING'
    )
    config = CalculatorConfig()
    assert config.max_history == 1000
    assert config.auto_save is True
    assert config.precision == 10
    assert config.max_input_val == Decimal("1e999")
    assert config.default_encoding == 'utf-8'

def test_get_project_root():

    from app.calculator_config import get_root
    assert (get_root() / "app").exists()

def test_log_dir_property():

    clear_env_vars('CALCULATOR_LOG_DIR')
    config = CalculatorConfig(root_dir=Path('/new_base_dir'))
    assert config.log_dir == Path('/new_base_dir/logs').resolve()

def test_history_dir_property():

    clear_env_vars('CALCULATOR_HISTORY_DIR')
    config = CalculatorConfig(root_dir=Path('/new_base_dir'))
    assert config.history_dir == Path('/new_base_dir/history').resolve()

def test_log_file_property():

    clear_env_vars('CALCULATOR_LOG_FILE')
    config = CalculatorConfig(root_dir=Path('/new_base_dir'))
    assert config.log_file == Path('/new_base_dir/logs/calculator.log').resolve()

def test_history_file_property():

    clear_env_vars('CALCULATOR_HISTORY_FILE')
    config = CalculatorConfig(root_dir=Path('/new_base_dir'))
    assert config.history_file == Path('/new_base_dir/history/calculator_history.csv').resolve()


def test_history_file_resolve_failure(monkeypatch):
    def broken_resolve(self):
        raise RuntimeError("Simulated resolve failure")

    monkeypatch.setenv('CALCULATOR_HISTORY_FILE', '/fake/path.csv')
    monkeypatch.setattr(Path, "resolve", broken_resolve)

    config = CalculatorConfig(root_dir = Path('/new_base_dir'))

    with pytest.raises(ValueError, match="Invalid CALCULATOR_HISTORY_FILE path: /fake/path.csv"):
        _ = config.history_file
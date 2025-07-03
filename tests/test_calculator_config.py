## test_calculator_config.py
## IS 601 Midterm
## Evan Garvey

## since the logger tests cover a large percentage of the config class, we will be testing the remaining edge cases

from numbers import Number
from pathlib import Path
from typing import Optional
from app.calculator_config import CalculatorConfig


class MockConfig(CalculatorConfig):

    def __init__(self):

        super.__init__()

    def test_history_path(self):

        assert self.history_dir.exists()

    def test_history_file(self):

        assert self.history_file.exists()

    def test_log_path(self):

        assert self.log_dir.exists()

    def test_log_file(self):

        assert self.log_file.exists()
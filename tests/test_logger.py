## test_logger.py
## IS 601 Midterm
## Evan Garvey

from unittest.mock import patch
import pytest

from app.calculator_config import CalculatorConfig
from app.logger import CalculationLogger


class MockLogger(CalculationLogger):

    def __init__(self):
    
        self.config = CalculatorConfig()
        self.log_file = self.config.log_file

        self.info_messages = []
        self.warning_messages = []
        self.error_messages = []

        super().__init__()

    def log_info(self, message: str) -> None:

        self.info_messages.append(message)

    def log_warning(self, message: str) -> None:

        self.warning_messages.append(message)

    def log_error(self, message: str) -> None:

        self.error_messages.append(message)

    def _log(self, level: int, message: str) -> None:

        super()._log(level, message)
    
class TestMockLogger:

    def setup_method(self):

        self.logger = MockLogger()

    def test_setup_success(self):

        self.logger.setup_logging()
        assert self.logger.log_file

    def test_setup_no_log_file(self):

        with patch('app.logger.CalculatorConfig') as MockConfig:

            MockConfig.return_value.log_file = None
            with pytest.raises(Exception, match = "No log file specified in config"):

                self.logger.setup_logging()

    def test_log_init_failure(self):

        side_effects = [Exception("Mock logging failure"), None]

        with patch("logging.basicConfig", side_effect = side_effects):

            with pytest.raises(Exception, match = "Could not initialize logger:"):

                self.logger.setup_logging()
    
    def test_arbitrary_log(self):

        try:

            self.logger._log(20, "Test info message")
            self.logger._log(30, "Test warning message")
            self.logger._log(40, "Test error message")
            
        except Exception:

            pytest.fail("Unexpected exception raised by _log")
## logger.py
## IS 601 Midterm
## Evan Garvey

from abc import ABC, abstractmethod
import logging
from app.calculator_config import CalculatorConfig


class CalculatorLogger(ABC):

    ## abstract class for a logger

    def log_info(self, message: str) -> None:

        self._log(logging.INFO, message)

    def log_warning(self, message: str) -> None:

        self._log(logging.WARNING, message)

    def log_error(self, message: str) -> None:

        self._log(logging.ERROR, message)

    @abstractmethod
    def _log(self, level: int, message: str) -> None:

        pass

class CalculationLogger(CalculatorLogger):

    def __init__(self) -> None:

        config = CalculatorConfig()
        self.log_file = config.log_file
        logging.basicConfig(filename=self.log_file, filemode='w', level=logging.INFO)

    def _log(self, level: int, message: str) -> None:

        logging.log(level, message)
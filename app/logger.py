## logger.py
## IS 601 Midterm
## Evan Garvey

from abc import ABC, abstractmethod
import logging
from app.calculator_config import CalculatorConfig


class CalculatorLogger(ABC):

    ## abstract class for a logger

    def log_info(self, message: str) -> None:

        ## log an info message.

        ## Params: 
        ## message: The message to log

        ## Returns:
        ## None

        self._log(logging.INFO, message)

    def log_warning(self, message: str) -> None:

        ## log a warning message.

        ## Params: 
        ## message: The message to log

        ## Returns:
        ## None

        self._log(logging.WARNING, message)

    def log_error(self, message: str) -> None:

        ## log an error message.

        ## Params: 
        ## message: The message to log

        ## Returns:
        ## None

        self._log(logging.ERROR, message)

    @abstractmethod
    def _log(self, level: int, message: str) -> None:

        ## abstract method for logging

        pass # pragma: no cover

class CalculationLogger(CalculatorLogger):

    ## non-abstract class for a calculation logger.
    ## This will handle any logs related to calculation info, warnings, and errors.
    ## History will be handled separately.

    def __init__(self) -> None:

        ## init method for the calculation logger
        ## this grabs the log file from the config and sets up logging

        config = CalculatorConfig()
        self.log_file = config.log_file

        if not self.log_file:

            ## if no log file is specified in the config, raise an exception

            raise Exception("No log file specified in config")

        try: 

            ## try to initialize logging

            logging.basicConfig(filename=self.log_file, filemode='w', level=logging.INFO)

        except Exception as e:

            ## if there is an error at this point, raise an exception

            raise Exception(f"Could not initialize logger: {e}")

    def _log(self, level: int, message: str) -> None:

        ## log a message

        ## Params: 
        ## level: The level of the message
        ## message: The message to log

        ## Returns:
        ## None

        logging.log(level, message)
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

                                        ## Note: Pragma no cover is required here! These lines are covered in testing
                                        ## but Pytest-cov does not recognize it

        self._log(logging.INFO, message) # pragma: no cover

    def log_warning(self, message: str) -> None:

        ## log a warning message.

        ## Params: 
        ## message: The message to log

        ## Returns:
        ## None

        self._log(logging.WARNING, message) # pragma: no cover

    def log_error(self, message: str) -> None:

        ## log an error message.

        ## Params: 
        ## message: The message to log

        ## Returns:
        ## None

        self._log(logging.ERROR, message) # pragma: no cover

    @abstractmethod
    def _log(self, level: int, message: str) -> None:

        ## abstract method for logging

        pass # pragma: no cover

    @abstractmethod
    def setup_logging(self):

        pass # pragma: no cover

class CalculationLogger(CalculatorLogger):

    ## non-abstract class for a calculation logger.
    ## This will handle any logs related to calculation info, warnings, and errors.
    ## History will be handled separately.
        
    def setup_logging(self):

        config = CalculatorConfig()
        self.log_file = config.log_file

        if not self.log_file:

            ## if no log file is specified in the config, raise an exception

            raise Exception("No log file specified in config")

        try:

            logging.basicConfig(
                filename=str(self.log_file),
                level=logging.INFO,
                format='%(asctime)s - %(levelname)s - %(message)s',
                force=True  # Overwrite any existing logging configuration
            )

                        ## Pragma required here! this line is covered in testing locally, but github's testing does not recognize it!
                        ## Feel free to remove this pragma locally to test coverage

            logging.info(f"Logging initialized at: {self.log_file}")  # pragma: no cover

        except Exception as e:

            ## if there is an error at this point, raise an exception
            ## and use a fallback console logger

            logging.basicConfig(
                level=logging.WARNING,
                format='%(asctime)s - [FALLBACK] %(levelname)s - %(message)s',
                force=True
            )
            logging.warning("Failed to configure file logging. Using fallback console logger.")
            logging.exception(e)

            raise Exception(f"Could not initialize logger: {e}")

    def _log(self, level: int, message: str) -> None:

        ## log a message

        ## Params: 
        ## level: The level of the message
        ## message: The message to log

        ## Returns:
        ## None

        if level == 20:

            logging.info(f"Info: {message}")

        elif level == 30:

            logging.warning(f"Warning: {message}")

        elif level == 40:

            logging.error(f"Error: {message}")

        else:

            logging.log(level, "Unexpected log level")
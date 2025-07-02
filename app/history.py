## history.py
## IS 601 Midterm
## Evan Garvey



from abc import ABC, abstractmethod
import logging
from typing import Any

from app.calculation import Calculation
from app.logger import CalculationLogger


class HistoryObserver(ABC):

    ## Abstract class for calculator observers

    @abstractmethod
    def update(self, calculation: Calculation) -> None:

        ## Abstract method for updating the history with a new calculation
        
        pass # pragma: no cover

class LoggingObserver(HistoryObserver):

    ## Non-abstract class for logging calculations

    def __init__(self, logger: CalculationLogger):

        ## Initializes the LoggingObserver

        ## Params:
        ## Logger: The logger object

        ## Returns:
        ## None

        self.logger = logger

    def update_calculation(self, calculation: Calculation) -> None:

        ## Logs the calculation to the console

        ## Params:
        ## Calculation: The calculation to log

        ## Returns:
        ## None

        if calculation is None:

            self.logger.log_error("Calculation cannot be None")
            raise AttributeError
        
        self.logger.log_info(calculation)

    def update_message(self, level: int, message: str) -> None:

        if level == 20:

            self.logger.log_info(message)

        elif level == 30:

            self.logger.log_warning(message)

        elif level == 40:

            self.logger.log_error(message)

        else:

            self.logger.log_error(f"Invalid level: {level}")

class AutoSaveObserver(HistoryObserver):

    ## Non-abstract class for saving calculations
    
    def __init__(self, logger: CalculationLogger, calculator: Any):

        ## Initializes the AutoSaveObserver

        ## Params:
        ## Calculator: The calculator object

        ## Returns:
        ## None
        logger = CalculationLogger()

        if not hasattr(calculator, 'config') or not hasattr(calculator, 'save_history'):

            ## Check if the calculator has a config and save_history method

            logger.log_error("Calculator must have a config and save_history method")
            raise TypeError
        
        self.calculator = calculator

    def update(self, calculation: Calculation) -> None:

        ## Saves the calculation to a file
        ## This will be automatically triggered as the calculator is used

        ## Params:
        ## Calculation: The calculation to save

        ## Returns:
        ## None

        if calculation is None:

            self.logger.log_error(f"Calculation cannot be None")
            raise AttributeError
        
        if self.calculator.config.auto_save:

            self.calculator.save_history()

            self.logger.log_info(f"History saved: {calculation}")
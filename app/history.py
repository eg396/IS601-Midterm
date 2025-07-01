## history.py
## IS 601 Midterm
## Evan Garvey



from abc import ABC, abstractmethod
from typing import Any

from app.calculation import Calculation


class HistoryObserver(ABC):

    ## Abstract class for calculator observers

    @abstractmethod
    def update(self, calculation: Calculation) -> None:

        ## Abstract method for updating the history with a new calculation
        
        pass # pragma: no cover

class LoggingObserver(HistoryObserver):

    ## Non-abstract class for logging calculations

    def update(self, calculation: Calculation) -> None:

        ## Logs the calculation to the console

        ## Params:
        ## Calculation: The calculation to log

        ## Returns:
        ## None

        if calculation is None:

            raise AttributeError("Calculation cannot be None")
        
        pass ## TODO: logging. Output the proper result

def AutoSaveObserver(HistoryObserver):

    ## Non-abstract class for saving calculations

    def __init__(self, calculator: Any):

        ## Initializes the AutoSaveObserver

        ## Params:
        ## Calculator: The calculator object

        ## Returns:
        ## None

        if not hasattr(calculator, 'config') or not hasattr(calculator, 'save_history'):

            ## Check if the calculator has a config and save_history method

            raise TypeError("Calculator must have a config and save_history method")
        
        self.calculator = calculator

    def update(self, calculation: Calculation) -> None:

        ## Saves the calculation to a file
        ## This will be automatically triggered as the calculator is used

        ## Params:
        ## Calculation: The calculation to save

        ## Returns:
        ## None

        if calculation is None:

            raise AttributeError("Calculation cannot be None")
        
        if self.calculator.config.auto_save:

            self.calculator.save_history()

            pass ## TODO: logging. report the history is auto saved
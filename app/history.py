## history.py
## IS 601 Midterm
## Evan Garvey



from abc import ABC, abstractmethod
import logging
from typing import Any
import pandas as pd

from app.calculation import Calculation
from app.logger import CalculationLogger


class HistoryObserver(ABC):

    ## Abstract class for calculator observers

    @abstractmethod
    def update(self, calculation: Calculation) -> None:

        ## Abstract method for updating the log with a new calculation. Non optional
        
        pass # pragma: no cover

    def update_message(self, level: int, message: str) -> None:

        ## Optionally overrideable method for updating the log with a new message
        
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

    def update(self, calculation: Calculation) -> None:

        ## Logs the calculation to the console

        ## Params:
        ## Calculation: The calculation to log

        ## Returns:
        ## None

        if calculation is None:

            self.logger.log_error(f"Calculation cannot be None")
            raise AttributeError
        
        self.logger.log_info(
            f"History updated: {calculation.operation},"
            f"{calculation.num1}, {calculation.num2} ="
            f"{calculation.result}"
        )

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

    def __init__(self, csv_path: str):

         self.csv_path = csv_path
         self.df = pd.DataFrame(columns=["operation", "num1", "num2", "result", "timestamp"])

    def update(self, calculation: Calculation) -> None:

        ## Saves the calculation to a file
        ## This will be automatically triggered as the calculator is used

        ## Params:
        ## Calculation: The calculation to save

        ## Returns:
        ## None

        if calculation is None:

            ## This doesn't need to be logged as it will run in parallel with the other observer, which will log

            raise AttributeError("Calculation cannot be None")

        ## Append the calculation to the dataframe

        new_row = pd.DataFrame([{
            "operation": calculation.operation,
            "num1": calculation.num1,
            "num2": calculation.num2,
            "result": calculation.result,
            "timestamp": calculation.timestamp
        }])

        self.df = pd.concat([self.df, new_row], ignore_index=True)

        ## Save the dataframe to the file

        self.df.to_csv(self.csv_path, index=False)
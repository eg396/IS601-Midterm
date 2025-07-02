## calculator.py
## IS 601 Midterm
## Evan Garvey

from decimal import Decimal
import os
from pathlib import Path
from typing import List, Optional, Union

from app.calculation import Calculation
from app.calculator_config import CalculatorConfig
from app.calculator_memento import CalculatorMemento
from app.history import HistoryObserver, LoggingObserver
from app.logger import CalculationLogger
from app.operations import Operation

## Definining type aliases that we will be using often

Number = Union[int, float, Decimal]
CalculationResult = Union[Number, str]

class Calculator:

    ## Calculator class which will be the heart of our applicaiton
    ## It will effectively communicate with any needed files as well as provide a REPL interface

    def __init__(self, config: Optional[CalculatorConfig] = None):

        ## initialize calculator using the configuration options provided

        ## Params:
        ## config: CalculatorConfig

        ## Returns:
        ## None

        if config is None:

            ## if no config provided, find the project root directory

            current_file = Path(__file__)
            project_root = current_file.parent.parent
            config = CalculatorConfig(base_dir = project_root)

        ## initialize the config and validate

        self.config = config
        self.config.validate()

        os.makedirs(self.config.log_dir, exist_ok = True)

        self._setup_logging()  

        self.history = List[Calculation] = []
        self.operation_strategy: Optional[Operation] = None

        self.observers = List[HistoryObserver] = []

        self.undo_stack = List[CalculatorMemento] = []
        self.redo_stack = List[CalculatorMemento] = []

        self._setup_directories()

        try:

            self.load_history()

        except Exception as e:

            print(f"Error loading history: {e}")

        def _setup_logging(self):

            try:

                os.makedirs(self.config.log_dir, exist_ok = True)
                log_file = self.config.log_file.resolve()

                logger = LoggingObserver(CalculationLogger())
                logger.update_message(20, f"Logging initialized at: {log_file}")

                self.observers.append(logger)

            except Exception as e:

                print(f"Error setting up logging: {e}")
                raise
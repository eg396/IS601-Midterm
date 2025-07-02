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
from app.exceptions import OperationError, ValidationError
from app.history import HistoryObserver, LoggingObserver
from app.input_validators import InputValidator
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

            ## Update logging observer with error

            self._send_message(40, f"Error loading history: {e}")

        self._send_message(20, f"Calculator initialized at: {self.config.root_dir}")

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

    def _send_message(self, level: int, message: str) -> None:

        for i in self.observers:

            i.update_message(level, message)

    def _send_calculation(self, calculation: Calculation) -> None:

        for i in self.observers:

            i.update(calculation)

    def _setup_directories(self) -> None:

        self.config.history_dir.mkdir(parents = True, exist_ok = True)

    def add_observer(self, observer: HistoryObserver) -> None:

        self.observers.append(observer)
        self._send_message(20, f"Added observer: {observer.__class__.__name__}")

    def remove_observer(self, observer: HistoryObserver) -> None:

        self.observers.remove(observer)
        self._send_message(20, f"Removed observer: {observer.__class__.__name__}")

    def notify_observers(self, calculation: Calculation) -> None:

        self._send_calculation(calculation)

    def set_operation(self, operation: Operation) -> None:

        self.operation_strategy = operation
        self._send_message(20, f"Operation set to: {operation}")

    def perform_calculation(self, str1: Union[str, Number], str2: Union[str, Number]) -> CalculationResult:

        if self.operation_strategy is None:

            raise OperationError("No operation set")
            
        try:

            validated_str1 = InputValidator.validate_input(str1, self.config)
            validated_str2 = InputValidator.validate_input(str2, self.config)

            result = self.operation_strategy.execute(validated_str1, validated_str2)

            calculation = Calculation(
                operation = str(self.operation_strategy),
                num1 = validated_str1,
                num2 = validated_str2,
            )

            self.undo_stack.append(CalculatorMemento(self.history.copy()))

            self.redo_stack.clear()

            self.history.append(calculation)

            if len(self.history) > self.config.max_history:

                self.history.pop(0)

            self.notify_observers(calculation)

            return result
            
        except ValidationError as e:

            self._send_message(40, f"Validation Error: {e}")

        except Exception as e:

            self._send_message(40, f"Operation Failed: {e}")

    
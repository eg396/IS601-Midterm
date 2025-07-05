## calculator.py
## IS 601 Midterm
## Evan Garvey

from decimal import Decimal
import os
from pathlib import Path
import sys
from typing import List, Optional, Union
import pandas as pd

from app.calculation import Calculation
from app.calculator_config import CalculatorConfig
from app.calculator_memento import CalculatorMemento
from app.exceptions import OperationError, ValidationError
from app.history import HistoryObserver, LoggingObserver
from app.input_validators import InputValidator
from app.logger import CalculationLogger
from app.operations import Operation, OperationFactory

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

        ## Initialize the observers first

        self.observers: List[HistoryObserver] = []

        if config is None:

            ## if no config provided, find the project root directory

            current_file = Path(__file__)
            project_root = current_file.parent.parent
            config = CalculatorConfig(root_dir = project_root)

        ## initialize the config and validate

        self.config = config
        self.config.validate()

        os.makedirs(self.config.log_dir, exist_ok = True)

        self._setup_logging()

        self.history: List[Calculation] = []
        self.operation_strategy: Optional[Operation] = None

        self.undo_stack: List[CalculatorMemento] = []
        self.redo_stack: List[CalculatorMemento] = []

        self._setup_directories()

        try:

            self.load_history()

        except Exception as e:

            ## Update logging observer with error

            self._send_message(40, f"Error loading history: {e}")
            raise e

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

    def perform_operation(self, str1: Union[str, Number], str2: Union[str, Number]) -> CalculationResult:

        if self.operation_strategy is None:

            raise OperationError("No operation set")
            
        try:

            validated_str1 = InputValidator.validate_input(str1, self.config)
            validated_str2 = InputValidator.validate_input(str2, self.config)

            result = self.operation_strategy.execute(validated_str1, validated_str2)

            operation_name = None

            calculation = Calculation(
                operation = self.operation_strategy.name,
                num1 = validated_str1,
                num2 = validated_str2
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
            raise

        except Exception as e:

            self._send_message(40, f"Operation Failed: {e}")
            raise

    def save_history(self) -> None:

        try:

            self.config.history_dir.mkdir(parents = True, exist_ok = True)

            history_data = []

            for calc in self.history:

                history_data.append({
                    'operation': str(calc.operation),
                    'num1': str(calc.num1),
                    'num2': str(calc.num2),
                    'result': str(calc.result),
                    'timestamp': calc.timestamp.isoformat()
                })

            if history_data:

                df = pd.DataFrame(history_data)
                df.to_csv(self.config.history_file, index = False)

                self._send_message(20, f"History saved to: {self.config.history_file}")

            else:

                pd.DataFrame(columns = [
                    'operation', 'num1', 'num2', 'result', 'timestamp'
                    ]).to_csv(self.config.history_file, index = False)
                self._send_message(20, f"Empty history saved to: {self.config.history_file}")

        except Exception as e:

            self._send_message(40, f"Error saving history: {e}")
            raise OperationError(f"Error saving history: {e}")
        
    def load_history(self) -> None:

        try:

            if self.config.history_file.exists():

                df = pd.read_csv(self.config.history_file)
                if not df.empty:

                    self.history = [
                        Calculation.from_dict({
                            'operation': row['operation'],
                            'num1': row['num1'],
                            'num2': row['num2'],
                            'result': row['result'],
                            'timestamp': row['timestamp']
                        })
                        for _, row in df.iterrows()
                    ]

                    self._send_message(20, f"Loaded {len(self.history)} calculations from history file")

                else:

                    self._send_message(20, f"Loaded empty history file")

            else:

                self._send_message(20, f"No history file found - starting with empty history")

        except Exception as e:

            self._send_message(40, f"Error loading history: {e}")
            raise OperationError(f"Error loading history: {e}")
        
    def get_history_dataframe(self) -> pd.DataFrame:

        history_data = []
        for calc in self.history:

            history_data.append({
                'operation': str(calc.operation),
                'num1': str(calc.num1),
                'num2': str(calc.num2),
                'result': str(calc.result),
                'timestamp': calc.timestamp
            })

        return pd.DataFrame(history_data)
    
    def show_history(self) -> List[str]:

        return [ 
            f"{calc.operation} ({calc.num1} {calc.num2}) = {calc.result}" for calc in self.history
        ]
    
    def clear_history(self) -> None:

        self.history.clear()
        self.redo_stack.clear()
        self.undo_stack.clear()
        self._send_message(20, f"History cleared")

    def undo(self) -> bool:

        if not self.undo_stack:

            return False
        
        memento = self.undo_stack.pop()
        self.redo_stack.append(CalculatorMemento(self.history.copy()))
        self.history = memento.history.copy()
        
        return True
    
    def redo(self) -> bool:

        if not self.redo_stack:

            return False
        
        memento = self.redo_stack.pop()
        self.undo_stack.append(CalculatorMemento(self.history.copy()))
        self.history = memento.history.copy()
        
        return True
    

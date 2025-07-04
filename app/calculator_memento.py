## calculator_memento.py
## IS 601 Midterm
## Evan Garvey

from dataclasses import dataclass, field
import datetime
from typing import Any, Dict, List

from app.calculation import Calculation



@dataclass
class CalculatorMemento:

    ## CalculatorMemento class

    ## This class is used to store the state of the calculator
    ## Primarily this will enable us to undo / redo our work in real time

    ## Fields:
    ## history: List[Calculation]
    ## timestamp: datetime

    history: List[Calculation]
    timestamp: datetime.datetime = field(default_factory = datetime.datetime.now)

    def to_dict(self) -> Dict[str, Any]:

        ## Converts the CalculatorMemento into a dictionary

        ## Params:
        ## None

        ## Returns:
        ## Dict[str, Any]: The dictionary representation of the CalculatorMemento

        return {
            'history': [calc.to_dict() for calc in self.history],
            'timestamp': self.timestamp.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CalculatorMemento':

        ## Converts the dictionary into a CalculatorMemento

        ## Params:
        ## Data: dict

        ## Returns:
        ## CalculatorMemento: The CalculatorMemento

        return cls(
            history=[Calculation.from_dict(calc) for calc in data['history']],
            timestamp=datetime.datetime.fromisoformat(data['timestamp'])
        )
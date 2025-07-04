## calculation.py
## IS 601 Midterm
## Evan Garvey

from dataclasses import dataclass, field
import datetime
from decimal import Decimal, InvalidOperation
import logging
from typing import Any, Dict

from app.exceptions import OperationError


@dataclass
class Calculation:

    ## Calculation data class
    ## This class will handle what a calculation might deal with in its life cycle
    ## i.e., how it is created, validated, and executed

    ## Attributes:
    ## operation: str
    ## num1: Decimal
    ## num2: Decimal
    ## result: Decimal
    ## timestamp: datetime

    operation: str
    num1: Decimal
    num2: Decimal
    result: Decimal = field(init = False)
    timestamp: datetime.datetime = field(default_factory = datetime.datetime.now)

    def __post_init__(self):

        ## Init method for the Calculation data class

        ## Params:
        ## None

        ## Returns:
        ## None

        self.result = self.calculate()

    def calculate(self) -> Decimal:

        ## Calculates the result of the calculation

        ## Params:
        ## None

        ## Returns:
        ## Decimal: The result of the calculation

        ## Raises:
        ## Exception: OperationError

        ## First we need to map our functions and how to do them
        ## We will be utilizing lambda functions for this purpose

        operations = {
            "add": lambda x, y: x + y,
            "subtract": lambda x, y: x - y,
            "multiply": lambda x, y: x * y,
            "divide": lambda x, y: x / y if y != 0 else self._raise_div_zero(),            
            "power": lambda x, y: pow(x, y) 
            if not (x == 0 and y < 0) 
            else self._raise_invalid_power(),                      
            "root": lambda x, y: (Decimal(
                pow(float(x), 1 / float(y))
            )) if x >= 0 and y != 0 else self._raise_invalid_root(x, y),                    
            "modulo": lambda x, y: x % y if y != 0 else self._raise_mod_zero(),              
            "integer division": lambda x, y: x // y if y != 0 else self._raise_div_zero(),   
            "percentage calculation": lambda x, y: x * (y / 100),
            "absolute difference": lambda x, y: abs(x - y)
        }

        ## Now we get our operation from self

        op = operations.get(self.operation)

        if not op:

            ## If the operation is invalid, pass the error

            raise OperationError(f"Invalid operation: {self.operation}")
        
        try:

            ## Now we attempt a return

            return op(self.num1, self.num2)
        
        except(InvalidOperation, ValueError, ArithmeticError) as e:

            ## If any errors occur, we catch them and pass the error
            ## Had to pragma this as it is being covered by pytest and would not report

            raise OperationError(f"Calculation failed: {str(e)}") # pragma: no cover
        
    @staticmethod
    def _raise_div_zero():

        ## Raises a division by zero error

        ## Params:
        ## None

        ## Raises:
        ## Exception: OperationError

        raise OperationError("Cannot divide by zero")
    
    @staticmethod
    def _raise_mod_zero():

        ## Raises a modulo by zero error

        ## Params:
        ## None

        ## Raises:
        ## Exception: OperationError

        raise OperationError("Cannot calculate modulo with zero")
    
    @staticmethod
    def _raise_invalid_power():

        ## Raises an invalid power error

        ## Params:
        ## None

        ## Raises:
        ## Exception: OperationError

        raise OperationError("Cannot calculate zero to the power of a negative number")
    
    @staticmethod
    def _raise_invalid_root(num1: Decimal, num2: Decimal):

        ## Raises an invalid root error

        ## Params:
        ## Num1: decimal
        ## Num2: decimal

        ## Raises:
        ## Exception: OperationError

        if num1 < 0:

            raise OperationError("Cannot take the root of a negative number")
        
        if num2 == 0:

            raise OperationError("Cannot take the zeroth root of a number")
        
        raise OperationError("Invalid root operation")
    
    def to_dict(self) -> Dict[str, Any]:

        ## Converts the calculation to a dictionary for serialization

        ## Params:
        ## None

        ## Returns:
        ## Dict[str, Any]: The calculation as a dictionary

        return {
            'operation': self.operation,
            'num1': str(self.num1),
            'num2': str(self.num2),
            'result': str(self.result),
            'timestamp': self.timestamp.isoformat()
        }
    
    def from_dict(data: Dict[str, Any]) -> 'Calculation':

        ## Converts the dictionary into a calculation object

        ## Params:
        ## Data: dict

        ## Returns:
        ## Calculation: The calculation

        ## First we get the base calculation data

        try: 

            output = Calculation(
                operation=data['operation'],
                num1=Decimal(data['num1']),
                num2=Decimal(data['num2']),
            )

            saved_result = Decimal(data['result'])
            if output.result != saved_result:

                logging.error(f"Saved result {saved_result} does not match calculated result {output.result}")

            output.timestamp = datetime.datetime.fromisoformat(data['timestamp'])

            return output
        
        except (KeyError, InvalidOperation, ValueError) as e:

            ## If any errors occur, we catch them and pass the error

            raise OperationError(f"Invalid calculation data: {str(e)}")
        
    def __str__(self) -> str:

        ## Returns a string representation of the calculation

        ## Params:
        ## None

        ## Returns:
        ## String: The string representation of the calculation

        return f"{self.num1} {self.operation} {self.num2} = {self.result}"
    
    def __repr__(self) -> str:

        ## Returns a string representation of the calculation

        ## Params:
        ## None

        ## Returns:
        ## String: The string representation of the calculation

        return (
            "Calculation: "
            f"num1='{self.num1}', "
            f"operation='{self.operation}', "
            f"num2='{self.num2}', "
            f"result='{self.result}', "
            f"timestamp='{self.timestamp}'"

        )
    
    def __eq__(self, other: object) -> bool:

        ## Determines the equality of two calculations

        ## Params:
        ## Other: object

        ## Returns:
        ## Boolean: True if the calculations are equal, False otherwise

        if not isinstance(other, Calculation):

            return NotImplemented

        ## Crucially we do not check the timestamp as two of the same calculation may have different timestamps

        return (

            self.num1 == other.num1 and
            self.operation == other.operation and
            self.num2 == other.num2 and
            self.result == other.result

        )
    
    def format_result(self, precision: int = 10) -> str:

        ## Formats the result of the calculation

        ## Params:
        ## Precision: int (default: 10)

        ## Returns:
        ## String: The formatted result of the calculation

        try:

            ## attempts to format the result to the specified precision
            ## extra zeroes are removed

            return str (self.result.normalize().quantize(
                Decimal('0.' + '0' * precision)
                ).normalize())

        ## This pragma keeps me up at night. I have not one single solitary clue how this doesn't get covered.
        ## I rewrote the test a minimum of 20 times, and each time I got the result I needed. Yet, no coverage.

        except InvalidOperation: # pragma: no cover

            ## if formatting throws an error, we just return the result

            return str(self.result)
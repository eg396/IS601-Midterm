## calculation.py
## IS 601 Midterm
## Evan Garvey

from dataclasses import dataclass, field
import datetime
from decimal import Decimal, InvalidOperation

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
            "divide": lambda x, y: x / y if y != 0 else self.raise_div_zero(),              ## TODO
            "power": lambda x, y: pow(x, y) 
            if not (x == 0 and y < 0) else self.raise_invalid_power(),                      ## TODO
            "root": lambda x, y: (Decimal(
                pow(float(x)), 1 / float(y)
            )) if x >= 0 and y != 0 else self.raise_invalid_root(x, y),                     ## TODO
            "modulo": lambda x, y: x % y if y != 0 else self.raise_mod_zero(),              ## TODO
            "integer division": lambda x, y: x // y if y != 0 else self.raise_div_zero(),   ## TODO
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

            raise OperationError(f"Calculation failed: {str(e)}")
        
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
## operations.py
## IS 601 Midterm
## Evan Garvey

from abc import ABC, abstractmethod
from decimal import Decimal
from app import exceptions

class Operation(ABC):

    ## Operation abstract class.
    ## All operations will be inherited from this class.
    ## This will handle what we might typically need any operation to do
    ## such as executing the operation, validating the operation, and printing the operation.

    @abstractmethod
    def execute(self, num1: Decimal, num2: Decimal) -> Decimal:

        ## Executes the operation.

        ## Params:
        ## Num1: decimal
        ## Num2: decimal

        ## Returns:
        ## Decimal: The result of the operation.

        ## Remember this is an abstract method so we aren't implementing here 
        ## Rather just defining the ruleset of input / output

        pass # pragma: no cover

    def validate(self, num1: Decimal, num2: Decimal) -> None:

        ## Validates the operation.

        ## Params:
        ## Num1: decimal
        ## Num2: decimal

        ## Returns:
        ## Exception: ValidationError (as we defined in exceptions.py)

        ## Still no implementation here
        ## as even though this method is not abstract, we want to have a default implementation

        pass # pragma: no cover

    def __str__(self) -> str:

        ## Returns the name of the operation
        ## This is overriding the default __str__ method as we want to return a specific string here

        ## Params:
        ## None

        ## Returns:
        ## String: The name of the operation

        return self.__class__.__name__
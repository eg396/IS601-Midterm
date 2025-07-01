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
    
## We now implement each of the operations we wish to support as subclasses of Operation
## add, subtract, multiply, divide, Power, Root, Modulo, Integer Division, Percentage Calculation, Absolute Difference

class Addition(Operation):

    ## Addition class
    ## For adding two numbers

    def execute(self, num1: Decimal, num2: Decimal) -> Decimal:
        
        ## Executes the addition operation

        ## Params:
        ## Num1: decimal
        ## Num2: decimal

        ## Returns:
        ## Decimal: The result of the addition operation

        self.validate(num1, num2)
        return num1 + num2
    
class Subtraction(Operation):

    ## Subtraction class
    ## For subtracting two numbers

    def execute(self, num1: Decimal, num2: Decimal) -> Decimal:
        
        ## Executes the subtraction operation

        ## Params:
        ## Num1: decimal
        ## Num2: decimal

        ## Returns:
        ## Decimal: The result of the subtraction operation

        self.validate(num1, num2)
        return num1 - num2
    

class Multiplication(Operation):

    ## Multiplication class
    ## For multiplying two numbers

    def execute(self, num1: Decimal, num2: Decimal) -> Decimal:
        
        ## Executes the multiplication operation

        ## Params:
        ## Num1: decimal
        ## Num2: decimal

        ## Returns:
        ## Decimal: The result of the multiplication operation

        self.validate(num1, num2)
        return num1 * num2
    
class Division(Operation):

    ## Division class
    ## For dividing two numbers

    def validate(self, num1: Decimal, num2: Decimal) -> None:
        
        ## Validates the division operation (i.e. is the divisor 0?)

        ## Params:
        ## Num1: decimal
        ## Num2: decimal

        ## Returns:
        ## Exception: ValidationError (as we defined in exceptions.py)

        ## Note: we call super().validate because we want to future proof our code
        ## for all future validate methods, we will follow this pattern

        super().validate(num1, num2)
        if num2 == 0:
            raise exceptions.CalculationError("Cannot divide by zero")
        
    def execute(self, num1: Decimal, num2: Decimal) -> Decimal:
        
        ## Executes the division operation

        ## Params:
        ## Num1: decimal
        ## Num2: decimal

        ## Returns:
        ## Decimal: The result of the division operation

        self.validate(num1, num2)
        return num1 / num2
    
class Power(Operation):

    ## Power class
    ## For raising one number to the power of another

    def validate(self, num1: Decimal, num2: Decimal) -> None:
        
        ## Validates the power operation (i.e. is the exponent negative?)

        ## Params:
        ## Num1: decimal
        ## Num2: decimal

        ## Returns:
        ## Exception: ValidationError (as we defined in exceptions.py)

        super().validate(num1, num2)
        if num2 < 0:
            raise exceptions.CalculationError("Cannot raise to a negative power")

    def execute(self, num1: Decimal, num2: Decimal) -> Decimal:
        
        ## Executes the power operation

        ## Params:
        ## Num1: decimal
        ## Num2: decimal

        ## Returns:
        ## Decimal: The result of the power operation

        self.validate(num1, num2)
        return num1 ** num2
    
class Root(Operation):

    ## Root class
    ## For finding the nth root of a number

    def validate(self, num1: Decimal, num2: Decimal) -> None:
        
        ## Validates the root operation (i.e. is the number being rooted negative?)

        ## Params:
        ## Num1: decimal
        ## Num2: decimal

        ## Returns:
        ## Exception: ValidationError (as we defined in exceptions.py)

        super().validate(num1, num2)
        if num1 < 0:
            raise exceptions.CalculationError("Cannot take the nth root of a negative number")
        
    def execute(self, num1: Decimal, num2: Decimal) -> Decimal:
        
        ## Executes the root operation

        ## Params:
        ## Num1: decimal
        ## Num2: decimal

        ## Returns:
        ## Decimal: The result of the root operation

        self.validate(num1, num2)
        return num1 ** (1 / num2)
    
class Modulo(Operation):

    ## Modulo class
    ## For finding the remainder of two numbers

    def validate(self, num1: Decimal, num2: Decimal) -> None:
        
        ## Validates the modulo operation (i.e. is the divisor 0?)

        ## Params:
        ## Num1: decimal
        ## Num2: decimal

        ## Returns:
        ## Exception: ValidationError (as we defined in exceptions.py)

        super().validate(num1, num2)
        if num2 == 0:
            raise exceptions.CalculationError("Cannot divide by zero")

    def execute(self, num1: Decimal, num2: Decimal) -> Decimal:
        
        ## Executes the modulo operation

        ## Params:
        ## Num1: decimal
        ## Num2: decimal

        ## Returns:
        ## Decimal: The result of the modulo operation

        self.validate(num1, num2)
        return num1 % num2
    
class IntegerDivision(Operation):

    ## IntegerDivision class
    ## For finding the integer division of two numbers

    def validate(self, num1: Decimal, num2: Decimal) -> None:
        
        ## Validates the integer division operation (i.e. is the divisor 0?)

        ## Params:
        ## Num1: decimal
        ## Num2: decimal

        ## Returns:
        ## Exception: ValidationError (as we defined in exceptions.py)

        super().validate(num1, num2)
        if num2 == 0:
            raise exceptions.CalculationError("Cannot divide by zero")

    def execute(self, num1: Decimal, num2: Decimal) -> Decimal:
        
        ## Executes the integer division operation

        ## Params:
        ## Num1: decimal
        ## Num2: decimal

        ## Returns:
        ## Decimal: The result of the integer division operation

        self.validate(num1, num2)
        return num1 // num2
    
class PercentageCalculation(Operation):

    ## PercentageCalculation class
    ## For finding the percentage of one number with respect to another

    def validate(self, num1: Decimal, num2: Decimal) -> None:
        
        ## Validates the percentage calculation (i.e. is the divisor 0?)

        ## Params:
        ## Num1: decimal
        ## Num2: decimal

        ## Returns:
        ## Exception: ValidationError (as we defined in exceptions.py)

        super().validate(num1, num2)
        if num2 == 0:
            raise exceptions.CalculationError("Cannot divide by zero")

    def execute(self, num1: Decimal, num2: Decimal) -> Decimal:
        
        ## Executes the percentage calculation

        ## Params:
        ## Num1: decimal
        ## Num2: decimal

        ## Returns:
        ## Decimal: The result of the percentage calculation

        self.validate(num1, num2)
        return num1 * (num2 / 100)
    
class AbsoluteDifference(Operation):

    ## AbsoluteDifference class
    ## For finding the absolute difference of two numbers

    ## No special validation required here!

    def execute(self, num1: Decimal, num2: Decimal) -> Decimal:
        
        ## Executes the absolute difference operation

        ## Params:
        ## Num1: decimal
        ## Num2: decimal

        ## Returns:
        ## Decimal: The result of the absolute difference operation

        self.validate(num1, num2)
        return abs(num1 - num2)
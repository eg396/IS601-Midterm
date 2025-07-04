## input_validators.py
## IS 601 Midterm
## Evan Garvey

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from typing import Any
from app.calculator_config import CalculatorConfig
from app.exceptions import ValidationError

@dataclass
class InputValidator:

    ## InputValidator class
    ## contains static methods for validating user input

    @staticmethod
    def validate_input(value: Any, config: CalculatorConfig) -> Decimal:

        ## Validate the input and convert it to Decimal

        ## Params:
        ## Value: input value
        ## Config: calculator configuration

        ## Returns:
        ## Decimal: The input as a Decimal

        ## Raises: 
        ## Exception: ValidationError

        try:

            ## If the value is a string, remove leading and trailing whitespace

            if isinstance(value, str):

                value = value.strip()

            ## Convert the value to a Decimal

            number = Decimal(str(value))

            ## Check if the value is greater than the maximum allowed value
            ## If so, raise a ValidationError

            if abs(number) > config.max_input_val:

                raise ValidationError(f"Value {number} exceeds maximum allowed value of {config.max_input_val}")
            
            ## Return the normalized number

            return number.normalize()
        
        ## If the operation is not valid, raise a ValidationError
        
        except InvalidOperation as e:

            raise ValidationError(f"Invalid number format: {value}")
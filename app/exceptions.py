## exceptions.py
## IS 601 Midterm
## Evan Garvey

class CalculatorError(Exception):

    ## CalculatorError base class. all other exceptions inherit from this
    ## No implementation for this, or any other, classes from this file.
    ## The purpose of this file is to provide exception templates, not implementations.
    ## The implementations will be handled by the appropriate files

    pass

class ConfigurationError(CalculatorError):

    ## ConfigurationError exception class. For when the config is off this is thrown
    ## Only raised when the config settings are incorrect / invalid.

    pass

class ValidationError(CalculatorError):

    ## ValidationError exception class. For when the user's input cannot be validated
    ## Only raised during user input handling.

    pass

class CalculationError(CalculatorError):

    ## CalculationError exception class. For when the calculation cannot be completed
    ## Only raised during calculation.

    pass
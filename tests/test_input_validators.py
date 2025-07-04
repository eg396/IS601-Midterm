import pytest
from decimal import Decimal
from app.calculator_config import CalculatorConfig
from app.exceptions import ValidationError
from app.input_validators import InputValidator

config = CalculatorConfig()
config.max_input_val = 1000000

def test_validate_input_positive_integer():
    assert InputValidator.validate_input(123, config) == Decimal('123')

def test_validate_input_positive_decimal():
    assert InputValidator.validate_input(123.456, config) == Decimal('123.456').normalize()

def test_validate_input_positive_string_integer():
    assert InputValidator.validate_input("123", config) == Decimal('123')

def test_validate_input_positive_string_decimal():
    assert InputValidator.validate_input("123.456", config) == Decimal('123.456').normalize()

def test_validate_input_negative_integer():
    assert InputValidator.validate_input(-789, config) == Decimal('-789')

def test_validate_input_negative_decimal():
    assert InputValidator.validate_input(-789.123, config) == Decimal('-789.123').normalize()

def test_validate_input_negative_string_integer():
    assert InputValidator.validate_input("-789", config) == Decimal('-789')

def test_validate_input_negative_string_decimal():
    assert InputValidator.validate_input("-789.123", config) == Decimal('-789.123').normalize()

def test_validate_input_zero():
    assert InputValidator.validate_input(0, config) == Decimal('0')

def test_validate_input_trimmed_string():
    assert InputValidator.validate_input("  456  ", config) == Decimal('456')

# Negative test cases
def test_validate_input_invalid_string():
    with pytest.raises(ValidationError, match="Invalid number format: abc"):
        InputValidator.validate_input("abc", config)

def test_validate_input_exceeds_max_value():
    with pytest.raises(ValidationError, match="Value 1000001 exceeds maximum allowed value of 1000000"):
        InputValidator.validate_input(Decimal('1000001'), config)

def test_validate_input_exceeds_max_value_string():
    with pytest.raises(ValidationError, match="Value 1000001 exceeds maximum allowed value of 1000000"):
        InputValidator.validate_input("1000001", config)

def test_validate_input_exceeds_negative_max_value():
    with pytest.raises(ValidationError, match="Value -1000001 exceeds maximum allowed value of 1000000"):
        InputValidator.validate_input(-Decimal('1000001'), config)

def test_validate_input_empty_string():
    with pytest.raises(ValidationError, match="Invalid number format: "):
        InputValidator.validate_input("", config)

def test_validate_input_whitespace_string():
    with pytest.raises(ValidationError, match="Invalid number format: "):
        InputValidator.validate_input("   ", config)

def test_validate_input_none_value():
    with pytest.raises(ValidationError, match="Invalid number format: None"):
        InputValidator.validate_input(None, config)

def test_validate_input_non_numeric_type():
    with pytest.raises(ValidationError, match="Invalid number format: "):
        InputValidator.validate_input([], config)
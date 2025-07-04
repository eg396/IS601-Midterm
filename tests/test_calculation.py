from unittest.mock import Mock, patch
import pytest
from decimal import Decimal, InvalidOperation
from datetime import datetime
from app.calculation import Calculation
from app.exceptions import OperationError
import logging


def test_addition():
    
    calc = Calculation(operation="add", num1=Decimal("2"), num2=Decimal("3"))
    assert calc.result == Decimal("5")


def test_subtraction():

    calc = Calculation(operation="subtract", num1=Decimal("5"), num2=Decimal("3"))
    assert calc.result == Decimal("2")


def test_multiplication():

    calc = Calculation(operation="multiply", num1=Decimal("4"), num2=Decimal("2"))
    assert calc.result == Decimal("8")


def test_division():

    calc = Calculation(operation="divide", num1=Decimal("8"), num2=Decimal("2"))
    assert calc.result == Decimal("4")


def test_division_by_zero():

    with pytest.raises(OperationError, match="Cannot divide by zero"):

        Calculation(operation="divide", num1=Decimal("8"), num2=Decimal("0"))


def test_power():

    calc = Calculation(operation="power", num1=Decimal("2"), num2=Decimal("3"))
    assert calc.result == Decimal("8")


def test_negative_power():

    with pytest.raises(OperationError, match="Cannot calculate zero to the power of a negative number"):

        Calculation(operation="power", num1=Decimal("0"), num2=Decimal("-3"))


def test_root():

    calc = Calculation(operation="root", num1=Decimal("16"), num2=Decimal("2"))
    assert calc.result == Decimal("4")


def test_invalid_root():

    with pytest.raises(OperationError, match="Cannot take the root of a negative number"):

        Calculation(operation="root", num1=Decimal("-16"), num2=Decimal("2"))

def test_invalid_root_zero():

    with pytest.raises(OperationError, match="Cannot take the zeroth root of a number"):

        Calculation(operation="root", num1=Decimal("16"), num2=Decimal("0"))

def test_raise_invalid_root_generic():

    with pytest.raises(OperationError, match="Invalid root operation"):

        Calculation._raise_invalid_root(Decimal("4"), Decimal("2"))

def test_modulo():

    calc = Calculation(operation="modulo", num1=Decimal("5"), num2=Decimal("3"))
    assert calc.result == Decimal("2")

def test_modulo_by_zero():

    with pytest.raises(OperationError, match="Cannot calculate modulo with zero"):

        Calculation(operation="modulo", num1=Decimal("5"), num2=Decimal("0"))


def test_unknown_operation():
    with pytest.raises(OperationError, match="Invalid operation: Unknown"):

        Calculation(operation="Unknown", num1=Decimal("5"), num2=Decimal("3"))


def test_to_dict():

    calc = Calculation(operation="add", num1=Decimal("2"), num2=Decimal("3"))
    result_dict = calc.to_dict()
    assert result_dict == {
        "operation": "add",
        "num1": "2",
        "num2": "3",
        "result": "5",
        "timestamp": calc.timestamp.isoformat()
    }


def test_from_dict():

    data = {
        "operation": "add",
        "num1": "2",
        "num2": "3",
        "result": "5",
        "timestamp": datetime.now().isoformat()
    }

    calc = Calculation.from_dict(data)
    assert calc.operation == "add"
    assert calc.num1 == Decimal("2")
    assert calc.num2 == Decimal("3")
    assert calc.result == Decimal("5")


def test_invalid_from_dict():

    data = {
        "operation": "add",
        "num1": "invalid",
        "num2": "3",
        "result": "5",
        "timestamp": datetime.now().isoformat()
    }

    with pytest.raises(OperationError, match="Invalid calculation data"):

        Calculation.from_dict(data)


def test_format_result():
    calc = Calculation(operation="divide", num1=Decimal("1"), num2=Decimal("3"))
    assert calc.format_result(precision=2) == "0.33"
    assert calc.format_result(precision=10) == "0.3333333333"


def test_equality():
    calc1 = Calculation(operation="add", num1=Decimal("2"), num2=Decimal("3"))
    calc2 = Calculation(operation="add", num1=Decimal("2"), num2=Decimal("3"))
    calc3 = Calculation(operation="subtract", num1=Decimal("5"), num2=Decimal("3"))
    assert calc1 == calc2
    assert calc1 != calc3

def test_calculation_eq_not_implemented():
    calc = Calculation(operation="add", num1=Decimal("2"), num2=Decimal("3"))
    result = Calculation.__eq__(calc, "not a calculation")
    assert result is NotImplemented

import pytest
from decimal import Decimal, InvalidOperation
from app.calculation import Calculation

def test_format_result_handles_invalid_operation():

    calc = Calculation(operation="add", num1=Decimal("1"), num2=Decimal("2"))
    calc.result = Decimal('NaN')
    output = calc.format_result(precision=10)
    assert output == 'NaN'

def test_format_result_handles_invalid_operation():
    calc = Calculation(operation="add", num1=Decimal("1"), num2=Decimal("2"))
    calc.result = Decimal('NaN')
    formatted = calc.format_result()
    assert formatted == 'NaN'

def test_from_dict_result_mismatch(caplog):

    data = {
        "operation": "add",
        "num1": "2",
        "num2": "3",
        "result": "10",
        "timestamp": datetime.now().isoformat()
    }

    with caplog.at_level(logging.WARNING):

        calc = Calculation.from_dict(data)

    assert "Saved result 10 does not match calculated result 5" in caplog.text


def test_calculate_generic_exception_handling(monkeypatch):

    calc = Calculation(operation="add", num1=Decimal("1"), num2=Decimal("2"))

    def raise_value_error(x, y):

        raise ValueError("forced error")

    def fake_calculate(self):

        operations = {

            "add": raise_value_error,

        }

        op = operations.get(self.operation)
        if not op:

            raise OperationError(f"Invalid operation: {self.operation}")
        
        try:

            return op(self.num1, self.num2)
        
        except (InvalidOperation, ValueError, ArithmeticError) as e:

            raise OperationError(f"Calculation failed: {str(e)}")

    monkeypatch.setattr(calc, "calculate", fake_calculate.__get__(calc))

    with pytest.raises(OperationError) as excinfo:

        calc.calculate()

    assert "Calculation failed: forced error" in str(excinfo.value)

def test_str():

    calc = Calculation(operation="add", num1=Decimal("2"), num2=Decimal("3"))
    assert str(calc) == "2 add 3 = 5"

def test_repr():

    calc = Calculation(operation="add", num1=Decimal("2"), num2=Decimal("3"))
    rep = repr(calc)

    # Check the static parts exist
    assert "Calculation: " in rep
    assert "operation='add'" in rep
    assert "num1='2'" in rep
    assert "num2='3'" in rep
    assert "result='5'" in rep
    assert "timestamp=" in rep
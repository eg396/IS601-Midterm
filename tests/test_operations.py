## test_operations.py
## IS 601 Midterm
## Evan Garvey

from decimal import Decimal
import gc
from typing import Any, Dict, Type
from app.exceptions import ValidationError
import pytest

from app.operations import (
    Operation,
    Addition,
    OperationFactory,
    Subtraction,
    Multiplication,
    Division,
    Power,
    Root,
    Modulo,
    IntegerDivision,
    PercentageCalculation,
    AbsoluteDifference
)

class MockOperation:

    def test_str_representation(self):

        class TestOp(Operation):

            def execute(self, num1: Decimal, num2: Decimal) -> Decimal:

                return num1
            
        assert str(TestOp()) == "TestOp"

class BaseOperationTest:

    operation_class = Type[Operation]
    valid_test_cases = Dict[str, Dict[str, Any]]
    invalid_test_cases = Dict[str, Dict[str, Any]]

    def test_valid_operations(self):

        operation = self.operation_class()
        for name, case in self.valid_test_cases.items():

            num1 = Decimal(str(case["num1"]))
            num2 = Decimal(str(case["num2"]))
            expected = Decimal(str(case["expected"]))
            result = operation.execute(num1, num2)
            assert result == expected, f"failed test case: {name}"

    def test_invalid_operations(self):

        operation = self.operation_class()
        for name, case in self.invalid_test_cases.items():

            num1 = Decimal(str(case["num1"]))
            num2 = Decimal(str(case["num2"]))
            error = case.get("error", ValidationError)
            error_message = case.get("message", "")

            with pytest.raises(error, match = error_message):

                operation.execute(num1, num2)

class TestAddition(BaseOperationTest):

    operation_class = Addition
    valid_test_cases = {
        "positive_nums": {"num1": "1", "num2": "2", "expected": "3"},
        "negative_nums": {"num1": "-1", "num2": "-2", "expected": "-3"},
        "zero": {"num1": "0", "num2": "0", "expected": "0"},
        "mixed_signs": {"num1": "1", "num2": "-2", "expected": "-1"},
        "decimals": {"num1": "1.5", "num2": "2.5", "expected": "4.0"},
        "large_nums": {"num1": "123456789", "num2": "987654321", "expected": "1111111110"},
    }

    invalid_test_cases = {}

class TestSubtraction(BaseOperationTest):

    operation_class = Subtraction
    valid_test_cases = {
        "positive_nums": {"num1": "1", "num2": "2", "expected": "-1"},
        "negative_nums": {"num1": "-1", "num2": "-2", "expected": "1"},
        "zero": {"num1": "0", "num2": "2", "expected": "-2"},
        "mixed_signs": {"num1": "1", "num2": "-2", "expected": "3"},
        "decimals": {"num1": "1.5", "num2": "2.5", "expected": "-1.0"},
        "large_nums": {"num1": "123456789", "num2": "987654321", "expected": "-864197532"},
    }

    invalid_test_cases = {}

class TestMultiplication(BaseOperationTest):

    operation_class = Multiplication
    valid_test_cases = {
        "positive_nums": {"num1": "1", "num2": "2", "expected": "2"},
        "negative_nums": {"num1": "-1", "num2": "-2", "expected": "2"},
        "zero": {"num1": "0", "num2": "5", "expected": "0"},
        "mixed_signs": {"num1": "1", "num2": "-2", "expected": "-2"},
        "decimals": {"num1": "1.5", "num2": "2.5", "expected": "3.75"},
        "large_nums": {"num1": "12345", "num2": "98765", "expected": "1219253925"},
    }

    invalid_test_cases = {}

class TestDivision(BaseOperationTest):

    operation_class = Division
    valid_test_cases= {
        "positive_nums": {"num1": "1", "num2": "2", "expected": "0.5"},
        "negative_nums": {"num1": "-1", "num2": "-2", "expected": "0.5"},
        "zero": {"num1": "0", "num2": "5", "expected": "0"},
        "mixed_signs": {"num1": "1", "num2": "-2", "expected": "-0.5"},
        "decimals": {"num1": "1.5", "num2": "2.5", "expected": "0.6"},
        "large_nums": {"num1": "123456789", "num2": "987654321", "expected": "0.1249999988609375000142382812"},
    }

    invalid_test_cases = {
        "divide_by_zero": {"num1": "1", "num2": "0", "error": ValidationError, "message": "Cannot divide by zero"},
    }

class TestPower(BaseOperationTest):

    operation_class = Power
    valid_test_cases = {
        "positive_nums": {"num1": "1", "num2": "2", "expected": "1"},
        "negative_nums": {"num1": "-1", "num2": "-2", "expected": "1"},
        "zero": {"num1": "0", "num2": "5", "expected": "0"},
        "mixed_signs": {"num1": "1", "num2": "-2", "expected": "1"},
        "decimals": {"num1": "1.5", "num2": "2.5", "expected": "2.755675960631075360471944584"},
        "large_nums": {"num1": "12345", "num2": "98765", "expected": "1.311974440088693590037902201E+404096"},
    }

    invalid_test_cases = {
        "raise_zero_to_negative_power": {"num1": "0", "num2": "-2", "error": ValidationError, "message": "Cannot raise zero to a negative power"},
    }

class TestRoot(BaseOperationTest):

    operation_class = Root
    valid_test_cases = {
        "positive_nums": {"num1": "1", "num2": "2", "expected": "1.00000000000000000000000000"},
        "mixed_signs": {"num1": "81", "num2": "-2", "expected": "0.1111111111111111111111111111"},
        "decimals": {"num1": "1.5", "num2": "2.5", "expected": "1.176079022524673572584977814"},
        "large_nums": {"num1": "12345", "num2": "98765", "expected": "1.000095392656731133701466809"},
    }

    invalid_test_cases = {
        "first_num_zero_or_less": {"num1": "0", "num2": "2", "error": ValidationError, "message": "Cannot take the root of a number less than or equal to zero"},
        "second_num_zero": {"num1": "1", "num2": "0", "error": ValidationError, "message": "Cannot take the zeroth root of a number"},
    }

class TestModulo(BaseOperationTest):

    operation_class = Modulo
    valid_test_cases = {
        "positive_nums": {"num1": "1", "num2": "2", "expected": "1"},
        "negative_nums": {"num1": "-1", "num2": "-2", "expected": "-1"},
        "zero": {"num1": "0", "num2": "5", "expected": "0"},
        "mixed_signs": {"num1": "1", "num2": "-2", "expected": "1"},
        "decimals": {"num1": "1.5", "num2": "2.5", "expected": "1.5"},
        "large_nums": {"num1": "12345", "num2": "98765", "expected": "12345"},
    }

    invalid_test_cases = {
        "divide_by_zero": {"num1": "1", "num2": "0", "error": ValidationError, "message": "Cannot divide by zero"},
    }

class TestIntegerDivision(BaseOperationTest):

    operation_class = IntegerDivision
    valid_test_cases = {
        "positive_nums": {"num1": "1", "num2": "2", "expected": "0"},
        "negative_nums": {"num1": "-1", "num2": "-2", "expected": "0"},
        "zero": {"num1": "0", "num2": "5", "expected": "0"},
        "mixed_signs": {"num1": "1", "num2": "-2", "expected": "0"},
        "decimals": {"num1": "1.5", "num2": "2.5", "expected": "0"},
        "large_nums": {"num1": "12345", "num2": "98765", "expected": "0"},
    }

    invalid_test_cases = {
        "divide_by_zero": {"num1": "1", "num2": "0", "error": ValidationError, "message": "Cannot divide by zero"},
    }

class TestPercentageCalculation(BaseOperationTest):

    operation_class = PercentageCalculation
    valid_test_cases = {
        "positive_nums": {"num1": "1", "num2": "2", "expected": "50"},
        "negative_nums": {"num1": "-1", "num2": "-2", "expected": "50"},
        "zero": {"num1": "0", "num2": "5", "expected": "0"},
        "mixed_signs": {"num1": "1", "num2": "-2", "expected": "-50"},
        "decimals": {"num1": "1.5", "num2": "2.5", "expected": "60"},
        "large_nums": {"num1": "12500", "num2": "100000", "expected": "12.5"},
    }

    invalid_test_cases = {
        "divide_by_zero": {"num1": "1", "num2": "0", "error": ValidationError, "message": "Cannot divide by zero"},
    }

class TestAbsoluteDifference(BaseOperationTest):

    operation_class = AbsoluteDifference
    valid_test_cases = {
        "positive_nums": {"num1": "1", "num2": "2", "expected": "1"},
        "negative_nums": {"num1": "-1", "num2": "-2", "expected": "1"},
        "zero": {"num1": "0", "num2": "5", "expected": "5"},
        "mixed_signs": {"num1": "1", "num2": "-2", "expected": "3"},
        "decimals": {"num1": "1.5", "num2": "2.5", "expected": "1"},
        "large_nums": {"num1": "12345", "num2": "98765", "expected": "86420"},
    }

    invalid_test_cases = {}

class TestMockOperation:

    def test_str(self):

        class TestOp(Operation):

            def execute(self, num1: Decimal, num2: Decimal) -> Decimal:

                return num1
            
        assert str(TestOp()) == "TestOp"

    def test_name(self):

        class TestOp(Operation):

            def execute(self, num1: Decimal, num2: Decimal) -> Decimal:

                return num1
            
        assert TestOp().name == "testop"

class TestOperationFactory:

    def test_create_valid_operations(self):

        operation_map = {
            "add": Addition,
            "subtract": Subtraction,
            "multiply": Multiplication,
            "divide": Division,
            "power": Power,
            "root": Root,
            "modulo": Modulo,
            "integer division": IntegerDivision,
            "percentage calculation": PercentageCalculation,
            "absolute difference": AbsoluteDifference
        }

        for op_name, op_class in operation_map.items():
            operation = OperationFactory.create(op_name)
            assert isinstance(operation, op_class)

    def test_create_invalid_operation(self):

        with pytest.raises(ValueError, match = "Invalid operation type: invalid_operation"):
            OperationFactory.create("invalid_operation")

    def test_register_valid_operation(self):

        class TestOp(Operation):

            def execute(self, num1: Decimal, num2: Decimal) -> Decimal:

                return num1
            
        OperationFactory.register("test_op", TestOp)
        operation = OperationFactory.create("test_op")
        assert isinstance(operation, TestOp)

    def test_register_invalid_operation(self):

        with pytest.raises(TypeError, match = "Registering operation class is not a subclass of Operation"):

            class TestOp:

                pass

            OperationFactory.register("invalid_operation", TestOp)

    def test_names(self):

        test_factory = OperationFactory()

        for op_name, op_class in test_factory._operations.items():
            if op_name != "test_op":
                assert op_name == op_class().name 
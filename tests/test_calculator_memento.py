## test_calculator_memento.py
## IS 601 Midterm
## Evan Garvey

import datetime
print(datetime)
print(dir(datetime))
print(hasattr(datetime.datetime, 'fromisoformat'))
from unittest.mock import Mock

from app.calculation import Calculation
from app.calculator_memento import CalculatorMemento


def test_calculator_memento_to_dict():
    # Mock Calculation instances with to_dict method
    calc1 = Mock(spec=Calculation)
    calc1.to_dict.return_value = {'operation': 'add', 'num1': 1, 'num2': 2, 'result': 3}
    calc2 = Mock(spec=Calculation)
    calc2.to_dict.return_value = {'operation': 'multiply', 'num1': 3, 'num2': 4, 'result': 12}

    timestamp = datetime.datetime(2024, 7, 4, 12, 0, 0)
    memento = CalculatorMemento(history=[calc1, calc2], timestamp=timestamp)

    result = memento.to_dict()

    # Check history list converted correctly
    assert result['history'] == [
        {'operation': 'add', 'num1': 1, 'num2': 2, 'result': 3},
        {'operation': 'multiply', 'num1': 3, 'num2': 4, 'result': 12}
    ]

    # Check timestamp is ISO formatted string
    assert result['timestamp'] == timestamp.isoformat()

    # Also verify to_dict was called on each Calculation instance
    calc1.to_dict.assert_called_once()
    calc2.to_dict.assert_called_once()

def test_calculator_memento_from_dict(monkeypatch):
    data = {
        'history': [
            {'operation': 'add', 'num1': 1, 'num2': 2, 'result': 3},
            {'operation': 'multiply', 'num1': 3, 'num2': 4, 'result': 12}
        ],
        'timestamp': '2024-07-04T12:00:00'
    }

    calc1 = Mock(spec=Calculation)
    calc2 = Mock(spec=Calculation)
    called_args = []

    def fake_from_dict(calc_dict):

        ## Mock Calculation.from_dict

        called_args.append(calc_dict)
        return calc1 if calc_dict['operation'] == 'add' else calc2
    
    ## Monkeypatch Calculation.from_dict

    monkeypatch.setattr(Calculation, "from_dict", fake_from_dict)
    memento = CalculatorMemento.from_dict(data)

    assert called_args == data['history']
    assert memento.history == [calc1, calc2]
    assert memento.timestamp == datetime.datetime.fromisoformat(data['timestamp'])
## Python Calculator

This is a midterm project for IS 601. It is an enhanced calculator application meant to be used through the terminal.

## Features

- Use the terminal to use an REPL-loop based calculator application.
- The calculator accepts single-word phrases, such as an operation or commands to save history, undo, or redo.
- Actively saved data using pandas, and actively logged info / calculation errors using logger.
- Add, subtract, multiply divide, modulo, and other advanced algebraic operations.
- Unit tests to ensure 100% test coverage, with GitHub action configuration already included.

## Installation

- Download this repository onto your local device.
- Download Python 3.12, or whatever version is the newest available to you.
- Run the command line "pip install -r requirements.txt".
- Begin a python venv, by typing "python3 -m venv venv" and then "source venv/bin/activate".
- Run the program by typing "python3 -m main"
- Enjoy the calculator!


## Configuration

The config file is available at .env. WARNING: Changing these values might lead to broken tests, but will not break the calculator itself! It is important to note that you do not need to change or set these values yourself - although, if you do want to tinker with the configuration of this calculator, the config options are as following:
- CALCULATOR_ROOT_DIR = The calculator root directory. Leave this be - it is automatically defined and heavily influences the function of the calculator.
- CALCULATOR_MAX_HISTORY = The maximum number of logged calculations the calculator can remember at a time.
- CALCULATOR_AUTO_SAVE = Whether or not the calculator will automatically save your history.
- CALCULATOR_PRECISION = The number of decimals you want your numbers to be rounded to.
- CALCULATOR_MAX_INPUT_VAL = The maximum value you wish to be allowed by the calculator.
- CALCULATOR_DEFAULT_ENCODING = The encoding of the calculator. Example = utf-8
- CALCULATOR_LOG_DIR = The directory in which the calculator will store its log file.
- CALCULATOR_LOG_FILE = The file name in which the calculator will store its logs.
- CALCULATOR_HISTORY_DIR = The directory in which the calculator will store its history file.
- CALCULATOR_HISTORY_FILE = The directory in which the calculator will store its history.

## Usage

There are a number of arguments to run using this calculator:
- add, subtract, multiply, divide, power, root, modulo, int_divide, percent, abs_diff: Perform calculations.
- history: Show history.
- clear: Clear history.
- undo: Undo last calculation.
- redo: Redo last calculation.
- save: Save history to file.
- load: Load history from file.
- help: Show available commands.
- exit: Exit program.

## Testing Instructions

To test, while the venv is activated (see 'Installation' for instructions), type the command line "python3 -m pytest". You will recieve a comprehensive menu of the number of tests run, the results of said tests, and the % coverage of each file that the tests cover.

## GitHub CI/CD Actions

Actions are already implemented into Git - They automatically check for test coverage, and each individual check occurs when a local instance of the code is pushed to this repository. Check out the results on the "Actions" tab!

## TODO

- Implement arithmetic calculations [Done]
- History management with undo & redo [Done]
- Observer pattern for logging & auto-saving [Done]
- Configuration management [50% Done]
- Error handling & input validation 
- Logging [Done]
- Command line REPL interface [Done]
- Unit testing
- Serialization & data persistence [Done]
- GitHub actions for CI/CD
- Documentation

## Optional TODO

- Dynamic help menu using Decorator Design Pattern
- Color-Coded outputs
- Additional Design Patterns
## calculator_config.py
## IS 601 Midterm
## Evan Garvey

from dataclasses import dataclass
from decimal import Decimal
from numbers import Number
import os
from pathlib import Path
from typing import Optional
from app.exceptions import ConfigurationError
from dotenv import load_dotenv

## Before we start we must load the dotenv

load_dotenv()

def get_root() -> Path:

    ## Gets the project root directory

    ## Params:
    ## None

    ## Returns:
    ## Path: The project root directory

    ## Note:
    ## In the output we go '.parent.parent' as we are in root/app/calculator_config.py
    ## And we desire to be in root, not app

    current_file = Path(__file__)
    return current_file.parent.parent

@dataclass
class CalculatorConfig:

    ## Calculator configuration settings class
    ## We are handling data, therefore a dataclass is appropriate here

    def __init__(
            self,
            root_dir: Optional[Path] = None,
            max_history: Optional[int] = None,
            auto_save: Optional[bool] = None,
            precision: Optional[int] = None,
            max_input_val: Optional[Number] = None,
            default_encoding: Optional[str] = None
    ):
        
        ## Initialize the config values
        ## Optional is used here as sometimes, these configs may be 'None'
        ## Number is also used here as we might recieve an int or a float so we need something flexible

        ## Args:
        ## root_dir: Optional[Path] = our root directory
        ## max_history: Optional[int] = the maximum calculation history we want to hold
        ## auto_save: Optional[bool] = whether we want to auto save
        ## precision: Optional[int] = how precise we want to be with our results
        ## max_input_val: Optional[Number] = the maximum input value
        ## default_encoding: Optional[str] = our default encoding
        ## All args default to none.

        ## Outputs:
        ## None

        ## First we must locate our root path. this is where our .env file is
        ## All params will be dealt with this way - sticking to None or getting our value from the .env

        project_root = get_root()
        self.root_dir = root_dir or Path(
            os.getenv('CALCULATOR_ROOT_DIR', str(project_root))
        )

        ## Max history

        self.max_history = max_history or Path(
            os.getenv('CALCULATOR_MAX_HISTORY', '1000')
        )

        ## Auto save
        ## This one is different than the last one as we have to do 2 things:
        ## 1. get the value from the .env and evaluate it
        ## 2. do an if statement to check if it's valid

        auto_save_env = os.getenv('CALCULATOR_AUTO_SAVE', 'true').lower()
        self.auto_save = auto_save if auto_save is not None else (
            auto_save_env == 'true' or auto_save_env == '1'
            )

        ## Precision

        self.precision = precision or int(
            os.getenv('CALCULATOR_PRECISION', '10')
        )

        ## Max input value

        self.max_input_val = max_input_val or Decimal(
            os.getenv('CALCULATOR_MAX_INPUT_VAL', '1e999')
        )

        ## Default encoding

        self.default_encoding = default_encoding or os.getenv(
            'CALCULATOR_DEFAULT_ENCODING', 'utf-8'
        )

    @property
    def log_dir(self) -> Path:
        
        ## Get the log directory path
        ## We are using @property as we want this method to act like an attribute
        ## This strategy will be used for the rest of the dir and file methods

        ## Params:
        ## None

        ## Returns:
        ## Path: The log directory path

        ## This patch of code gets our log dir with the fallback being our root dir / 'logs'
        ## The resulting path is then resolved to an absolute path
        ## This strategy will be used for the rest of the attribute methods

        return Path(os.getenv(

            'CALCULATOR_LOG_DIR',
            str(self.root_dir / 'logs')

        )).resolve()
    
    @property
    def log_file(self) -> Path:
        
        ## Get the log file path

        ## Params:
        ## None

        ## Returns:
        ## Path: The log file path

        return Path(os.getenv(
            'CALCULATOR_LOG_FILE',
            str(self.log_dir / 'calculator.log')
        )).resolve()
    
    @property
    def history_dir(self) -> Path:
        
        ## Get the history directory path

        ## Params:
        ## None

        ## Returns:
        ## Path: The history directory path

        return Path(os.getenv(
            'CALCULATOR_HISTORY_DIR',
            str(self.root_dir / 'history')
        )).resolve()

    @property
    def history_file(self) -> Path:
        
        ## Get the history file path

        ## Params:
        ## None

        ## Returns:
        ## Path: The history file path

        return Path(os.getenv(
            'CALCULATOR_HISTORY_FILE',
            str(self.history_dir / 'calculator_history.csv')
        )).resolve()
    
    def validate(self) -> None:
        
        ## Validate the config settings

        ## Params:
        ## None

        ## Returns:
        ## None

        ## Raises:
        ## Exception: ConfigurationError

        if self.max_history <= 0:

            raise ConfigurationError("Max history must be greater than 0")

        if self.precision <= 0:

            raise ConfigurationError("Precision must be greater than 0")

        if self.max_input_val <= 0:

            raise ConfigurationError("Max input value must be greater than 0")
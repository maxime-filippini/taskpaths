"""
    This module holds various derived classes that define commonly used
    I/O steps involved in processes
"""
import json
from dataclasses import dataclass
from typing import Any
from typing import Callable
from typing import List
from typing import Optional

from taskpaths.process import Step


class ReadTextFileStep(Step):
    def instruction(self, file_path: str):
        with open(file_path) as f:
            out = f.readlines()
        return out


@dataclass
class ReadJsonFileStep(Step):
    parse_float: Optional[Callable[[str], Any]] = None

    def instruction(self, file_path: str):
        with open(file_path) as f:
            out = json.load(f, parse_float=self.parse_float)
        return out

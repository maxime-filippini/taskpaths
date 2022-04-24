"""
    This module holds various derived classes that define commonly used
    I/O steps involved in processes
"""
import json
from dataclasses import dataclass
from typing import Any

from taskpaths.process import Step


@dataclass
class StoreAsJsonStep(Step):
    indent: int = 4
    sort_keys: bool = True

    def instruction(self, content: Any, out_path: str):
        with open(out_path, "w") as f:
            json.dump(content, f, indent=self.indent, sort_keys=self.sort_keys)

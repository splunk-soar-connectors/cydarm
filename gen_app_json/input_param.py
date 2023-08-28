import dataclasses
from typing import List


@dataclasses.dataclass
class InputParam:
    name: str
    description: str
    order: int = 0
    data_type: str = "string"
    required: bool = False
    primary: bool = False
    contains: List = dataclasses.field(default_factory=list)
    value_list: List = dataclasses.field(default_factory=list)
    default: str = ""

    def as_output_field(self) -> dict:
        return {
            "data_path": f"action_result.data.*.{self.name}",
            "data_type": self.data_type
        }

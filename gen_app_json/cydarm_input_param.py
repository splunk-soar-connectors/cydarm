# File: cydarm_input_param.py
#
# Copyright (c) 2023-2025 Splunk Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions
# and limitations under the License.
#

import dataclasses


@dataclasses.dataclass
class InputParam:
    name: str
    description: str
    order: int = 0
    data_type: str = "string"
    required: bool = False
    primary: bool = False
    contains: list = dataclasses.field(default_factory=list)
    value_list: list = dataclasses.field(default_factory=list)
    default: str = ""

    def as_output_field(self) -> dict:
        return {"data_path": f"action_result.data.*.{self.name}", "data_type": self.data_type}

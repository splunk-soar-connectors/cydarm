# File: __init__.py
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
from typing import Dict, List, Optional

from gen_app_json.create_case import INPUT_PARAMS_CREATE_CASE
from gen_app_json.cydarm_input_param import InputParam
from gen_app_json.update_case import INPUT_PARAMS_UPDATE_CASE, OUTPUT_CASE_MODEL


@dataclasses.dataclass
class OutputField:
    data_path: str
    data_type: str = "string"


def as_list_of_dicts(output_fields: list[OutputField]) -> list[dict]:
    return [dataclasses.asdict(x) for x in output_fields]


OUTPUT_RANK_MODEL = as_list_of_dicts([OutputField(data_path="action_result.data.*.rank", data_type="numeric")])

OUTPUT_UUID_AND_ACL_MODEL = as_list_of_dicts(
    [
        OutputField(data_path="action_result.data.*.uuid"),
        OutputField(data_path="action_result.data.*.acl"),
    ]
)
OUTPUT_USER_MODEL = as_list_of_dicts(
    [
        OutputField(data_path="action_result.data.*.uuid"),
        OutputField(data_path="action_result.data.*.username"),
        OutputField(data_path="action_result.data.*.email"),
    ]
)
OUTPUT_ACL_OBJECT_MODEL = as_list_of_dicts(
    [
        OutputField(data_path="action_result.data.*.uuid"),
        OutputField(data_path="action_result.data.*.description"),
        OutputField(data_path="action_result.data.*.aci.*.uuid"),
    ]
)
OUTPUT_PLAYBOOK_ACTION_DATA_MODEL = as_list_of_dicts(
    [
        OutputField(data_path="action_result.data.*.atc.uuid"),
        OutputField(data_path="action_result.data.*.atc.name"),
        OutputField(data_path="action_result.data.*.atc.description"),
    ]
)
OUTPUT_ACTION_INSTANCE_DATA_MODEL = as_list_of_dicts(
    [
        OutputField(data_path="action_result.data.*.uuid"),
        OutputField(data_path="action_result.data.*.action_instance_uuid"),
        OutputField(data_path="action_result.data.*.caseuuid"),
    ]
)

OUTPUT_CASE_PLAYBOOK_MODEL = as_list_of_dicts(
    [
        OutputField(data_path="action_result.data.*.casePlaybookUuid"),
        OutputField(data_path="action_result.data.*.caseUuid"),
        OutputField(data_path="action_result.data.*.playbookName"),
        OutputField(data_path="action_result.data.*.playbookDescription"),
        OutputField(data_path="action_result.data.*.action_statuses.*.actionName"),
        OutputField(data_path="action_result.data.*.action_statuses.*.actionInstanceUuid"),
    ]
)
OUTPUT_STATUS_MESSAGE_SUMMARY = as_list_of_dicts(
    [
        OutputField(data_path="action_result.status"),
        OutputField(data_path="action_result.message"),
        OutputField(data_path="summary.total_objects", data_type="numeric"),
        OutputField(data_path="summary.total_objects_successful", data_type="numeric"),
    ]
)

INPUT_PARAMS_CREATE_PLAYBOOK = [
    InputParam(name="name", description="The name of the playbook", required=True),
    InputParam(name="acl", description="The UUID of the ACL of the playbook", required=True),
    InputParam(name="description", description="Playbook description", required=True),
]
INPUT_PARAMS_CREATE_PLAYBOOK_ACTION = [
    InputParam(name="name", description="The name of the action", required=True),
    InputParam(name="acl", description="The UUID of the ACL of the action", required=True),
    InputParam(name="description", description="Action description", required=True),
]

INPUT_PARAMS_ADD_ACTION_TO_PLAYBOOK = [
    InputParam(name="playbook_uuid", description="UUID of playbook.", required=True),
    InputParam(name="action_uuid", description="UUID of action to add.", required=True),
]

INPUT_PARAMS_UPDATE_CASE_HISTORY = [
    InputParam(name="case_uuid", description="Case UUID", required=True),
    InputParam(name="modified", description="The time at which the case was modified. Expected format: ISO-8601.", required=True),
    InputParam(name="status", description="Case's status. Currently only supports value of 'Event'.", required=True),
]


def generate_input_params_dict(params: list[InputParam]) -> dict:
    output = {}
    for index, param in enumerate(params):
        param.order = index
        output[param.name] = dataclasses.asdict(param)
    return output


def generate_action(
    identifier: str,
    description: str,
    parameters: dict,
    output: list,
    action_type="generic",
    read_only=False,
    verbose=None,
    action_name: Optional[str] = None,
):
    # action names must be lower case
    resolved_action_name = action_name or identifier.replace("_", " ").lower()
    result = {
        "action": resolved_action_name,
        "identifier": identifier,
        "description": description,
        "type": action_type,
        "read_only": read_only,
        "parameters": parameters,
        "output": output,
        "render": {"type": "table"},
        "versions": "EQ(*)",
    }
    if verbose is not None:
        result["verbose"] = verbose
    return result

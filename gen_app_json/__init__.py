import dataclasses
from typing import Dict, List

from gen_app_json.input_param import InputParam
from gen_app_json.create_case import INPUT_PARAMS_CREATE_CASE
from gen_app_json.update_case import INPUT_PARAMS_UPDATE_CASE, OUTPUT_CASE_MODEL

@dataclasses.dataclass
class OutputField:
    data_path: str
    data_type: str = "string"


def as_list_of_dicts(output_fields: List[OutputField]) -> List[dict]:
    return [dataclasses.asdict(x) for x in output_fields]


OUTPUT_RANK_MODEL = as_list_of_dicts([
    OutputField(data_path="action_result.data.*.rank", data_type="numeric")
])

OUTPUT_UUID_AND_ACL_MODEL = as_list_of_dicts([
    OutputField(data_path="action_result.data.*.uuid"),
    OutputField(data_path="action_result.data.*.acl"),
])
OUTPUT_USER_MODEL = as_list_of_dicts([
    OutputField(data_path="action_result.data.*.uuid"),
    OutputField(data_path="action_result.data.*.username"),
    OutputField(data_path="action_result.data.*.email"),
])
OUTPUT_ACL_OBJECT_MODEL = as_list_of_dicts([
    OutputField(data_path="action_result.data.*.uuid"),
    OutputField(data_path="action_result.data.*.description"),
    OutputField(data_path="action_result.data.*.aci.*.uuid"),
])
OUTPUT_PLAYBOOK_ACTION_DATA_MODEL = as_list_of_dicts([
    OutputField(data_path="action_result.data.*.atc.uuid"),
    OutputField(data_path="action_result.data.*.atc.name"),
    OutputField(data_path="action_result.data.*.atc.description"),
])
OUTPUT_ACTION_INSTANCE_DATA_MODEL = as_list_of_dicts([
    OutputField(data_path="action_result.data.*.uuid"),
    OutputField(data_path="action_result.data.*.action_instance_uuid"),
    OutputField(data_path="action_result.data.*.caseuuid"),
])

OUTPUT_CASE_PLAYBOOK_MODEL = as_list_of_dicts([
    OutputField(data_path="action_result.data.*.casePlaybookUuid"),
    OutputField(data_path="action_result.data.*.caseUuid"),
    OutputField(data_path="action_result.data.*.playbookName"),
    OutputField(data_path="action_result.data.*.playbookDescription"),
    OutputField(data_path="action_result.data.*.action_statuses.*.actionName"),
    OutputField(data_path="action_result.data.*.action_statuses.*.actionInstanceUuid"),
])
OUTPUT_STATUS_MESSAGE_SUMMARY = as_list_of_dicts([
    OutputField(data_path="action_result.status"),
    OutputField(data_path="action_result.message"),
    OutputField(data_path="summary.total_objects", data_type="numeric"),
    OutputField(data_path="summary.total_objects_successful", data_type="numeric"),

])

INPUT_PARAMS_CREATE_PLAYBOOK = [
    InputParam(name="name",
               description="The name of the playbook",
               required=True),
    InputParam(name="acl",
               description="The UUID of the ACL of the playbook",
               required=True),
    InputParam(name="description",
               description="Playbook description",
               required=True),
]
INPUT_PARAMS_CREATE_PLAYBOOK_ACTION = [
    InputParam(name="name",
               description="The name of the action",
               required=True),
    InputParam(name="acl",
               description="The UUID of the ACL of the action",
               required=True),
    InputParam(name="description",
               description="Action description",
               required=True),
]

INPUT_PARAMS_ADD_ACTION_TO_PLAYBOOK = [
    InputParam(name="playbook_uuid",
               description="UUID of playbook.",
               required=True),
    InputParam(name="action_uuid",
               description="UUID of action to add.",
               required=True),
]

INPUT_PARAMS_UPDATE_CASE_HISTORY = [
    InputParam(name="case_uuid",
               description="Case UUID",
               required=True),
    InputParam(name="modified",
               description="The time at which the case was modified. Expected format: ISO-8601.",
               required=True),
    InputParam(name="status",
               description="Case's status. Currently only supports value of 'Event'.",
               required=True),
]


def generate_input_params_dict(params: List[InputParam]) -> dict:
    output = {}
    for index, param in enumerate(params):
        param.order = index
        output[param.name] = dataclasses.asdict(param)
    return output


def generate_action(identifier: str, description: str, parameters: Dict, output: List, action_type="generic",
                    read_only=False):
    return {
        # action names must be lower case
        "action": identifier.replace("_", " ").lower(),
        "identifier": identifier,
        "description": description,
        "verbose": "",
        "type": action_type,
        "read_only": read_only,
        "parameters": parameters,
        "output": output,
        "render": {
            "type": "table"
        },
        "versions": "EQ(*)"
    }

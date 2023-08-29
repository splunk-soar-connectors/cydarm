import os

from gen_app_json import *

APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
ACTIONS = [
    generate_action(identifier="test_connectivity",
                    action_type="test",
                    description="Validate the Cydarm asset configuration by attempting to generate an Access Token",
                    read_only=True,
                    parameters={},
                    output=[]),
    generate_action(identifier="get_case",
                    description="Get a Cydarm case by UUID",
                    read_only=True,
                    parameters=generate_input_params_dict([
                        InputParam(name="case_uuid", description="UUID of case to get", required=True),
                    ]),
                    output=OUTPUT_STATUS_MESSAGE_SUMMARY + OUTPUT_CASE_MODEL
                    ),
    generate_action(identifier="get_case_quick_search",
                    description="Query Cydarm cases with a keyword filter",
                    read_only=True,
                    parameters=generate_input_params_dict([
                        InputParam(name="search_string", description="Search string", required=True),
                    ]),
                    output=OUTPUT_STATUS_MESSAGE_SUMMARY + OUTPUT_UUID_AND_ACL_MODEL + OUTPUT_RANK_MODEL
                    ),
    generate_action(identifier="get_cases_filtered",
                    description="""Query Cydarm cases with fine-grain filters including text, tags, etc.
                    Warning: Not fully implemented.
                    Cydarm support confirmed that this REST API endpoint is still under development.
                    TODO: Add remaining params
                    """,
                    read_only=True,
                    parameters=generate_input_params_dict([
                        # TODO: add other params
                        # InputParam(name="filter_text",
                        #            description="""(NOTE: this API field is not yet implemented).
                        #            Text to search for in case locator, description, and metadata values."""),
                        # InputParam(name="tags_included", description="Comma-delimited list of tags to include."),
                    ]),
                    output=OUTPUT_STATUS_MESSAGE_SUMMARY + OUTPUT_CASE_MODEL
                    ),
    generate_action(identifier="create_action_instance_data",
                    description="""Create a plaintext comment on an action instance.
                    Assumes a mimeType='text/plain' and a significance='Comment'.
                    TODO: support other mimeTypes and remaining REST parameters
                    """,
                    read_only=False,
                    parameters=generate_input_params_dict([
                        InputParam(name="action_instance_uuid",
                                   description="UUID of action instance.",
                                   required=True),
                        InputParam(name="data",
                                   description="Comment to add to action instance.",
                                   required=True),
                    ]),
                    output=OUTPUT_STATUS_MESSAGE_SUMMARY + OUTPUT_ACTION_INSTANCE_DATA_MODEL
                    ),
    generate_action(identifier="create_case_data_comment",
                    description="""Create a plaintext comment on a case""",
                    read_only=False,
                    parameters=generate_input_params_dict([
                        InputParam(name="case_uuid",
                                   description="UUID of the case",
                                   required=True),
                        InputParam(name="data",
                                   description="Comment text",
                                   required=True),
                    ]),
                    output=OUTPUT_STATUS_MESSAGE_SUMMARY + OUTPUT_UUID_AND_ACL_MODEL
                    ),
    generate_action(identifier="create_case",
                    description="Create case",
                    read_only=False,
                    parameters=generate_input_params_dict(INPUT_PARAMS_CREATE_CASE),
                    output=OUTPUT_STATUS_MESSAGE_SUMMARY + OUTPUT_UUID_AND_ACL_MODEL
                    ),
    generate_action(identifier="update_case",
                    description="""Update a case.
                    Note: updating tags via this API endpoint doesn't seem to work (at time of testing).
                    Please use actions "add case tag" and "delete case tag" instead
                    """,
                    read_only=False,
                    parameters=generate_input_params_dict(
                        [InputParam(name="case_uuid",
                                    description="Case UUID",
                                    required=True),
                         ] + INPUT_PARAMS_UPDATE_CASE),
                    output=OUTPUT_STATUS_MESSAGE_SUMMARY
                    ),
    generate_action(identifier="update_case_history",
                    description="""Update a case's history.
                    Note: API only supports updating 'status' field to 'Event'
                    """,
                    read_only=False,
                    parameters=generate_input_params_dict(INPUT_PARAMS_UPDATE_CASE_HISTORY),
                    output=OUTPUT_STATUS_MESSAGE_SUMMARY
                    ),
    generate_action(identifier="create_case_playbook",
                    description="Add a playbook to a case",
                    read_only=False,
                    parameters=generate_input_params_dict([
                        InputParam(name="case_uuid",
                                   description="Case UUID",
                                   required=True),
                        InputParam(name="playbook_uuid",
                                   description="Playbook UUID",
                                   required=True),
                    ]),
                    output=OUTPUT_STATUS_MESSAGE_SUMMARY + OUTPUT_UUID_AND_ACL_MODEL
                    ),
    generate_action(identifier="get_case_playbook",
                    description="""Get a playbook instance associated with a case.
                    Warning: Only a subset of output fields are mapped
                    """,
                    read_only=True,
                    parameters=generate_input_params_dict([
                        InputParam(name="case_uuid",
                                   description="Case UUID",
                                   required=True),
                        InputParam(name="case_playbook_uuid",
                                   description="Case Playbook instance UUID",
                                   required=True),
                    ]),
                    output=OUTPUT_STATUS_MESSAGE_SUMMARY + OUTPUT_CASE_PLAYBOOK_MODEL
                    ),
    generate_action(identifier="get_case_playbooks",
                    description="""Gets a list of playbooks for a case.
                    Warning: Only a subset of output fields are mapped
                    """,
                    read_only=True,
                    parameters=generate_input_params_dict([
                        InputParam(name="case_uuid",
                                   description="Case UUID",
                                   required=True),
                    ]),
                    output=OUTPUT_STATUS_MESSAGE_SUMMARY + OUTPUT_CASE_PLAYBOOK_MODEL
                    ),
    generate_action(identifier="get_playbook_action",
                    description="""Get playbook action.
                    Note: only a subset of output fields are mapped
                    """,
                    read_only=True,
                    parameters=generate_input_params_dict([
                        InputParam(name="action_uuid",
                                   description="UUID of the action",
                                   required=True),
                    ]),
                    output=OUTPUT_STATUS_MESSAGE_SUMMARY + OUTPUT_PLAYBOOK_ACTION_DATA_MODEL
                    ),
    generate_action(identifier="create_playbook_action",
                    description="Create playbook action",
                    read_only=False,
                    parameters=generate_input_params_dict(INPUT_PARAMS_CREATE_PLAYBOOK_ACTION),
                    output=OUTPUT_STATUS_MESSAGE_SUMMARY + OUTPUT_UUID_AND_ACL_MODEL
                    ),
    generate_action(identifier="create_playbook",
                    description="Create playbook",
                    read_only=False,
                    parameters=generate_input_params_dict(INPUT_PARAMS_CREATE_PLAYBOOK),
                    output=OUTPUT_STATUS_MESSAGE_SUMMARY + OUTPUT_UUID_AND_ACL_MODEL
                    ),
    generate_action(identifier="add_action_to_playbook",
                    description="Add an existing action to a playbook",
                    read_only=False,
                    parameters=generate_input_params_dict(INPUT_PARAMS_ADD_ACTION_TO_PLAYBOOK),
                    output=OUTPUT_STATUS_MESSAGE_SUMMARY
                    ),
    generate_action(identifier="get_acl",
                    description="Get an ACL by UUID",
                    read_only=True,
                    parameters=generate_input_params_dict([
                        InputParam(name="acl_uuid", description="UUID of acl to get", required=True),
                    ]),
                    output=OUTPUT_STATUS_MESSAGE_SUMMARY + OUTPUT_ACL_OBJECT_MODEL
                    ),
    generate_action(identifier="get_user",
                    description="Get a user by UUID",
                    read_only=True,
                    parameters=generate_input_params_dict([
                        InputParam(name="user_uuid", description="UUID of user to get", required=True),
                    ]),
                    output=OUTPUT_STATUS_MESSAGE_SUMMARY + OUTPUT_USER_MODEL
                    ),
    generate_action(identifier="add_watcher_to_case",
                    description="Add watcher to case",
                    read_only=False,
                    parameters=generate_input_params_dict([
                        InputParam(name="case_uuid", description="Case UUID", required=True),
                        InputParam(name="user_uuid", description="UUID of user to add as watcher", required=True),
                    ]),
                    output=OUTPUT_STATUS_MESSAGE_SUMMARY + OUTPUT_UUID_AND_ACL_MODEL
                    ),
    generate_action(identifier="add_member_to_case",
                    description="Adds a case as a member of another case",
                    read_only=False,
                    parameters=generate_input_params_dict([
                        InputParam(name="case_uuid", description="Case UUID", required=True),
                        InputParam(name="member_case_uuid",
                                   description="UUID of case to add as a member of the case group", required=True),
                    ]),
                    output=OUTPUT_STATUS_MESSAGE_SUMMARY + OUTPUT_UUID_AND_ACL_MODEL
                    ),
    generate_action(identifier="add_case_tag",
                    description="Add tag to case",
                    read_only=False,
                    parameters=generate_input_params_dict([
                        InputParam(name="case_uuid", description="Case UUID", required=True),
                        InputParam(name="tag_value", description="Name of tag", required=True),
                    ]),
                    output=OUTPUT_STATUS_MESSAGE_SUMMARY + OUTPUT_UUID_AND_ACL_MODEL
                    ),
    generate_action(identifier="delete_case_tag",
                    description="Delete tag from case",
                    read_only=False,
                    parameters=generate_input_params_dict([
                        InputParam(name="case_uuid", description="Case UUID", required=True),
                        InputParam(name="tag_value", description="Name of tag", required=True),
                    ]),
                    output=OUTPUT_STATUS_MESSAGE_SUMMARY
                    ),

]
JSON = {
    "appid": "2205e95a-16ab-479d-9c10-363d05153dcb",
    "name": "Cydarm",
    "description": "Integration with Cydarm API",
    "type": "endpoint",
    "product_vendor": "Cydarm",
    "logo": "cydarm.svg",
    "logo_dark": "cydarm_dark.svg",
    "product_name": "Cydarm",
    "python_version": "3",
    "product_version_regex": ".*",
    "publisher": "Splunk Community",
    "contributors": [
        {
            "name": "Ben Liew"
        }
    ],
    "license": "Copyright (c) Splunk, 2023",
    "app_version": APP_VERSION,
    "utctime_updated": "2023-05-22T04:55:46.914172Z",
    "package_name": "phantom_cydarm",
    "main_module": "cydarm_connector.py",
    "min_phantom_version": "6.0.0.114895",
    "app_wizard_version": "1.0.0",
    "custom_made": True,
    "configuration": {
        "cydarm_api_base_url": {
            "description": "Base URL of Cydarm API.  Example: https://xyz.cydarm.io/cydarm-api",
            "data_type": "string",
            "required": True,
            "value_list": [],
            "default": "",
            "order": 0,
            "name": "cydarm_api_base_url",
            "id": 0
        },
        "cydarm_username": {
            "description": "Cydarm username",
            "data_type": "string",
            "required": True,
            "value_list": [],
            "default": "",
            "order": 1,
            "name": "cydarm_username",
            "id": 1
        },
        "cydarm_password": {
            "description": "Cydarm password",
            "data_type": "password",
            "required": True,
            "order": 2,
            "name": "cydarm_password",
            "id": 2
        },
        "basic_auth_username": {
            "description": "Basic auth username",
            "data_type": "string",
            "required": False,
            "value_list": [],
            "default": "",
            "order": 3,
            "name": "basic_auth_username",
            "id": 3
        },
        "basic_auth_password": {
            "description": "Basic auth password",
            "data_type": "password",
            "required": False,
            "order": 4,
            "name": "basic_auth_password",
            "id": 4
        },
    },
    "actions": ACTIONS
}


def main():
    import json
    j = json.dumps(JSON, indent=2)
    print(j)


if __name__ == '__main__':
    # names = [x.name for x in INPUT_CASE_PARAMS]
    main()

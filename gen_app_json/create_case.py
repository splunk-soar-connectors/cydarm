# File: create_case.py
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

from gen_app_json.cydarm_input_param import InputParam


INPUT_PARAMS_CREATE_CASE = [
    InputParam(name="acl", description="The ACL of the data object", required=False),
    InputParam(name="assignee", description="The name of the current assignee", required=False),
    InputParam(name="closed", description="The time at which the case was closed", required=False),
    InputParam(name="created", description="The time at which the case was created", required=False),
    InputParam(name="deletable", data_type="boolean", description="Whether the data is deletable in the current context", required=True),
    InputParam(name="description", description="Description", required=True),
    InputParam(name="editable", data_type="boolean", description="Whether the data is editable in the current context", required=True),
    InputParam(name="locator", description="The locator of the case", required=False),
    InputParam(name="manageable", data_type="boolean", description="Whether the data is manageable in the current context", required=True),
    InputParam(
        name="members",
        description="""UUIDs of member cases (if this case is a group).
                           Expected format: JSON Array.
                           Example: ["d9e526e8-59fc-44e3-8458-08da3269e0b0", "bd10075d-740c-4a7c-931c-c2a65843f3dc"]
                           """,
        required=False,
    ),
    InputParam(
        name="metadata",
        description="""Metadata fields attached to the case.
               Expected format: JSON Object. Example:
               {
                "Email-From" : { "value" : "sender@email.com"},
                "Email-To" : { "value" : "recipient@email.com"}
               }
               """,
        required=False,
    ),
    InputParam(name="minSlaName", description="The minimum SLA name.", required=False),
    InputParam(name="minSlaSeconds", data_type="numeric", description="The minimum SLA remaining time, in seconds.", required=False),
    InputParam(name="org", description="The name of the organisation who the case is relevant to", required=True),
    InputParam(name="readable", data_type="boolean", description="Whether the data is readable in the current context", required=True),
    InputParam(name="severity", data_type="numeric", description="An integer 1 to 5.", required=False),
    InputParam(name="severityName", description="The severity name for the case", required=False),
    InputParam(name="status", description="The current status of the case", required=False),
    InputParam(name="tags", description="The tags attached to this case. Expected format: JSON Array.", required=False),
    InputParam(
        name="totalActionsInAllPlaybooks",
        data_type="numeric",
        description="The total number of actions for all playbooks in a case",
        required=False,
    ),
    InputParam(
        name="totalCompletedActionsInAllPlaybooks",
        data_type="numeric",
        description="The number of actions that are completed for all playbooks in a case",
        required=False,
    ),
    InputParam(name="updateAcls", data_type="boolean", description="Update all ACLS for the case including data items", required=False),
    InputParam(name="uuid", description="The UUID of the case", required=False),
]

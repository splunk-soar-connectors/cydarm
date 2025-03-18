# Cydarm

Publisher: Splunk Community \
Connector Version: 1.0.1 \
Product Vendor: Cydarm \
Product Name: Cydarm \
Minimum Product Version: 6.0.0.114895

Integration with Cydarm API

# Manual Readme Content

## Authentication with Cydarm API

This SOAR app uses token-based authentication to connect to Cydarm API.
Token is generated with the `POST /auth/password` Cydarm endpoint with the user's username and password.

### Configuration variables

This table lists the configuration variables required to operate Cydarm. These variables are specified when configuring a Cydarm asset in Splunk SOAR.

VARIABLE | REQUIRED | TYPE | DESCRIPTION
-------- | -------- | ---- | -----------
**cydarm_api_base_url** | required | string | Base URL of Cydarm API. Example: https://xyz.cydarm.io/cydarm-api |
**cydarm_username** | required | string | Cydarm Username |
**cydarm_password** | required | password | Cydarm Password |
**basic_auth_username** | optional | string | Basic Auth Username |
**basic_auth_password** | optional | password | Basic Auth Password |

### Supported Actions

[test connectivity](#action-test-connectivity) - Validate the Cydarm asset configuration by attempting to generate an Access Token \
[get case](#action-get-case) - Get a Cydarm case by UUID \
[quick search cases](#action-quick-search-cases) - Query Cydarm cases with a keyword filter \
[create action comment](#action-create-action-comment) - Create a plaintext comment on an action instance \
[create case comment](#action-create-case-comment) - Create a plaintext comment on a case \
[create case](#action-create-case) - Create case \
[update case](#action-update-case) - Update a case \
[update case history](#action-update-case-history) - Update a case's history \
[create case playbook](#action-create-case-playbook) - Add a playbook to a case \
[get case playbook](#action-get-case-playbook) - Get a playbook instance associated with a case \
[get case playbooks](#action-get-case-playbooks) - Gets a list of playbooks for a case \
[get playbook action](#action-get-playbook-action) - Get playbook action \
[create playbook action](#action-create-playbook-action) - Create playbook action \
[create playbook](#action-create-playbook) - Create playbook \
[add playbook action](#action-add-playbook-action) - Add an existing action to a playbook \
[get acl](#action-get-acl) - Get an ACL by UUID \
[get user](#action-get-user) - Get a user by UUID \
[add case watcher](#action-add-case-watcher) - Add watcher to case \
[add case member](#action-add-case-member) - Adds a case as a member of another case \
[add case tag](#action-add-case-tag) - Add tag to case \
[delete case tag](#action-delete-case-tag) - Delete tag from case

## action: 'test connectivity'

Validate the Cydarm asset configuration by attempting to generate an Access Token

Type: **test** \
Read only: **True**

#### Action Parameters

No parameters are required for this action

#### Action Output

No Output

## action: 'get case'

Get a Cydarm case by UUID

Type: **generic** \
Read only: **True**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**case_uuid** | required | UUID of case to get | string | `cydarm case uuid` |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failed |
action_result.parameter.case_uuid | string | `cydarm case uuid` | |
action_result.data.\*.acl | string | | |
action_result.data.\*.assignee | string | | |
action_result.data.\*.closed | string | | |
action_result.data.\*.created | string | | |
action_result.data.\*.deletable | boolean | | |
action_result.data.\*.description | string | | |
action_result.data.\*.editable | boolean | | |
action_result.data.\*.locator | string | | |
action_result.data.\*.manageable | boolean | | |
action_result.data.\*.members | string | | |
action_result.data.\*.metadata | string | | |
action_result.data.\*.minSlaName | string | | |
action_result.data.\*.minSlaSeconds | numeric | | |
action_result.data.\*.org | string | | |
action_result.data.\*.readable | boolean | | |
action_result.data.\*.severity | numeric | | |
action_result.data.\*.severityName | string | | |
action_result.data.\*.status | string | | |
action_result.data.\*.tags | string | | |
action_result.data.\*.totalActionsInAllPlaybooks | numeric | | |
action_result.data.\*.totalCompletedActionsInAllPlaybooks | numeric | | |
action_result.data.\*.updateAcls | boolean | | |
action_result.data.\*.uuid | string | | |
action_result.summary | string | | |
action_result.message | string | | |
summary.total_objects | numeric | | |
summary.total_objects_successful | numeric | | |

## action: 'quick search cases'

Query Cydarm cases with a keyword filter

Type: **generic** \
Read only: **True**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**search_string** | required | Search string | string | |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failed |
action_result.parameter.search_string | string | | |
action_result.data.\*.acl | string | | |
action_result.data.\*.rank | numeric | | |
action_result.data.\*.uuid | string | | |
action_result.summary | string | | |
action_result.message | string | | |
summary.total_objects | numeric | | |
summary.total_objects_successful | numeric | | |

## action: 'create action comment'

Create a plaintext comment on an action instance

Type: **generic** \
Read only: **False**

Assumes a mimeType='text/plain' and a significance='Comment'.

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**action_instance_uuid** | required | UUID of action instance | string | `cydarm action instance uuid` |
**data** | required | Comment to add to action instance | string | |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failed |
action_result.parameter.action_instance_uuid | string | `cydarm action instance uuid` | |
action_result.parameter.data | string | | |
action_result.data.\*.action_instance_uuid | string | | |
action_result.data.\*.caseuuid | string | | |
action_result.data.\*.uuid | string | | |
action_result.summary | string | | |
action_result.message | string | | |
summary.total_objects | numeric | | |
summary.total_objects_successful | numeric | | |

## action: 'create case comment'

Create a plaintext comment on a case

Type: **generic** \
Read only: **False**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**case_uuid** | required | UUID of the case | string | `cydarm case uuid` |
**data** | required | Comment text | string | |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failed |
action_result.parameter.case_uuid | string | `cydarm case uuid` | |
action_result.parameter.data | string | | |
action_result.data.\*.acl | string | | |
action_result.data.\*.uuid | string | | |
action_result.summary | string | | |
action_result.message | string | | |
summary.total_objects | numeric | | |
summary.total_objects_successful | numeric | | |

## action: 'create case'

Create case

Type: **generic** \
Read only: **False**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**acl** | optional | The ACL of the data object | string | |
**assignee** | optional | The email address of the current assignee | string | |
**closed** | optional | The time at which the case was closed. Expected format: ISO-8601 | string | |
**created** | optional | The time at which the case was created. Expected format: ISO-8601 | string | |
**deletable** | required | Whether the data is deletable in the current context | boolean | |
**description** | required | Description | string | |
**editable** | required | Whether the data is editable in the current context | boolean | |
**locator** | optional | The locator of the case | string | |
**manageable** | required | Whether the data is manageable in the current context | boolean | |
**members** | optional | UUIDs of member cases (if this case is a group).
Expected format: JSON Array.
Example: ["d9e526e8-59fc-44e3-8458-08da3269e0b0", "bd10075d-740c-4a7c-931c-c2a65843f3dc"]
| string | |
**metadata** | optional | Metadata fields attached to the case.
Expected format: JSON Object. Example:
{
"Email-From" : { "value" : "sender@email.com"},
"Email-To" : { "value" : "recipient@email.com"}
}
| string | |
**minSlaName** | optional | The minimum SLA name | string | |
**minSlaSeconds** | optional | The minimum SLA remaining time, in seconds | numeric | |
**org** | required | The name of the organisation who the case is relevant to | string | |
**readable** | required | Whether the data is readable in the current context | boolean | |
**severity** | optional | An integer 1 to 5 | numeric | |
**severityName** | optional | The severity name for the case | string | |
**status** | optional | The current status of the case | string | |
**tags** | optional | The tags attached to this case. Expected format: JSON Array | string | |
**totalActionsInAllPlaybooks** | optional | The total number of actions for all playbooks in a case | numeric | |
**totalCompletedActionsInAllPlaybooks** | optional | The number of actions that are completed for all playbooks in a case | numeric | |
**updateAcls** | optional | Update all ACLS for the case including data items | boolean | |
**uuid** | optional | The UUID of the case | string | `cydarm case uuid` |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failed |
action_result.parameter.acl | string | | |
action_result.parameter.assignee | string | | |
action_result.parameter.closed | string | | |
action_result.parameter.created | string | | |
action_result.parameter.deletable | string | | |
action_result.parameter.description | string | | |
action_result.parameter.editable | string | | |
action_result.parameter.locator | string | | |
action_result.parameter.manageable | string | | |
action_result.parameter.members | string | | |
action_result.parameter.metadata | string | | |
action_result.parameter.minSlaName | string | | |
action_result.parameter.minSlaSeconds | string | | |
action_result.parameter.org | string | | |
action_result.parameter.readable | string | | |
action_result.parameter.severity | string | | |
action_result.parameter.severityName | string | | |
action_result.parameter.status | string | | |
action_result.parameter.tags | string | | |
action_result.parameter.totalActionsInAllPlaybooks | string | | |
action_result.parameter.totalCompletedActionsInAllPlaybooks | string | | |
action_result.parameter.updateAcls | string | | |
action_result.parameter.uuid | string | `cydarm case uuid` | |
action_result.data.\*.acl | string | | |
action_result.data.\*.uuid | string | | |
action_result.summary | string | | |
action_result.message | string | | |
summary.total_objects | numeric | | |
summary.total_objects_successful | numeric | | |

## action: 'update case'

Update a case

Type: **generic** \
Read only: **False**

Note: updating tags via this API endpoint doesn't seem to work (at time of testing). Please use actions 'add case tag' and 'delete case tag' instead.

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**case_uuid** | required | Case UUID | string | `cydarm case uuid` |
**acl** | optional | The ACL of the data object | string | |
**assignee** | optional | The email address of the current assignee | string | |
**closed** | optional | The time at which the case was closed. Expected format: ISO-8601 | string | |
**created** | optional | The time at which the case was created. Expected format: ISO-8601 | string | |
**deletable** | optional | Whether the data is deletable in the current context | boolean | |
**description** | optional | Description | string | |
**editable** | optional | Whether the data is editable in the current context | boolean | |
**locator** | optional | The locator of the case | string | |
**manageable** | optional | Whether the data is manageable in the current context | boolean | |
**members** | optional | UUIDs of member cases (if this case is a group).
Expected format: JSON Array.
Example: ["d9e526e8-59fc-44e3-8458-08da3269e0b0", "bd10075d-740c-4a7c-931c-c2a65843f3dc"]
| string | |
**metadata** | optional | Metadata fields attached to the case.
Expected format: JSON Object. Example:
{
"Email-From" : { "value" : "sender@email.com"},
"Email-To" : { "value" : "recipient@email.com"}
}
| string | |
**minSlaName** | optional | The minimum SLA name | string | |
**minSlaSeconds** | optional | The minimum SLA remaining time, in seconds | numeric | |
**org** | optional | The name of the organisation who the case is relevant to | string | |
**readable** | optional | Whether the data is readable in the current context | boolean | |
**severity** | optional | An integer 1 to 5 | numeric | |
**severityName** | optional | The severity name for the case | string | |
**status** | optional | The current status of the case | string | |
**tags** | optional | The tags attached to this case. Expected format: JSON Array | string | |
**totalActionsInAllPlaybooks** | optional | The total number of actions for all playbooks in a case | numeric | |
**totalCompletedActionsInAllPlaybooks** | optional | The number of actions that are completed for all playbooks in a case | numeric | |
**updateAcls** | optional | Update all ACLS for the case including data items | boolean | |
**uuid** | optional | The UUID of the case | string | `cydarm case uuid` |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failed |
action_result.parameter.acl | string | | |
action_result.parameter.assignee | string | | |
action_result.parameter.case_uuid | string | `cydarm case uuid` | |
action_result.parameter.closed | string | | |
action_result.parameter.created | string | | |
action_result.parameter.deletable | string | | |
action_result.parameter.description | string | | |
action_result.parameter.editable | string | | |
action_result.parameter.locator | string | | |
action_result.parameter.manageable | string | | |
action_result.parameter.members | string | | |
action_result.parameter.metadata | string | | |
action_result.parameter.minSlaName | string | | |
action_result.parameter.minSlaSeconds | string | | |
action_result.parameter.org | string | | |
action_result.parameter.readable | string | | |
action_result.parameter.severity | string | | |
action_result.parameter.severityName | string | | |
action_result.parameter.status | string | | |
action_result.parameter.tags | string | | |
action_result.parameter.totalActionsInAllPlaybooks | string | | |
action_result.parameter.totalCompletedActionsInAllPlaybooks | string | | |
action_result.parameter.updateAcls | string | | |
action_result.parameter.uuid | string | `cydarm case uuid` | |
action_result.data | string | | |
action_result.summary | string | | |
action_result.message | string | | |
summary.total_objects | numeric | | |
summary.total_objects_successful | numeric | | |

## action: 'update case history'

Update a case's history

Type: **generic** \
Read only: **False**

Note: API only supports updating 'status' field to 'Event'.

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**case_uuid** | required | Case UUID | string | `cydarm case uuid` |
**modified** | required | The time at which the case was modified. Expected format: ISO-8601 | string | |
**status** | required | Case's status. Currently only supports value of 'Event' | string | |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failed |
action_result.parameter.case_uuid | string | `cydarm case uuid` | |
action_result.parameter.modified | string | | |
action_result.parameter.status | string | | |
action_result.data | string | | |
action_result.summary | string | | |
action_result.message | string | | |
summary.total_objects | numeric | | |
summary.total_objects_successful | numeric | | |

## action: 'create case playbook'

Add a playbook to a case

Type: **generic** \
Read only: **False**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**case_uuid** | required | Case UUID | string | `cydarm case uuid` |
**playbook_uuid** | required | Playbook UUID | string | `cydarm playbook uuid` |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failed |
action_result.parameter.case_uuid | string | `cydarm case uuid` | |
action_result.parameter.playbook_uuid | string | `cydarm playbook uuid` | |
action_result.data.\*.acl | string | | |
action_result.data.\*.uuid | string | | |
action_result.summary | string | | |
action_result.message | string | | |
summary.total_objects | numeric | | |
summary.total_objects_successful | numeric | | |

## action: 'get case playbook'

Get a playbook instance associated with a case

Type: **generic** \
Read only: **True**

Warning: Only a subset of output fields are mapped.

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**case_uuid** | required | Case UUID | string | `cydarm case uuid` |
**case_playbook_uuid** | required | Case Playbook instance UUID | string | `cydarm case playbook uuid` |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failed |
action_result.parameter.case_playbook_uuid | string | `cydarm case playbook uuid` | |
action_result.parameter.case_uuid | string | `cydarm case uuid` | |
action_result.data.\*.action_statuses.\*.actionInstanceUuid | string | | |
action_result.data.\*.action_statuses.\*.actionName | string | | |
action_result.data.\*.casePlaybookUuid | string | | |
action_result.data.\*.caseUuid | string | | |
action_result.data.\*.playbookDescription | string | | |
action_result.data.\*.playbookName | string | | |
action_result.summary | string | | |
action_result.message | string | | |
summary.total_objects | numeric | | |
summary.total_objects_successful | numeric | | |

## action: 'get case playbooks'

Gets a list of playbooks for a case

Type: **generic** \
Read only: **True**

Warning: Only a subset of output fields are mapped.

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**case_uuid** | required | Case UUID | string | `cydarm case uuid` |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failed |
action_result.parameter.case_uuid | string | `cydarm case uuid` | |
action_result.data.\*.action_statuses.\*.actionInstanceUuid | string | | |
action_result.data.\*.action_statuses.\*.actionName | string | | |
action_result.data.\*.casePlaybookUuid | string | | |
action_result.data.\*.caseUuid | string | | |
action_result.data.\*.playbookDescription | string | | |
action_result.data.\*.playbookName | string | | |
action_result.summary | string | | |
action_result.message | string | | |
summary.total_objects | numeric | | |
summary.total_objects_successful | numeric | | |

## action: 'get playbook action'

Get playbook action

Type: **generic** \
Read only: **True**

Note: only a subset of output fields are mapped.

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**action_uuid** | required | UUID of the action | string | `cydarm action uuid` |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failed |
action_result.parameter.action_uuid | string | `cydarm action uuid` | |
action_result.data.\*.atc.description | string | | |
action_result.data.\*.atc.name | string | | |
action_result.data.\*.atc.uuid | string | | |
action_result.summary | string | | |
action_result.message | string | | |
summary.total_objects | numeric | | |
summary.total_objects_successful | numeric | | |

## action: 'create playbook action'

Create playbook action

Type: **generic** \
Read only: **False**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**name** | required | The name of the action | string | |
**acl** | required | The UUID of the ACL of the action | string | |
**description** | required | Action description | string | |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failed |
action_result.parameter.acl | string | | |
action_result.parameter.description | string | | |
action_result.parameter.name | string | | |
action_result.data.\*.acl | string | | |
action_result.data.\*.uuid | string | | |
action_result.summary | string | | |
action_result.message | string | | |
summary.total_objects | numeric | | |
summary.total_objects_successful | numeric | | |

## action: 'create playbook'

Create playbook

Type: **generic** \
Read only: **False**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**name** | required | The name of the playbook | string | |
**acl** | required | The UUID of the ACL of the playbook | string | |
**description** | required | Playbook description | string | |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failed |
action_result.parameter.acl | string | | |
action_result.parameter.description | string | | |
action_result.parameter.name | string | | |
action_result.data.\*.acl | string | | |
action_result.data.\*.uuid | string | | |
action_result.summary | string | | |
action_result.message | string | | |
summary.total_objects | numeric | | |
summary.total_objects_successful | numeric | | |

## action: 'add playbook action'

Add an existing action to a playbook

Type: **generic** \
Read only: **False**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**playbook_uuid** | required | UUID of playbook | string | `cydarm playbook uuid` |
**action_uuid** | required | UUID of action to add | string | `cydarm action uuid` |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failed |
action_result.parameter.action_uuid | string | `cydarm action uuid` | |
action_result.parameter.playbook_uuid | string | `cydarm playbook uuid` | |
action_result.data | string | | |
action_result.summary | string | | |
action_result.message | string | | |
summary.total_objects | numeric | | |
summary.total_objects_successful | numeric | | |

## action: 'get acl'

Get an ACL by UUID

Type: **generic** \
Read only: **True**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**acl_uuid** | required | UUID of acl to get | string | `cydarm acl uuid` |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failed |
action_result.parameter.acl_uuid | string | `cydarm acl uuid` | |
action_result.data.\*.aci.\*.uuid | string | | |
action_result.data.\*.description | string | | |
action_result.data.\*.uuid | string | | |
action_result.summary | string | | |
action_result.message | string | | |
summary.total_objects | numeric | | |
summary.total_objects_successful | numeric | | |

## action: 'get user'

Get a user by UUID

Type: **generic** \
Read only: **True**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**user_uuid** | required | UUID of user to get | string | `cydarm user uuid` |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failed |
action_result.parameter.user_uuid | string | `cydarm user uuid` | |
action_result.data.\*.email | string | | |
action_result.data.\*.username | string | | |
action_result.data.\*.uuid | string | | |
action_result.summary | string | | |
action_result.message | string | | |
summary.total_objects | numeric | | |
summary.total_objects_successful | numeric | | |

## action: 'add case watcher'

Add watcher to case

Type: **generic** \
Read only: **False**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**case_uuid** | required | Case UUID | string | `cydarm case uuid` |
**user_uuid** | required | UUID of user to add as watcher | string | `cydarm user uuid` |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failed |
action_result.parameter.case_uuid | string | `cydarm case uuid` | |
action_result.parameter.user_uuid | string | `cydarm user uuid` | |
action_result.data.\*.acl | string | | |
action_result.data.\*.uuid | string | | |
action_result.summary | string | | |
action_result.message | string | | |
summary.total_objects | numeric | | |
summary.total_objects_successful | numeric | | |

## action: 'add case member'

Adds a case as a member of another case

Type: **generic** \
Read only: **False**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**case_uuid** | required | Case UUID | string | `cydarm case uuid` |
**member_case_uuid** | required | UUID of case to add as a member of the case group | string | `cydarm case uuid` |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failed |
action_result.parameter.case_uuid | string | `cydarm case uuid` | |
action_result.parameter.member_case_uuid | string | `cydarm case uuid` | |
action_result.data.\*.acl | string | | |
action_result.data.\*.uuid | string | | |
action_result.summary | string | | |
action_result.message | string | | |
summary.total_objects | numeric | | |
summary.total_objects_successful | numeric | | |

## action: 'add case tag'

Add tag to case

Type: **generic** \
Read only: **False**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**case_uuid** | required | Case UUID | string | `cydarm case uuid` |
**tag_value** | required | Name of tag | string | |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failed |
action_result.parameter.case_uuid | string | `cydarm case uuid` | |
action_result.parameter.tag_value | string | | |
action_result.data.\*.acl | string | | |
action_result.data.\*.uuid | string | | |
action_result.summary | string | | |
action_result.message | string | | |
summary.total_objects | numeric | | |
summary.total_objects_successful | numeric | | |

## action: 'delete case tag'

Delete tag from case

Type: **generic** \
Read only: **False**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**case_uuid** | required | Case UUID | string | `cydarm case uuid` |
**tag_value** | required | Name of tag | string | |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failed |
action_result.parameter.case_uuid | string | `cydarm case uuid` | |
action_result.parameter.tag_value | string | | |
action_result.data | string | | |
action_result.summary | string | | |
action_result.message | string | | |
summary.total_objects | numeric | | |
summary.total_objects_successful | numeric | | |

______________________________________________________________________

Auto-generated Splunk SOAR Connector documentation.

Copyright 2025 Splunk Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.

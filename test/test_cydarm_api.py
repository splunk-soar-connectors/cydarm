import os
import random
from datetime import datetime
from random import randint

import pytest

from cydarm_api import CydarmAPI

ACL_UUID = "e26a30a0-2b4e-4d39-a1d3-5fd0792e6f84"


@pytest.fixture
def cydarm_api_instance():
    base_url = os.environ["CYDARM_BASE_URL"]
    username = os.environ["CYDARM_USERNAME"]
    password = os.environ["CYDARM_PASSWORD"]
    yield CydarmAPI(base_url=base_url, username=username, password=password)


def test_get_bearer_token(cydarm_api_instance):
    token = cydarm_api_instance.generate_bearer_token()
    print(token)


def test_get_case(cydarm_api_instance):
    case_uuid = "00e99897-f141-4819-a371-e3cd03290cd9"
    case = cydarm_api_instance.get_case(case_uuid=case_uuid)
    assert case["uuid"] == case_uuid
    assert "description" in case
    assert "status" in case


def test_update_case(cydarm_api_instance):
    case_uuid = "00e99897-f141-4819-a371-e3cd03290cd9"
    new_severity = random.randint(1, 5)
    cydarm_api_instance.update_case(case_uuid=case_uuid, severity=new_severity)
    case = cydarm_api_instance.get_case(case_uuid=case_uuid)
    assert case['severity'] == new_severity


def test_update_case_history(cydarm_api_instance):
    case_uuid = "a2c49cea-b230-421c-bb8d-a459e0610ea3"
    now = datetime.now().astimezone().isoformat()
    resp = cydarm_api_instance.update_case_history(case_uuid=case_uuid, modified=now, status="Event")
    # HTTP status: no content
    assert resp.status_code == 204


def test_add_watcher_to_case(cydarm_api_instance):
    case_uuid = "a2c49cea-b230-421c-bb8d-a459e0610ea3"
    user = "901ab104-fb6d-498b-b456-dabb1c2dfdac"
    cydarm_api_instance.add_watcher_to_case(case_uuid=case_uuid, user_uuid=user)


def test_add_member_to_case(cydarm_api_instance):
    case_uuid = "a582e39f-ee17-406a-8bb6-a7f78409513a"
    member_case = "1c4a708d-1266-4b97-b7d0-7d02aee433b7"
    resp = cydarm_api_instance.add_member_to_case(case_uuid=case_uuid, member_case_uuid=member_case)
    assert "uuid" in resp


def test_get_cases_filtered_1(cydarm_api_instance):
    # cases = cydarm_api_instance.get_cases_filtered(filter_text="Test", tags_included=["testing"])
    cases = cydarm_api_instance.get_cases_filtered(filter_text="CVE")
    assert len(cases) >= 10
    case_descriptions = set([case["description"] for case in cases])
    assert "Citrix ADC and Citrix Gateway Security Bulletin for CVE-2022-27518" in case_descriptions


def test_get_case_quick_search(cydarm_api_instance):
    cases = cydarm_api_instance.get_case_quick_search(search_string="CVE")
    assert len(cases) > 0
    first_case = cases[0]
    assert "uuid" in first_case
    assert "acl" in first_case


def test_get_playbook(cydarm_api_instance):
    playbook_uuid = "36a3bbd0-d9e9-4dcb-a9a7-ce81931bf579"
    playbook = cydarm_api_instance.get_playbook(playbook_uuid=playbook_uuid)
    assert playbook["atc"]["uuid"] == playbook_uuid
    assert type(playbook["atc"]["actions"]) is list


def test_get_playbooks(cydarm_api_instance):
    playbooks = cydarm_api_instance.get_case_playbooks(case_uuid="a2c49cea-b230-421c-bb8d-a459e0610ea3")
    assert len(playbooks) >= 2
    playbook_names = {x['playbookName'] for x in playbooks}
    assert 'Lessons Learnt' in playbook_names


def test_create_playbook(cydarm_api_instance):
    playbook_name = f"Test playbook {randint(100, 1000)}"
    playbook = cydarm_api_instance.create_playbook(name=playbook_name, description="Test playbook",
                                                   acl_uuid=ACL_UUID)
    assert "uuid" in playbook
    assert "acl" in playbook


def test_create_action(cydarm_api_instance):
    action_name = f"Test action {randint(100, 1000)}"
    action = cydarm_api_instance.create_playbook_action(name=action_name, description="action",
                                                        acl_uuid=ACL_UUID)
    assert "uuid" in action
    assert "acl" in action


def test_add_action_to_playbook(cydarm_api_instance):
    playbook_name = f"Test playbook {randint(100, 1000)}"
    playbook = cydarm_api_instance.create_playbook(name=playbook_name, description="Test playbook",
                                                   acl_uuid=ACL_UUID)
    action_name = f"Test action {randint(100, 1000)}"
    action = cydarm_api_instance.create_playbook_action(name=action_name, description="action",
                                                        acl_uuid=ACL_UUID)
    resp = cydarm_api_instance.add_action_to_playbook(playbook_uuid=playbook["uuid"], action_uuid=action["uuid"])
    assert resp.status_code == 201


def test_get_playbook_action(cydarm_api_instance):
    action_uuid = "0943efeb-b211-4939-952e-65d55d0046f1"
    action = cydarm_api_instance.get_playbook_action(action_uuid=action_uuid)
    atc_obj = action["atc"]
    assert atc_obj["uuid"] == action_uuid
    assert atc_obj["name"] == "Seek external help"


def test_create_case_playbook(cydarm_api_instance):
    playbook_uuid = "be8b8c4d-4a96-4837-b740-5d12030dc4d3"
    case_uuid = "00e99897-f141-4819-a371-e3cd03290cd9"
    resp = cydarm_api_instance.create_case_playbook(playbook_uuid=playbook_uuid,
                                                    case_uuid=case_uuid)
    assert "uuid" in resp


def test_get_case_playbook(cydarm_api_instance):
    case_uuid = "85e344cd-93e9-4b5d-a2ee-e96dd00b8eef"
    case_playbook_uuid = "9d290e96-bf92-4f63-905f-1dae53e69f5d"
    playbook = cydarm_api_instance.get_case_playbook(case_uuid=case_uuid, case_playbook_uuid=case_playbook_uuid)
    assert playbook["caseUuid"] == case_uuid
    assert playbook["casePlaybookUuid"] == case_playbook_uuid
    assert playbook["playbookName"] == "Phishing email"


def test_add_comment_to_action_instance(cydarm_api_instance):
    action_instance_uuid = "15c450e7-5519-4e65-9de7-4f96d8ad2953"
    cydarm_api_instance.create_action_instance_data(action_instance_uuid=action_instance_uuid,
                                                    comment="hello from python")


def test_create_case(cydarm_api_instance):
    resp = cydarm_api_instance.create_case(description="Created in Python", org="SplunkAppDev")
    assert "uuid" in resp


def test_get_user(cydarm_api_instance):
    resp = cydarm_api_instance.get_user(user_uuid="020ea449-f56a-4965-a016-293dbe6ec854")
    assert "uuid" in resp
    assert resp["username"] == "bliew@splunk.com"


def test_get_acl(cydarm_api_instance):
    resp = cydarm_api_instance.get_acl(acl_uuid="e26a30a0-2b4e-4d39-a1d3-5fd0792e6f84")
    assert resp["description"] == "SplunkAppDev case defaults"


def test_add_and_remove_case_tag(cydarm_api_instance):
    created_case = cydarm_api_instance.create_case(description="Created in Python", org="SplunkAppDev")
    case_uuid = created_case["uuid"]

    # assumes that "testing" is an existing tag
    cydarm_api_instance.add_case_tag(case_uuid=case_uuid, tag_value="testing")

    updated_case_1 = cydarm_api_instance.get_case(case_uuid)
    assert "testing" in updated_case_1["tags"]

    cydarm_api_instance.delete_case_tag(case_uuid=case_uuid, tag_value="testing")
    updated_case_2 = cydarm_api_instance.get_case(case_uuid)
    assert updated_case_2["tags"] == []


def test_add_comment_to_case(cydarm_api_instance):
    created_case = cydarm_api_instance.create_case(description="Created in Python", org="SplunkAppDev")
    case_uuid = created_case["uuid"]
    cydarm_api_instance.create_case_data_comment(case_uuid=case_uuid, comment="hello from python")
    print(case_uuid)
    data_list = cydarm_api_instance.get_case_data_list(case_uuid=case_uuid)
    assert any([x["significance"] == "Comment" for x in data_list["case_data"]])

# File: cydarm_connector.py
#
# Copyright (c) Splunk, 2023-2025
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

import json
from collections.abc import Iterable
from typing import Callable, Optional

# Phantom App imports
import phantom.app as phantom
import requests
from phantom.action_result import ActionResult
from phantom.base_connector import BaseConnector

from cydarm_api import CydarmAPI


class RetVal(tuple):
    def __new__(cls, val1, val2=None):
        return tuple.__new__(RetVal, (val1, val2))


class CydarmConnector(BaseConnector):
    def __init__(self):
        super().__init__()

        self._state = None
        self.cydarm: Optional[CydarmAPI] = None

    def _handle_test_connectivity(self, param):
        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        # NOTE: test connectivity does _NOT_ take any parameters
        # i.e. the param dictionary passed to this handler will be empty.
        # Also typically it does not add any data into an action_result either.
        # The status and progress messages are more important.

        self.save_progress("Verifying connection & auth to Cydarm")
        try:
            self.cydarm.generate_bearer_token()
            self.save_progress("Test Connectivity Passed")
            return action_result.set_status(phantom.APP_SUCCESS)
        except Exception as e:
            return action_result.set_status(phantom.APP_ERROR, f"Connection failed: {e}")

    def _handle_get_case_playbook(self, param):
        func = self.cydarm.get_case_playbook
        kwargs = self.extract_args_dict(param, ["case_uuid", "case_playbook_uuid"])
        return self.call_cydarm_api(func, kwargs)

    def _handle_get_case(self, param):
        func = self.cydarm.get_case
        kwargs = self.extract_args_dict(param, ["case_uuid"])
        return self.call_cydarm_api(func, kwargs)

    def _handle_get_case_quick_search(self, param):
        func = self.cydarm.get_case_quick_search
        kwargs = self.extract_args_dict(param, ["search_string"])
        return self.call_cydarm_api(func, kwargs)

    def _handle_get_cases_filtered(self, param):
        func = self.cydarm.get_cases_filtered
        kwargs = self.extract_args_dict(param, ["filter_text", "tags_included"])
        return self.call_cydarm_api(func, kwargs)

    def _handle_create_action_instance_data(self, param):
        func = self.cydarm.create_action_instance_data
        kwargs = self.extract_args_dict(param, ["action_instance_uuid"])
        kwargs["comment"] = param["data"]
        return self.call_cydarm_api(func, kwargs)

    def _handle_create_case_data_comment(self, param):
        func = self.cydarm.create_case_data_comment
        kwargs = self.extract_args_dict(param, ["case_uuid"])
        kwargs["comment"] = param["data"]
        return self.call_cydarm_api(func, kwargs)

    @staticmethod
    def parse_case_args(param) -> dict:
        arg_names = [
            "acl",
            "assignee",
            "closed",
            "created",
            "deletable",
            "description",
            "editable",
            "locator",
            "manageable",
            "members",
            "metadata",
            "minSlaName",
            "minSlaSeconds",
            "modified",
            "org",
            "readable",
            "severity",
            "severityName",
            "status",
            "tags",
            "totalActionsInAllPlaybooks",
            "totalCompletedActionsInAllPlaybooks",
            "updateAcls",
            "uuid",
        ]
        output = CydarmConnector.extract_args_dict(param, arg_names=arg_names)

        if "severity" in output:
            sev = output["severity"]
            if not 1 <= sev <= 5:
                raise ValueError(f"Given severity ({sev}) is not valid - expected 1 to 5.")

        for field in ("metadata", "tags", "members"):
            if field in output:
                output[field] = json.loads(output[field])
        return output

    @staticmethod
    def extract_args_dict(param, arg_names: Iterable[str]) -> dict:
        output = {}
        for arg in arg_names:
            if arg in param:
                output[arg] = param[arg]
        return output

    def _handle_create_case(self, param):
        func = self.cydarm.create_case
        kwargs = self.parse_case_args(param)
        return self.call_cydarm_api(func, kwargs)

    def _handle_update_case(self, param):
        func = self.cydarm.update_case
        kwargs = self.parse_case_args(param)
        return self.call_cydarm_api(func, kwargs)

    def _handle_update_case_history(self, param):
        func = self.cydarm.update_case_history
        kwargs = self.extract_args_dict(param, ["case_uuid", "modified", "status"])
        return self.call_cydarm_api(func, kwargs)

    def _handle_create_case_playbook(self, param):
        func = self.cydarm.create_case_playbook
        kwargs = self.extract_args_dict(param, ["case_uuid", "playbook_uuid"])
        return self.call_cydarm_api(func, kwargs)

    def _handle_get_case_playbooks(self, param):
        func = self.cydarm.get_case_playbooks
        kwargs = self.extract_args_dict(param, ["case_uuid"])
        return self.call_cydarm_api(func, kwargs)

    def _handle_create_playbook(self, param):
        func = self.cydarm.create_playbook
        kwargs = self.extract_args_dict(param, arg_names=("name", "description", "acl_uuid"))
        return self.call_cydarm_api(func, kwargs)

    def _handle_create_playbook_action(self, param):
        func = self.cydarm.create_playbook_action
        kwargs = self.extract_args_dict(param, arg_names=("name", "description", "acl_uuid"))
        return self.call_cydarm_api(func, kwargs)

    def _handle_get_playbook_action(self, param):
        func = self.cydarm.get_playbook_action
        kwargs = self.extract_args_dict(param, ["action_uuid"])
        return self.call_cydarm_api(func, kwargs)

    def _handle_add_action_to_playbook(self, param):
        func = self.cydarm.add_action_to_playbook
        kwargs = self.extract_args_dict(param, ["playbook_uuid", "action_uuid"])
        return self.call_cydarm_api(func, kwargs)

    def _handle_get_user(self, param):
        func = self.cydarm.get_user
        kwargs = self.extract_args_dict(param, ["user_uuid"])
        return self.call_cydarm_api(func, kwargs)

    def _handle_get_acl(self, param):
        func = self.cydarm.get_acl
        kwargs = self.extract_args_dict(param, ["acl_uuid"])
        return self.call_cydarm_api(func, kwargs)

    def _handle_add_watcher_to_case(self, param):
        func = self.cydarm.add_watcher_to_case
        kwargs = self.extract_args_dict(param, ["case_uuid", "user_uuid"])
        return self.call_cydarm_api(func, kwargs)

    def _handle_add_member_to_case(self, param):
        func = self.cydarm.add_member_to_case
        kwargs = self.extract_args_dict(param, ["case_uuid", "member_case_uuid"])
        return self.call_cydarm_api(func, kwargs)

    def _handle_add_case_tag(self, param):
        func = self.cydarm.add_case_tag
        kwargs = self.extract_args_dict(param, ["case_uuid", "tag_value"])
        return self.call_cydarm_api(func, kwargs)

    def call_cydarm_api(self, cydarm_api_func, kwargs):
        self.save_progress(f"Calling {cydarm_api_func.__name__} with kwargs: {kwargs}")
        result = cydarm_api_func(**kwargs)
        self.save_progress(f"Output from {cydarm_api_func.__name__}: {result}")
        return result

    def _handle_delete_case_tag(self, param):
        func = self.cydarm.delete_case_tag
        kwargs = self.extract_args_dict(param, ["case_uuid", "tag_value"])
        return self.call_cydarm_api(func, kwargs)

    def generate_action_result(self, param, request_func: Callable):
        self.save_progress(f"In action handler for: {self.get_action_identifier()}")

        action_result = self.add_action_result(ActionResult(dict(param)))

        response = request_func(param)
        num_items = 1
        if isinstance(response, list):
            num_items = len(response)
            for item in response:
                action_result.add_data(item)
        elif isinstance(response, dict):
            action_result.add_data(response)
        else:
            self.save_progress("No response data.")

        action_result.update_summary(
            {
                "total_objects": num_items,
                "total_objects_successful": num_items,
            }
        )

        return action_result.set_status(phantom.APP_SUCCESS)

    def handle_action(self, param):
        # Get the action that we are supposed to execute for this App Run
        action_id = self.get_action_identifier()

        self.debug_print("action_id", self.get_action_identifier())

        if action_id == "test_connectivity":
            return self._handle_test_connectivity(param)

        func_name = f"_handle_{action_id}"
        func = getattr(self, func_name, None)
        if func is None:
            raise RuntimeError(f"No function found called: {func_name}")
        return self.generate_action_result(param, func)

    def initialize(self):
        # Load the state in initialize, use it to store data
        # that needs to be accessed across actions
        self._state = self.load_state()

        # get the asset config
        config = self.get_config()
        """
        # Access values in asset config by the name

        # Required values can be accessed directly
        required_config_name = config['required_config_name']

        # Optional values should use the .get() function
        optional_config_name = config.get('optional_config_name')
        """

        basic_auth_creds = None
        basic_auth_user = config.get("basic_auth_username")
        basic_auth_pass = config.get("basic_auth_password")
        if basic_auth_user and basic_auth_pass:
            basic_auth_creds = (basic_auth_user, basic_auth_pass)

        self.cydarm = CydarmAPI(
            base_url=config.get("cydarm_api_base_url"),
            username=config.get("cydarm_username"),
            password=config.get("cydarm_password"),
            basic_auth_creds=basic_auth_creds,
            log_function=self.save_progress,
        )

        return phantom.APP_SUCCESS

    def finalize(self):
        # Save the state, this data is saved across actions and app upgrades
        self.save_state(self._state)
        return phantom.APP_SUCCESS


def main():
    import argparse
    import sys

    argparser = argparse.ArgumentParser()

    argparser.add_argument("input_test_json", help="Input Test JSON file")
    argparser.add_argument("-u", "--username", help="username", required=False)
    argparser.add_argument("-p", "--password", help="password", required=False)
    argparser.add_argument("-v", "--verify", action="store_true", help="verify", required=False, default=False)

    args = argparser.parse_args()
    session_id = None

    username = args.username
    password = args.password
    verify = args.verify

    if username is not None and password is None:
        # User specified a username but not a password, so ask
        import getpass

        password = getpass.getpass("Password: ")

    if username and password:
        try:
            login_url = CydarmConnector._get_phantom_base_url() + "/login"

            print("Accessing the Login page")
            r = requests.get(login_url, verify=verify)
            csrftoken = r.cookies["csrftoken"]

            data = dict()
            data["username"] = username
            data["password"] = password
            data["csrfmiddlewaretoken"] = csrftoken

            headers = dict()
            headers["Cookie"] = "csrftoken=" + csrftoken
            headers["Referer"] = login_url

            print("Logging into Platform to get the session id")
            r2 = requests.post(login_url, verify=verify, data=data, headers=headers)
            session_id = r2.cookies["sessionid"]
        except Exception as e:
            print("Unable to get session id from the platform. Error: " + str(e))
            sys.exit(1)

    with open(args.input_test_json) as f:
        in_json = f.read()
        in_json = json.loads(in_json)
        print(json.dumps(in_json, indent=4))

        connector = CydarmConnector()
        connector.print_progress_message = True

        if session_id is not None:
            in_json["user_session_token"] = session_id
            connector._set_csrf_info(csrftoken, headers["Referer"])

        ret_val = connector._handle_action(json.dumps(in_json), None)
        print(json.dumps(json.loads(ret_val), indent=4))

    sys.exit(0)


if __name__ == "__main__":
    main()

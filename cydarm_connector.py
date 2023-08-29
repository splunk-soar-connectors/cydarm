#!/usr/bin/python
# -*- coding: utf-8 -*-
# -----------------------------------------
# Phantom sample App Connector python file
# -----------------------------------------

# Python 3 Compatibility imports
from __future__ import print_function, unicode_literals

import json
from typing import Callable, Iterable, Optional

# Phantom App imports
import phantom.app as phantom
import requests
from bs4 import BeautifulSoup
from phantom.action_result import ActionResult
from phantom.base_connector import BaseConnector

# Usage of the consts file is recommended
# from cydarm_consts import *
from cydarm_api import CydarmAPI


class RetVal(tuple):

    def __new__(cls, val1, val2=None):
        return tuple.__new__(RetVal, (val1, val2))


class CydarmConnector(BaseConnector):

    def __init__(self):

        # Call the BaseConnectors init first
        super(CydarmConnector, self).__init__()

        self._state = None
        self.cydarm: Optional[CydarmAPI] = None

    def _process_empty_response(self, response, action_result):
        if response.status_code == 200:
            return RetVal(phantom.APP_SUCCESS, {})

        return RetVal(
            action_result.set_status(
                phantom.APP_ERROR, "Empty response and no information in the header"
            ), None
        )

    def _process_html_response(self, response, action_result):
        # An html response, treat it like an error
        status_code = response.status_code

        try:
            soup = BeautifulSoup(response.text, "html.parser")
            error_text = soup.text
            split_lines = error_text.split('\n')
            split_lines = [x.strip() for x in split_lines if x.strip()]
            error_text = '\n'.join(split_lines)
        except:
            error_text = "Cannot parse error details"

        message = "Status Code: {0}. Data from server:\n{1}\n".format(status_code, error_text)

        message = message.replace(u'{', '{{').replace(u'}', '}}')
        return RetVal(action_result.set_status(phantom.APP_ERROR, message), None)

    def _process_json_response(self, r, action_result):
        # Try a json parse
        try:
            resp_json = r.json()
        except Exception as e:
            return RetVal(
                action_result.set_status(
                    phantom.APP_ERROR, "Unable to parse JSON response. Error: {0}".format(str(e))
                ), None
            )

        # Please specify the status codes here
        if 200 <= r.status_code < 399:
            return RetVal(phantom.APP_SUCCESS, resp_json)

        # You should process the error returned in the json
        message = "Error from server. Status Code: {0} Data from server: {1}".format(
            r.status_code,
            r.text.replace(u'{', '{{').replace(u'}', '}}')
        )

        return RetVal(action_result.set_status(phantom.APP_ERROR, message), None)

    def _process_response(self, r, action_result):
        # store the r_text in debug data, it will get dumped in the logs if the action fails
        if hasattr(action_result, 'add_debug_data'):
            action_result.add_debug_data({'r_status_code': r.status_code})
            action_result.add_debug_data({'r_text': r.text})
            action_result.add_debug_data({'r_headers': r.headers})

        # Process each 'Content-Type' of response separately

        # Process a json response
        if 'json' in r.headers.get('Content-Type', ''):
            return self._process_json_response(r, action_result)

        # Process an HTML response, Do this no matter what the api talks.
        # There is a high chance of a PROXY in between phantom and the rest of
        # world, in case of errors, PROXY's return HTML, this function parses
        # the error and adds it to the action_result.
        if 'html' in r.headers.get('Content-Type', ''):
            return self._process_html_response(r, action_result)

        # it's not content-type that is to be parsed, handle an empty response
        if not r.text:
            return self._process_empty_response(r, action_result)

        # everything else is actually an error at this point
        message = "Can't process response from server. Status Code: {0} Data from server: {1}".format(
            r.status_code,
            r.text.replace('{', '{{').replace('}', '}}')
        )

        return RetVal(action_result.set_status(phantom.APP_ERROR, message), None)

    def _make_rest_call(self, endpoint, action_result, method="get", **kwargs):
        # **kwargs can be any additional parameters that requests.request accepts

        config = self.get_config()

        resp_json = None

        try:
            request_func = getattr(requests, method)
        except AttributeError:
            return RetVal(
                action_result.set_status(phantom.APP_ERROR, "Invalid method: {0}".format(method)),
                resp_json
            )

        # Create a URL to connect to
        url = self._base_url + endpoint

        try:
            r = request_func(
                url,
                # auth=(username, password),  # basic authentication
                verify=config.get('verify_server_cert', False),
                **kwargs
            )
        except Exception as e:
            return RetVal(
                action_result.set_status(
                    phantom.APP_ERROR, "Error Connecting to server. Details: {0}".format(str(e))
                ), resp_json
            )

        return self._process_response(r, action_result)

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
        return self.cydarm.get_case_playbook(case_uuid=param['case_uuid'],
                                             case_playbook_uuid=param['case_playbook_uuid'])

    def _handle_get_case(self, param):
        return self.cydarm.get_case(case_uuid=param["case_uuid"])

    def _handle_get_case_quick_search(self, param):
        return self.cydarm.get_case_quick_search(search_string=param['search_string'])

    def _handle_get_cases_filtered(self, param):
        return self.cydarm.get_cases_filtered(filter_text=param.get("filter_text"),
                                              tags_included=param.get("tags_included"))

    def _handle_create_action_instance_data(self, param):
        return self.cydarm.create_action_instance_data(action_instance_uuid=param["action_instance_uuid"],
                                                       comment=param["data"])

    def _handle_create_case_data_comment(self, param):
        return self.cydarm.create_case_data_comment(case_uuid=param["case_uuid"],  comment=param["data"])

    @staticmethod
    def parse_case_args(param) -> dict:
        arg_names = ['acl', 'assignee', 'closed', 'created', 'deletable', 'description', 'editable', 'locator',
                     'manageable', 'members', 'metadata', 'minSlaName', 'minSlaSeconds', 'modified', 'org', 'readable',
                     'severity', 'severityName', 'status', 'tags', 'totalActionsInAllPlaybooks',
                     'totalCompletedActionsInAllPlaybooks', 'updateAcls', 'uuid']
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
        kwargs = self.parse_case_args(param)
        return self.cydarm.create_case(**kwargs)

    def _handle_update_case(self, param):
        kwargs = self.parse_case_args(param)
        return self.cydarm.update_case(case_uuid=param["case_uuid"], **kwargs)

    def _handle_update_case_history(self, param):
        return self.cydarm.update_case_history(case_uuid=param["case_uuid"], modified=param["modified"],
                                               status=param["status"])

    def _handle_create_case_playbook(self, param):
        return self.cydarm.create_case_playbook(case_uuid=param["case_uuid"], playbook_uuid=param["playbook_uuid"])

    def _handle_get_case_playbooks(self, param):
        return self.cydarm.get_case_playbooks(case_uuid=param["case_uuid"])

    def _handle_create_playbook(self, param):
        kwargs = self.extract_args_dict(param, arg_names=("name", "description", "acl_uuid"))
        return self.cydarm.create_playbook(**kwargs)

    def _handle_create_playbook_action(self, param):
        kwargs = self.extract_args_dict(param, arg_names=("name", "description", "acl_uuid"))
        return self.cydarm.create_playbook_action(**kwargs)

    def _handle_get_playbook_action(self, param):
        return self.cydarm.get_playbook_action(action_uuid=param["action_uuid"])

    def _handle_add_action_to_playbook(self, param):
        return self.cydarm.add_action_to_playbook(playbook_uuid=param["playbook_uuid"],
                                                  action_uuid=param["action_uuid"])

    def _handle_get_user(self, param):
        return self.cydarm.get_user(user_uuid=param["user_uuid"])

    def _handle_get_acl(self, param):
        return self.cydarm.get_acl(acl_uuid=param["acl_uuid"])

    def _handle_add_watcher_to_case(self, param):
        return self.cydarm.add_watcher_to_case(case_uuid=param['case_uuid'], user_uuid=param['user_uuid'])

    def _handle_add_member_to_case(self, param):
        return self.cydarm.add_member_to_case(case_uuid=param['case_uuid'], member_case_uuid=param['member_case_uuid'])

    def _handle_add_case_tag(self, param):
        return self.cydarm.add_case_tag(case_uuid=param['case_uuid'], tag_value=param['tag_value'])

    def _handle_delete_case_tag(self, param):
        return self.cydarm.delete_case_tag(case_uuid=param['case_uuid'], tag_value=param['tag_value'])

    def generate_action_result(self, param, request_func: Callable):
        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        action_result = self.add_action_result(ActionResult(dict(param)))

        response = request_func(param)
        num_items = 1
        if type(response) == list:
            num_items = len(response)
            for item in response:
                action_result.add_data(item)
        elif type(response) == dict:
            action_result.add_data(response)
        else:
            self.save_progress("No response data.")

        action_result.update_summary({
            "total_objects": num_items,
            "total_objects_successful": num_items,
        })

        return action_result.set_status(phantom.APP_SUCCESS)

    def handle_action(self, param):
        # Get the action that we are supposed to execute for this App Run
        action_id = self.get_action_identifier()

        self.debug_print("action_id", self.get_action_identifier())

        if action_id == 'test_connectivity':
            return self._handle_test_connectivity(param)
        else:
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

        def log_function(string):
            self.save_progress(string)

        basic_auth_creds = None
        basic_auth_user = config.get("basic_auth_username")
        basic_auth_pass = config.get("basic_auth_password")
        if basic_auth_user and basic_auth_pass:
            basic_auth_creds = (basic_auth_user, basic_auth_pass)

        self.cydarm = CydarmAPI(base_url=config.get('cydarm_api_base_url'),
                                username=config.get("cydarm_username"),
                                password=config.get("cydarm_password"),
                                basic_auth_creds=basic_auth_creds,
                                log_function=log_function)

        return phantom.APP_SUCCESS

    def finalize(self):
        # Save the state, this data is saved across actions and app upgrades
        self.save_state(self._state)
        return phantom.APP_SUCCESS


def main():
    import argparse

    argparser = argparse.ArgumentParser()

    argparser.add_argument('input_test_json', help='Input Test JSON file')
    argparser.add_argument('-u', '--username', help='username', required=False)
    argparser.add_argument('-p', '--password', help='password', required=False)

    args = argparser.parse_args()
    session_id = None

    username = args.username
    password = args.password

    if username is not None and password is None:
        # User specified a username but not a password, so ask
        import getpass
        password = getpass.getpass("Password: ")

    if username and password:
        try:
            login_url = CydarmConnector._get_phantom_base_url() + '/login'

            print("Accessing the Login page")
            r = requests.get(login_url, verify=False)
            csrftoken = r.cookies['csrftoken']

            data = dict()
            data['username'] = username
            data['password'] = password
            data['csrfmiddlewaretoken'] = csrftoken

            headers = dict()
            headers['Cookie'] = 'csrftoken=' + csrftoken
            headers['Referer'] = login_url

            print("Logging into Platform to get the session id")
            r2 = requests.post(login_url, verify=False, data=data, headers=headers)
            session_id = r2.cookies['sessionid']
        except Exception as e:
            print("Unable to get session id from the platform. Error: " + str(e))
            exit(1)

    with open(args.input_test_json) as f:
        in_json = f.read()
        in_json = json.loads(in_json)
        print(json.dumps(in_json, indent=4))

        connector = CydarmConnector()
        connector.print_progress_message = True

        if session_id is not None:
            in_json['user_session_token'] = session_id
            connector._set_csrf_info(csrftoken, headers['Referer'])

        ret_val = connector._handle_action(json.dumps(in_json), None)
        print(json.dumps(json.loads(ret_val), indent=4))

    exit(0)


if __name__ == '__main__':
    main()

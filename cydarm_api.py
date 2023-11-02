# File: cydarm_api.py
#
# Copyright (c) 2023 Splunk Inc.
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

from base64 import b64encode
from typing import Callable, Tuple

import requests


class CydarmAPI:
    def __init__(self, base_url, username, password, basic_auth_creds: Tuple[str, str] = None,
                 log_function: Callable[[str], None] = None):
        # base_url should look like https://xyz.cydarm.io/cydarm_api
        self.base_url = base_url
        self.username = username
        self.password = password
        self.basic_auth_creds = basic_auth_creds
        self.log_function = log_function

    @staticmethod
    def to_base64(string):
        return b64encode(string.encode("ascii")).decode("ascii")

    def generate_bearer_token(self) -> str:
        session = self.create_session(with_bearer_token=False)
        resp = self.rest_call_with_session(session, "post", "/auth/password", return_json=False,
                                           json={
                                               "username": self.to_base64(self.username),
                                               "password": self.to_base64(self.password)
                                           })
        return resp.headers["Access-Token"]

    def create_session(self, with_bearer_token=True):
        session = requests.session()

        if self.basic_auth_creds:
            session.auth = self.basic_auth_creds

        if with_bearer_token:
            session.headers.update({
                "x-cydarm-authz": self.generate_bearer_token()
            })
        return session

    def rest_call_with_session(self, session, method: str, url_path: str, return_json: bool = True, **kwargs):
        func = getattr(session, method)
        url = f"{self.base_url}{url_path}"

        if self.log_function:
            self.log_function(
                f"HTTP {method} request to {url} with auth={session.auth}, headers={session.headers} and kwargs={kwargs}")

        resp = func(url, **kwargs)
        resp.raise_for_status()
        if return_json:
            return resp.json()
        else:
            return resp

    def rest_call(self, method: str, url_path: str, return_json: bool = True, **kwargs):
        session = self.create_session()
        return self.rest_call_with_session(session, method, url_path, return_json=return_json, **kwargs)

    def rest_get(self, url, **kwargs):
        return self.rest_call(method="get", url_path=url, **kwargs)

    def rest_post(self, url, **kwargs):
        return self.rest_call(method="post", url_path=url, **kwargs)

    def rest_delete(self, url, **kwargs):
        return self.rest_call(method="delete", url_path=url, return_json=False, **kwargs)

    def rest_put(self, url, **kwargs):
        return self.rest_call(method="put", url_path=url, return_json=False, **kwargs)

    def get_case(self, case_uuid):
        return self.rest_get(f"/case/{case_uuid}")

    def get_playbook(self, playbook_uuid):
        return self.rest_get(f"/playbook/{playbook_uuid}")

    def create_playbook(self, name: str = None, description: str = None, acl_uuid: str = None):
        return self.rest_post("/playbook", json={
            "atc": {
                "name": name,
                "description": description,
                "acl": acl_uuid
            }
        })

    def get_playbook_action(self, action_uuid):
        return self.rest_get(f"/playbook-action/{action_uuid}")

    def create_playbook_action(self, name: str = None, description: str = None, acl_uuid: str = None):
        return self.rest_post("/playbook-action", json={
            "atc": {
                "name": name,
                "description": description,
                "acl": acl_uuid
            }
        })

    def add_action_to_playbook(self, playbook_uuid: str, action_uuid: str):
        return self.rest_post(f"/playbook/{playbook_uuid}/playbook-action/{action_uuid}", json={
            "atc": {}
        }, return_json=False)

    def get_case_playbook(self, case_uuid, case_playbook_uuid):
        return self.rest_get(f"/case/{case_uuid}/playbook/{case_playbook_uuid}")

    def get_case_playbooks(self, case_uuid):
        return self.rest_get(f"/case/{case_uuid}/playbook")

    def create_case_playbook(self, case_uuid, playbook_uuid):
        return self.rest_post(f"/case/{case_uuid}/playbook/{playbook_uuid}")

    def add_watcher_to_case(self, case_uuid: str, user_uuid: str):
        return self.rest_post(f"/case/{case_uuid}/watch", json={
            "user_uuid": user_uuid
        })

    def add_member_to_case(self, case_uuid: str, member_case_uuid: str):
        return self.rest_post(f"/case/{case_uuid}/member/{member_case_uuid}")

    def update_case(self, case_uuid: str, **kwargs):
        self.rest_put(f"/case/{case_uuid}", json=kwargs)

    def update_case_history(self, case_uuid: str, modified: str, status: str):
        return self.rest_put(f"/case/{case_uuid}/history", json={
            "modified": modified,
            "status": status,
        })

    def create_case(self, description: str, org: str, deletable: bool = True, editable: bool = True,
                    manageable: bool = True, readable: bool = True, **kwargs):
        body = {
            "deletable": deletable,
            "description": description,
            "editable": editable,
            "manageable": manageable,
            "org": org,
            "readable": readable
        }
        body.update(**kwargs)
        return self.rest_post("/case",
                              json=body)

    def create_action_instance_data(self, action_instance_uuid: str, comment: str):
        return self.rest_post(f"/action-instance/{action_instance_uuid}/data",
                              json={
                                  "data": self.to_base64(comment),
                                  "mimeType": "text/plain",
                                  "significance": "Comment"})

    def create_case_data_comment(self, case_uuid: str, comment: str):
        return self.rest_post(f"/case/{case_uuid}/data", json={
            "data": self.to_base64(comment),
            "mimeType": "text/plain",
            "significance": "Comment"
        })

    def get_case_data_list(self, case_uuid: str):
        return self.rest_get(f"/case/{case_uuid}/data")

    def get_case_quick_search(self, search_string: str):

        return self.rest_post("/case/quick-search", json={
            "searchString": search_string
        })

    def get_cases_filtered(self, page_size=1000, filter_text: str = "", tags_included: str = ""):
        # TODO: implement remaining query params for getCasesFiltered
        # TODO: Cydarm API seems to have bug with cases that have multiple assigned tags - returns HTTP 500
        """

        :param page_size:
        :param filter_text:
        :param tags_included: comma separated list of tags.
        :return:
        """
        all_data = []
        page_number = 0
        while True:
            resp = self.get_cases_filtered_paginated(page_num=page_number, page_size=page_size, filter_text=filter_text,
                                                     tags_included=tags_included)
            all_data.extend(resp['data'])
            if 'next' in resp['links']:
                page_number += 1
            else:
                break
        return all_data

    def get_cases_filtered_paginated(self, page_size=1000, page_num=0, filter_text: str = None,
                                     tags_included: str = None):
        params = {
            "page[number]": page_num,
            "page[size]": page_size,
        }
        if filter_text:
            params["filter[text]"] = filter_text
        if tags_included:
            params["filter[inc_tag]"] = tags_included
        return self.rest_get("/case", params=params)

    def get_user(self, user_uuid):
        return self.rest_get(f"/user/{user_uuid}")

    def get_acl(self, acl_uuid):
        return self.rest_get(f"/acl/{acl_uuid}")

    def add_case_tag(self, case_uuid: str, tag_value: str):
        return self.rest_post(f"/case/{case_uuid}/tag", json={
            "tagValue": tag_value
        })

    def delete_case_tag(self, case_uuid: str, tag_value: str):
        return self.rest_delete(f"/case/{case_uuid}/tag", json={
            "tagValue": tag_value
        })

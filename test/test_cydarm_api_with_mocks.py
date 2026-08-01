# File: test_cydarm_api_with_mocks.py
#
# Copyright (c) 2023-2026 Splunk Inc.
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

import base64

import pytest

from cydarm_api import CydarmAPI


BASE_URL = "mock://cydarm.com/api"
USERNAME = "user"
PASSWORD = "pass"  # pragma: allowlist secret
BEARER_TOKEN = "bearer token jwt"
CASE_UUID = "00e99897-f141-4819-a371-e3cd03290cd9"  # pragma: allowlist secret


def as_b64_string(string) -> str:
    return base64.b64encode(string.encode("ascii")).decode("ascii")


class TestGenerateBearerToken:
    def custom_matcher(self, request):
        # check json payload
        j = request.json()
        assert j["password"] == as_b64_string(PASSWORD)
        assert j["username"] == as_b64_string(USERNAME)
        return True

    def test_with_no_basic_auth(self, requests_mock):
        requests_mock.post(f"{BASE_URL}/auth/password", additional_matcher=self.custom_matcher, headers={"Access-Token": BEARER_TOKEN})

        api = CydarmAPI(base_url=BASE_URL, username=USERNAME, password=PASSWORD)
        token = api.generate_bearer_token()
        assert token == BEARER_TOKEN

    def test_with_basic_auth(self, requests_mock):
        requests_mock.post(
            f"{BASE_URL}/auth/password",
            additional_matcher=self.custom_matcher,
            request_headers={
                "Authorization": f"Basic {as_b64_string('basic:basic')}",
            },
            headers={"Access-Token": BEARER_TOKEN},
        )

        api = CydarmAPI(base_url=BASE_URL, username=USERNAME, password=PASSWORD, basic_auth_creds=("basic", "basic"))
        token = api.generate_bearer_token()
        assert token == BEARER_TOKEN


class TestGetCase:
    def test_get_case_with_basic_auth_disabled(self, mocker, requests_mock):
        mocker.patch("cydarm_api.CydarmAPI.generate_bearer_token", return_value=BEARER_TOKEN)
        response_object = {"uuid": CASE_UUID}
        requests_mock.get(f"{BASE_URL}/case/{CASE_UUID}", request_headers={"x-cydarm-authz": BEARER_TOKEN}, json=response_object)
        api = CydarmAPI(base_url=BASE_URL, username=USERNAME, password=PASSWORD)
        assert response_object == api.get_case(case_uuid=CASE_UUID)

    def test_get_case_with_basic_auth_enabled(self, mocker, requests_mock):
        mocker.patch("cydarm_api.CydarmAPI.generate_bearer_token", return_value=BEARER_TOKEN)
        response_object = {"uuid": CASE_UUID}
        expected_auth_header = f"Basic {as_b64_string('basic:basic')}"
        requests_mock.get(
            f"{BASE_URL}/case/{CASE_UUID}",
            request_headers={"Authorization": expected_auth_header, "x-cydarm-authz": BEARER_TOKEN},
            json=response_object,
        )
        api = CydarmAPI(base_url=BASE_URL, username=USERNAME, password=PASSWORD, basic_auth_creds=("basic", "basic"))
        assert response_object == api.get_case(case_uuid=CASE_UUID)

    def test_uppercase_uuid_is_normalized(self, mocker, requests_mock):
        mocker.patch("cydarm_api.CydarmAPI.generate_bearer_token", return_value=BEARER_TOKEN)
        requests_mock.get(
            f"{BASE_URL}/case/{CASE_UUID}",
            request_headers={"x-cydarm-authz": BEARER_TOKEN},
            json={"uuid": CASE_UUID},
        )

        api = CydarmAPI(base_url=BASE_URL, username=USERNAME, password=PASSWORD)
        assert api.get_case(case_uuid=CASE_UUID.upper()) == {"uuid": CASE_UUID}

    @pytest.mark.parametrize(
        "invalid_uuid",
        [
            ".",
            "..",
            "../user?",
            "../../admin/secret-config?injected=1",
            "00e99897/f141/4819/a371/e3cd03290cd9",
            "00e99897-f141-4819-a371-e3cd03290cd9?role=admin",
            "00e99897f1414819a371e3cd03290cd9",  # pragma: allowlist secret
            "abc123",
        ],
    )
    def test_noncanonical_uuid_is_rejected_before_request(self, mocker, invalid_uuid):
        generate_bearer_token = mocker.patch("cydarm_api.CydarmAPI.generate_bearer_token")
        api = CydarmAPI(base_url=BASE_URL, username=USERNAME, password=PASSWORD)

        with pytest.raises(ValueError, match="canonical UUID"):
            api.get_case(case_uuid=invalid_uuid)

        generate_bearer_token.assert_not_called()


class TestRequestLogging:
    def test_request_log_omits_credentials_headers_and_payload(self, requests_mock):
        messages = []
        requests_mock.post(f"{BASE_URL}/auth/password", headers={"Access-Token": BEARER_TOKEN})
        api = CydarmAPI(
            base_url=BASE_URL,
            username=USERNAME,
            password=PASSWORD,
            basic_auth_creds=("basic", "basic-secret"),
            log_function=messages.append,
        )

        api.generate_bearer_token()

        assert messages == [f"HTTP post request to {BASE_URL}/auth/password"]
        assert as_b64_string(PASSWORD) not in messages[0]
        assert "basic-secret" not in messages[0]

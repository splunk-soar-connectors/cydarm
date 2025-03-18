# File: update_case.py
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

from copy import deepcopy

from gen_app_json.create_case import INPUT_PARAMS_CREATE_CASE


INPUT_PARAMS_UPDATE_CASE = deepcopy(INPUT_PARAMS_CREATE_CASE)
for input_param in INPUT_PARAMS_UPDATE_CASE:
    input_param.required = False

OUTPUT_CASE_MODEL = [x.as_output_field() for x in INPUT_PARAMS_UPDATE_CASE]

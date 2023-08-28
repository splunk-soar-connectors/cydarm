from copy import deepcopy

from gen_app_json.create_case import INPUT_PARAMS_CREATE_CASE

INPUT_PARAMS_UPDATE_CASE = deepcopy(INPUT_PARAMS_CREATE_CASE)
for input_param in INPUT_PARAMS_UPDATE_CASE:
    input_param.required = False

OUTPUT_CASE_MODEL = [x.as_output_field() for x in INPUT_PARAMS_UPDATE_CASE]

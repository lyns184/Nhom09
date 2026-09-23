from policy import POLICY
from test_data import *


def json_search(key, input_object, role=None):
    ret_val = []

    if key in POLICY and role not in POLICY[key]:
        return ret_val

    if isinstance(input_object, dict):
        # Iterate dictionary
        for k, v in input_object.items():
            # searching key in the dict
            if k == key:
                temp = {k: v}
                ret_val.append(temp)

            if isinstance(v, dict):
                # the value is another dict so repeat
                ret_val.extend(json_search(key, v, role))

            elif isinstance(v, list):
                # it's a list
                for item in v:
                    # if dict or list repeat
                    if isinstance(item, (dict, list)):
                        ret_val.extend(json_search(key, item, role))

    elif isinstance(input_object, list):
        # Iterate a list because some APIs return JSON object in a list
        for val in input_object:
            if isinstance(val, (dict, list)):
                ret_val.extend(json_search(key, val, role))

    return ret_val

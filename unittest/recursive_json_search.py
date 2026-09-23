from test_data import *


def json_search(key, input_object):
    ret_val = []

    if isinstance(input_object, dict):
        for current_key, value in input_object.items():
            if current_key == key:
                ret_val.append({current_key: value})

            if isinstance(value, (dict, list)):
                child_results = json_search(key, value)
                ret_val.extend(child_results)

    elif isinstance(input_object, list):
        for item in input_object:
            if isinstance(item, (dict, list)):
                child_results = json_search(key, item)
                ret_val.extend(child_results)

    return ret_val


if __name__ == "__main__":
    print(json_search("issueSummary", data))
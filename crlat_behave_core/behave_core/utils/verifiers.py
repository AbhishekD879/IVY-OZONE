from jsonpath_ng import parse


def verify_json_field(json_resp, field_path, field_value):
    actual_field_value = get_field_value(json_resp, field_path)
    assert actual_field_value == field_value, f'Actual value "{actual_field_value}" for "key" - ' \
                                              f'"{field_path}" differs from expected "{field_value}".'


def verify_json_field_is_string(json_resp, field_path):
    actual_field_value = get_field_value(json_resp, field_path)
    assert isinstance(actual_field_value, str), f'"{actual_field_value}" is not type of string.'


def get_field_value(json_resp, field_path):
    expr = parse(field_path)
    if isinstance(json_resp, (list, tuple)):
        field_value = [match.value for match in expr.find(json_resp[0])]
        return field_value[0] if field_value else None
    elif isinstance(json_resp, dict):
        field_value = [match.value for match in expr.find(json_resp)]
        return field_value[0] if field_value else None

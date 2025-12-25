import requests
import json
from requests.exceptions import JSONDecodeError
from jsonschema import validate
from jsonschema.exceptions import ValidationError

def is_valid_response(response: requests.Response, check_json: bool = False, check_type: str = None):
    """
    Docstring for is_valid_response

    :param response: Requests response object.
    :type response: requests.Response
    :param check_json: If set to true it will check if the response is parseable to a json-like object with the requests json provided method.
    :type check_json: bool
    :param check_type: If set to true it will check if after parsing the response we get and specific type, for example: an array.
    :type check_type: str
    """
    r = None

    if not isinstance(response, requests.Response):
        # TODO: add loggin
        return False

    if response.status_code not in [200, 206]:
        return False

    if check_json:
        try:
            r = response.json()
        except JSONDecodeError:
            return False

    if check_type and check_json:
        return isinstance(r, check_type)

    return True


def validate_json_schema(instance: list[dict], schema_type: dict):
    schema = {}
    if str.lower(schema_type) == 'devoto':
        with open("/home/FranciscoGibert/supermarkets-uy/Supermarkets-UY/utils/devoto_schema.json", "r") as file:
            schema = json.load(file)

    try:
        validate(instance=instance, schema=schema)
    except ValidationError:
        return False

    return True
import requests
import json
from requests.exceptions import JSONDecodeError
from utils.custom_exceptions import NotARequestObjectError
from jsonschema import validate
from jsonschema.exceptions import ValidationError

def validate_request(response, *args, **kwargs) -> bool:
    if not isinstance(response, requests.Response): raise NotARequestObjectError("Response passed is not a requests object.")
    if not response.ok: print(f"Status code of request {response.url} was not good, see this: {response.status_code}, {response.reason}")

def validate_json_schema(instance: list[dict], schema_type: dict):
    schema = {}
    if str.lower(schema_type) == 'devoto':
        with open("utils/devoto_schema.json", "r") as file:
            schema = json.load(file)

    try:
        validate(instance=instance, schema=schema)
    except ValidationError:
        return False
    
    return True
import requests
import json
from requests.exceptions import JSONDecodeError
from utils.custom_exceptions import NotARequestObjectError
from jsonschema import validate
from jsonschema.exceptions import ValidationError

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
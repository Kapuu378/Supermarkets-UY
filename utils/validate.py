from context import *
from jsonschema import validate
from jsonschema.exceptions import ValidationError
import json as jsonlib

def validate_json_schema(json, path_to_schema):
    schema = {}
    with open(path_to_schema, "r") as file:
        schema = jsonlib.load(file)

    try:
        validate(instance=json, schema=schema)
    except ValidationError:
        return False

    return True
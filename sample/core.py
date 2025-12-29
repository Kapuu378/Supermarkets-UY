from pathlib import Path
from utils.validate import validate_json_schema
from utils._request import Client
from requests.exceptions import JSONDecodeError

class VtexBaseScrapper():    
    client = Client()

    def __init__(self, base_url):
        self.base_url = base_url

    def _fetch(self, params):
        return self.client.get(url=self.base_url, params=params)
    
    def _parse(self, response):
        parsed_res = None
        try:
            parsed_res = response.json()
        except JSONDecodeError:
            print("Response can't be parsed into json.")
        return parsed_res

    def _validate_json(self, json, path_to_schema: Path):
        return validate_json_schema(json, path_to_schema)
    
    def _extract_subdict(self, dict, key_mapping):
        result = {}
        for key, value in key_mapping.items():
            dummy_dict = dict.copy()
            for v in value:
                try:
                    dummy_dict = dummy_dict[v]
                except KeyError:
                    print("Error during creation of subdict. Some key in mapping was not found. ", value)
                    return {}
            result.update({key: dummy_dict})
        return result




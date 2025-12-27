
from context import *
from datetime import datetime

from utils.database import Prices, create_session, get_or_create_product
from utils.validate import validate_json_schema, is_valid_response
from utils.transform import flatten
from utils._request import Client
from sample.devoto_categories import CATEGORIES

import requests

db_session = create_session()

DEFAULT_KEY_MAPPING = {
    "productId": "PROD_ID",
    "productName": "PROD_NAME",
    "brand": "BRAND",
    "linkText": "LK_TEXT",
    "FullSellingPrice": "UNIT_P",
    "Price": "FULL_P",
    "PriceWithoutDiscount": "FULL_P_ND",
}

class Devoto():
    base_url = 'https://www.devoto.com.uy/api/catalog_system/pub/products/search?'

    def __init__(self):
        self.client = Client()

    def _fetch(
            self,
            category: str,
            _from: int,
            _to: int
    ) -> requests.Response | None:
        params = {
            "_from":_from,
            "_to":_to,
            "fq":f"C:{category}",
            "hideUnavailableItems":"true",
            "sc":"1"
        }
        print("Fetching devoto: ", params)
        response = self.client.get(self.base_url, params=params)
        return response

    def _validate_response(self, response):
        if not is_valid_response(response, check_json=True, check_type=list):
            return False
        
        return response

    def _validate_json(self, json_list, schema='Devoto'):
        """
        This function receives a list of dictionaries (parsed jsons) and returns a
        list of the dictionaries that were proved valid against a json schema.

        :param json_list: List of dictionaries.
        :param schema: a Json schema.
        """
        for index, json in enumerate(json_list):
            if not validate_json_schema(json, schema):
                json_list[index] = 'invalid json'

        valid_jsons_list = [j for j in json_list if j != 'invalid json']
        return valid_jsons_list

    def _extract_data(self,
        vaild_json_list,
        key_mapping=DEFAULT_KEY_MAPPING
    ):

        data_list = []

        for json in vaild_json_list:
            flat_json = flatten(json)

            data = {
                key_mapping[k]: flat_json[k]
                for k in key_mapping
                if k in flat_json
            }

            data_list.append(data)

        return data_list
    
    def scrape(self, category: str, _from: int, _to: int, schema: str, *args, **kwargs):
        response = self._fetch(category=category, _from=_from, _to=_to)
        response = self._validate_response(response)
        if not response: return []

        json = response.json()
        valid_jsons_list = self._validate_json(json_list=json, schema=schema)

        data_list = self._extract_data(valid_jsons_list)
        return data_list



if __name__ == '__main__':
    devoto = Devoto()
    today = datetime.now().strftime("%Y-%m-%d")
    cluster_ids = None
    db_session.info["_pushed_product_ids"] = []
    
    # Here we grab the list of the products that were already inserted in the DB today. 
    # We load those into memory for quick validating.
    db_session.info["_pushed_product_ids"].extend(
        [int(price.PROD_FK) for price in 
        db_session.query(Prices.PROD_FK).filter(Prices.DATE==today).all()])
    
    # Category ID's:
    categories = CATEGORIES
    for category in categories:
        _from = 0
        _to = 49
        empty_hit = 0
        
        while _from < 2500:
            data_list = devoto.scrape(
                category=category,
                _from=_from,
                _to=_to,
                schema='Devoto'
            ) 
            if empty_hit == 2:
                print("Hitting dead end for category: ", category)
                break
            if data_list == []:
                empty_hit = empty_hit + 1
                continue
            
            def add_info(d):
                d.update({'DATE': today, 'SMK_NAME':'Devoto'})
                return d
            data_list = list(map(add_info, data_list))

            for d in data_list:
                product = get_or_create_product(d, db_session)
                
                if product.ID in db_session.info["_pushed_product_ids"]:
                    print(f"Product: {product.PROD_NAME} already pushed today to DB with Primary Key: {product.ID}")
                    continue
                else:
                    price = Prices(**{k:v for k,v in d.items() if k in Prices.__table__.columns}, PROD_FK=product.ID)
                    db_session.add(price)
                    # Save last pushed product id in cache.
                    db_session.info["_pushed_product_ids"].append(product.ID)

            db_session.commit()
            _from = _from + 49
            _to = _to + 49

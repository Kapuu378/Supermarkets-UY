
from context import *
from datetime import datetime
import pickle
import os
import time

from utils.database import Prices, Products, create_session
from utils.validate import validate_json_schema, is_valid_response
from utils.transform import flatten
from utils._request import Client

import requests
from sqlalchemy.orm.exc import NoResultFound

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
    base_url = 'https://www.devoto.com.uy/api/catalog_system/pub/products/search?&_from=0&_to=49&fq=productClusterIds:'
    date = datetime.now()

    def __init__(self):
        self.client = Client()

    def _fetch(
            self,
            cluster_id,
    ) -> requests.Response | None:

        response = self.client.get(f"{self.base_url}{cluster_id}")
        return response

    def _validate_response(self, response, check_json=True, check_type=list):
        if not is_valid_response(response, check_json=check_json, check_type=check_type):
            return None

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

    def scrape(self, cluster_id, schema='devoto', *args, **kwargs):
        response = self._fetch(cluster_id=cluster_id)
        response = self._validate_response(response=response, check_json=True, check_type=list)
        if not response: return []

        json = response.json()
        valid_jsons_list = self._validate_json(json_list=json, schema=schema)

        data_list = self._extract_data(valid_jsons_list)
        return data_list



if __name__ == '__main__':
    devoto = Devoto()
    today = datetime.now()
    block = 3
    cluster_ids = None

    with open(os.path.join(ROOT_PATH, "utils/devoto_cluster_ids.plk"), "rb") as plk:
        cluster_ids = pickle.load(plk)

    results = []

    for index, cluster_id in enumerate(cluster_ids):
        print(index)
        if index > 3: break
        data_list = devoto.scrape(
            cluster_id=cluster_id,
            schema='Devoto'
        )

        for data in data_list:
            data.update({'CLUS_ID': cluster_id, 'DATE': today, 'SMK_NAME':'Devoto'})
            results.append(data)

        if (index + 1) % block == 0:
            product = None
            for r in results:
                try:
                    product = db_session.query(Products).filter_by(
                        PROD_ID=r['PROD_ID'],
                        SMK_NAME=r['SMK_NAME']).one()
                except NoResultFound:
                    product = Products(**{k:v for k,v in r.items() if k in Products.__table__.columns})
                    db_session.add(product)
                    db_session.flush()
                finally:
                    db_session.add(
                        Prices(**{k:v for k,v in r.items() if k in Prices.__table__.columns}, PROD_FK=product.ID))
            
            db_session.commit()
            results = []
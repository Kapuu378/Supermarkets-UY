from utils.database import Prices, Base, create_session
from utils._request import Client
from utils.validate import validate_json_schema
from utils.transform import flatten
from requests.exceptions import JSONDecodeError, ConnectionError, ConnectTimeout
from sqlalchemy import select, inspect


import pickle
from datetime import datetime
import pandas as pd
import os
import time

class Devoto():
    container = []

    def __init__(self, path_to_clusters, base_url):
        self.cluster_ids = self.load_cluster_ids(path_to_clusters)
        self.base_url = base_url
        self.client = Client()

    def fetch_products(
            self,
            limit_clusters=None,
            date=None,
            key_mapping=None
    ):
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")

        if not key_mapping:
            key_mapping = {
                "productId": "PROD_ID",
                "productName": "PROD_NAME",
                "brand": "BRAND",
                "linkText": "LK_TEXT",
                "FullSellingPrice": "FULL_P",
                "Price": "UNIT_P",
                "PriceWithoutDiscount": "FULL_P_ND",
            }

        for n, id in enumerate(self.cluster_ids):
            print(n, id)
            if limit_clusters is not None:
                if n > limit_clusters: break

            try:
                response = self.client.get(self.base_url + str(id))
            except (ConnectionError, ConnectTimeout):
                print("Connection was not estabilished succesfully. Waiting and continuing...")
                time.sleep(60)
                continue

            try:
                response = response.json()
            except JSONDecodeError:
                continue

            if type(response) == list:
                for i, dic in enumerate(response):
                    valid = validate_json_schema(dic, 'devoto')
                    if not valid:
                        response[i] = {}
            else:
                valid = validate_json_schema(response)
                if not valid: response = {}

            for dic in response:
                flat = flatten(dic)

                data = {
                    key_mapping[k]: flat[k]
                    for k in key_mapping
                    if k in flat
                }
                # I know this is hardcoded and it's not good but it will change
                data["CLUS_ID"] = id
                data["DATE"] = date
                data["SMK_NAME"] = 'Devoto'
                data["PROD_UI"] = data["PROD_ID"] + "-" + data["SMK_NAME"]

                print(data)
                self.container.append(data)

    def remove_duplicates(self, subset):
        self.container = pd.DataFrame(data=self.container).drop_duplicates(subset=subset, ignore_index=True).to_dict('records')
        return self.container

    def add_orm_objects(self, session, table, if_not_exists=False, match=[], *args, **kwargs):
        if not issubclass(table, Base):
            raise TypeError("param: base should be an instance of Base mysqlalchemy class.")

        for dic in self.container:
            obj = table(**{k:v for k,v in dic.items() if k in table.__table__.columns})

            if if_not_exists:
                stmt = select(table).filter_by(
                    **get_orm_object_dict(obj, match)
                )
                result = session.execute(stmt).first()
                if result is not None:
                    continue
            
            print(obj)
            session.add(obj)
        return None

    def merge_orm_objects(self, session, table):
        if not issubclass(table, Base):
            raise TypeError("param: base should be an instance of Base mysqlalchemy class.")

        for dic in self.container:
            elem = table(**{k:v for k,v in dic.items() if k in table.__table__.columns})
            print(elem)
            session.merge(elem)
        return None

    def load_cluster_ids(self, path):
        with open(path, "rb") as plk:
            clusters = pickle.load(plk).copy()
            print(f"Loaded cluster ids:\n", pd.Series(data=clusters))
            return clusters
    
def get_orm_object_dict(obj, match: list)-> dict:
    return {
        attr.key: getattr(obj, attr.key)
        for attr in inspect(obj).mapper.column_attrs
        if attr.key in match
    }


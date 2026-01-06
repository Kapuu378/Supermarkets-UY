from context import *
from datetime import datetime
import json

from utils.database import create_session
from sample.categories import get_tata_categories
from utils.models import VtexBaseScrapper
from utils.functions import(
    get_valid_jsons, extract_subdictionaries, get_or_create_product, 
    create_price_object, get_pushed_products_id, is_json_parseable
)

class Tata(VtexBaseScrapper):
    def __init__(self):
        super().__init__(base_url='https://www.tata.com.uy/api/graphql?')
        self.path_to_schema = os.path.join(ROOT_PATH, "utils/tata_schema.json")
        self.key_mapping = {
        'PROD_ID':['node','id'],
        'PROD_NAME':['node','name'],
        'BRAND':['node','brand', 'brandName'],
        'LK_TEXT':['node','slug'],
        'UNIT_P':['node','offers', 'offers', 0, 'price'],
        # FULL_P doesn't exist in this API.
        'FULL_P_ND':['node', 'offers', 'offers', 0, 'listPrice'],
        }

    def scrape(self, _from, category) -> list[dict]:
        variables = json.dumps(
            {
                "first":50,
                "after":f"{_from}",
                "sort":"score_desc",
                "term":"",
                "selectedFacets":[{"key":"category-1","value":category},{"key":"channel","value":"{\"salesChannel\":\"4\",\"regionId\":\"U1cjdGF0YXV5bW9udGV2aWRlbw==\"}"},{"key":"locale","value":"es-UY"}]
            }
        )
        params = {
            "variables":variables,
            "operationName":"ProductsQuery"
        }
        response = self._fetch(params)
        print(f"Fetching Tata at: {params}")

        if not is_json_parseable(response):
            return []

        try:
            response_jsons = response.json()["data"]["search"]["products"]["edges"]
        except TypeError:
            """Emtpy hit"""
            return []
        valid_jsons = get_valid_jsons(response_jsons, self.path_to_schema)

        return extract_subdictionaries(valid_jsons, self.key_mapping)

if __name__ == '__main__':
    tata = Tata()
    db_session = create_session()
    today = datetime.now().strftime("%Y-%m-%d")
    pushed_ids = get_pushed_products_id(db_session, today)

    categories = get_tata_categories()
    for category in categories:
        _from = 0
        empty_hit = 0
        
        while True:

            data_list = tata.scrape(
                _from=_from,
                category=category
            ) 
            
            if empty_hit == 2:
                print("Hitting dead end for category: ", category)
                break
            if data_list == []:
                empty_hit = empty_hit + 1
                continue
            
            for d in data_list:
                d.update({'DATE': today, 'SMK_NAME':'Tata'})
                product = get_or_create_product(d, db_session)
                
                if product.ID in pushed_ids:
                    print(f"Product: {product.PROD_NAME} already pushed today to DB with Primary Key: {product.ID}")
                    continue
                else:
                    price = create_price_object(d, PROD_FK=product.ID)
                    db_session.add(price)
                    pushed_ids.append(product.ID)

            db_session.commit()
            _from = _from + 50

from context import *
from datetime import datetime
import json

from bs4 import BeautifulSoup

from utils.database import create_session
from sample.categories import get_tienda_inglesa_categories
from utils.models import VtexBaseScrapper
from utils.functions import(
    get_valid_jsons, extract_subdictionaries, get_or_create_product, 
    create_price_object, get_pushed_products_id, parse_price
)

class TiendaInglesa():
    def __init__(self):
        super().__init__(base_url='https://www.tiendainglesa.com.uy/supermercado/categoria/category/busqueda')
        self.path_to_schema = os.path.join(ROOT_PATH, "utils/tienda_inglesa_schema.json")
        self.key_mapping = {
        'PROD_ID':['Id'],
        'PROD_NAME':['Name'],
        'UNIT_P':['Price'],
        # FULL_P, LK_TEXT, BRAND are not able to be retrived from this call.
        'FULL_P_ND':['BeforePriceStr'],
        }

    def scrape(self, page, category) -> list[dict]:
        url = self.base_url + f"?0,0,*%3A*,{category},0,0,,,false,,,,{page}"

        response = self.client.get(url, params=None)
        print(f"Fetching Tienda Inglesa at: {url}")
        # Tienda Inglesa works very differently from the other supermarkets scraped in this project.
        # It's very hard to find a hidden api that we can request and get a clean json with all the data.
        # Insted, i found that in every page there is one single html tag that contains a big json with
        # all the valuable data.
        html = BeautifulSoup(response.content, 'html.parser')
        gxstate = html.select_one("input[name='GXState']").get('value')
        json_data = json.loads(gxstate)['vSEARCHRESPONSE']['Product']

        valid_jsons = get_valid_jsons(json_data, self.path_to_schema)

        return extract_subdictionaries(valid_jsons, self.key_mapping)

if __name__ == '__main__':
    tata = TiendaInglesa()
    db_session = create_session()
    today = datetime.now().strftime("%Y-%m-%d")
    pushed_ids = get_pushed_products_id(db_session, today)

    categories = get_tienda_inglesa_categories()
    for category in categories:
        page = 0
        empty_hit = 0
        
        while True:

            data_list = tata.scrape(
                page=page,
                category=category
            ) 
            
            if empty_hit == 2:
                print("Hitting dead end for category: ", category)
                break
            if data_list == []:
                empty_hit = empty_hit + 1
                continue
            
            for d in data_list:
                # Prices are given as strings like this: "$ 34"
                d['UNIT_P'] = parse_price(d['UNIT_P'])
                
                if len(d['FULL_P_ND']) > 1:
                    d['FULL_P_ND'] = parse_price(d['FULL_P_ND'])
                else:
                    d['FULL_P_ND'] = d['UNIT_P']

                d.update({'DATE': today, 'SMK_NAME':'Tienda_inglesa'})

                product = get_or_create_product(d, db_session)
                if product.ID in pushed_ids:
                    print(f"Product: {product.PROD_NAME} already pushed today to DB with Primary Key: {product.ID}")
                    continue
                else:
                    price = create_price_object(d, PROD_FK=product.ID)
                    db_session.add(price)
                    pushed_ids.append(product.ID)

            db_session.commit()
            page = page + 1

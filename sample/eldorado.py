from context import *
from datetime import datetime

from utils.database import create_session
from sample.categories import get_eldorado_categories
from utils.models import VtexBaseScrapper
from utils.functions import(
    get_valid_jsons, extract_subdictionaries, get_or_create_product, 
    create_price_object, get_pushed_products_id, is_json_parseable
)

class Eldorado(VtexBaseScrapper):
    def __init__(self):
        super().__init__(base_url='https://www.eldorado.com.uy/api/catalog_system/pub/products/search?')
        self.path_to_schema = os.path.join(ROOT_PATH, "utils/eldorado_schema.json")
        self.key_mapping = {
        'PROD_ID':['productId'],
        'PROD_NAME':['productName'],
        'BRAND':['brand'],
        'LK_TEXT':['linkText'],
        'UNIT_P':['items', 0, 'sellers', 0, 'commertialOffer', 'FullSellingPrice'],
        'FULL_P':['items', 0, 'sellers', 0, 'commertialOffer', 'Price'],
        'FULL_P_ND':['items', 0, 'sellers', 0, 'commertialOffer', 'PriceWithoutDiscount'],
        }

    def scrape(self, _from, _to, category) -> list[dict]:
        params = {
            "_from":_from,
            "_to":_to,
            "fq":f"C:{category}",
            "hideUnavailableItems":"true",
            "sc":"1"
        }
        response = self._fetch(params)
        print(f"Fetching Eldorado at: {params}")

        if not is_json_parseable(response):
            return []

        valid_jsons = get_valid_jsons(response.json(), self.path_to_schema)

        return extract_subdictionaries(valid_jsons, self.key_mapping)

if __name__ == '__main__':
    eldorado = Eldorado()
    db_session = create_session()
    today = datetime.now().strftime("%Y-%m-%d")
    pushed_ids = get_pushed_products_id(db_session, today)

    categories = get_eldorado_categories()
    for category in categories:
        _from = 0
        _to = 49
        empty_hit = 0
        
        while True:

            data_list = eldorado.scrape(
                _from=_from,
                _to=_to,
                category=category
            ) 
            
            if empty_hit == 2:
                print("Hitting dead end for category: ", category)
                break
            if data_list == []:
                empty_hit = empty_hit + 1
                continue
            
            for d in data_list:
                d.update({'DATE': today, 'SMK_NAME':'Eldorado'})
                product = get_or_create_product(d, db_session)
                
                if product.ID in pushed_ids:
                    print(f"Product: {product.PROD_NAME} already pushed today to DB with Primary Key: {product.ID}")
                    continue
                else:
                    price = create_price_object(d, PROD_FK=product.ID)
                    db_session.add(price)
                    pushed_ids.append(product.ID)

            db_session.commit()
            _from = _from + 49
            _to = _to + 49

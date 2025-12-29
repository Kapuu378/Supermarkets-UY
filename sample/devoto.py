
from context import *
from datetime import datetime

from utils.database import Prices, Products, create_session, get_or_create_product
from sample.devoto_categories import get_categories
from sample.core import VtexBaseScrapper

KEY_MAPPING = {
    "productId": "PROD_ID",
    "productName": "PROD_NAME",
    "brand": "BRAND",
    "linkText": "LK_TEXT",
    "FullSellingPrice": "UNIT_P",
    "Price": "FULL_P",
    "PriceWithoutDiscount": "FULL_P_ND",
}

class Devoto(VtexBaseScrapper):
    def __init__(self):
        super().__init__(base_url='https://www.devoto.com.uy/api/catalog_system/pub/products/search?')
        self.path_to_schema = os.path.join(ROOT_PATH, "utils/devoto_schema.json")
        self.key_mapping = {
        'PROD_ID':['productId'],
        'PROD_NAME':['productName'],
        'BRAND':['brand'],
        'LK_TEXT':['linkText'],
        'UNIT_P':['items', 0, 'sellers', 0, 'commertialOffer', 'FullSellingPrice'],
        'FULL_P':['items', 0, 'sellers', 0, 'commertialOffer', 'Price'],
        'FULL_P_ND':['items', 0, 'sellers', 0, 'commertialOffer', 'PriceWithoutDiscount'],
        }

    def scrape(self, _from, _to, category):
        params = {
            "_from":_from,
            "_to":_to,
            "fq":f"C:{category}",
            "hideUnavailableItems":"true",
            "sc":"1"
        }
        response = self._fetch(params)

        # After parsing we expect a list that contains dicts since the json is an array of jsons.
        parsed_json_list = self._parse(response)
        valid_jsons = [json for json in parsed_json_list if self._validate_json(json, self.path_to_schema)]

        data_list = []
        for json in valid_jsons:
            subdict = self._extract_subdict(json, self.key_mapping)
            if subdict is not {}:
                data_list.append(subdict)

        return data_list

if __name__ == '__main__':
    devoto = Devoto()
    db_session = create_session()
    db_session.info["_pushed_product_ids"] = []
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Here we grab the list of the products that were already inserted in the DB today. 
    # We load those into memory for quick validating.
    db_session.info["_pushed_product_ids"].extend(
        [int(price.PROD_FK) for price in 
        db_session.query(Prices.PROD_FK).filter(Prices.DATE==today).all()])
    
    # Category ID's:
    categories = get_categories()
    for category in categories:
        _from = 0
        _to = 49
        empty_hit = 0
        
        while _from < 2500:
            data_list = devoto.scrape(
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
                d.update({'DATE': today, 'SMK_NAME':'Devoto'})
                product = Products(**{k:v for k,v in d.items() if k in Products.__table__.columns})
                product = get_or_create_product(product, db_session)
                
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

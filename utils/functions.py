from json import JSONDecodeError
from pathlib import Path
from typing import Union
from datetime import datetime

from sqlalchemy.orm import Session
import requests

from utils.validate import validate_json_schema
from utils.database import Prices, Products, create_session

def get_valid_jsons(json: dict | list[dict], schema: Path) -> list[dict]:
        """
        Returns valid jsons in a list based on a jsonschema.
        If none of the jsons in the list are valid it returns an empty list.
        """
        return [j for j in json if validate_json_schema(j, schema)]

def extract_subdictionary(dictionary: dict, key_mapping: dict) -> dict | None:
    """
    Returns a list of sub-dictionaries based on a key_mapping
    
    :param key_mapping: example: {'new_name_for_key':[path/to/value/in/dict]}    
    :param dictionary: dict
    """
    subdict = {}
    for key, value in key_mapping.items():
        current = dictionary
        for v in value:
            try:
                current = current[v]
            except KeyError:
                print("Error during creation of subdict. Some key in mapping was not found. ", value)
                return None
        subdict.update({key: current})
    return subdict

def extract_subdictionaries(dict_list: list[dict], key_mapping: dict) -> list[dict]:
    result = []
    for d in dict_list:
        subdict = extract_subdictionary(d, key_mapping)
        if subdict:
            result.append(subdict)
    return result

def create_product_object(dictionary: dict, **kwargs) -> Products:
    return Products(
        **{k:v for k,v in dictionary.items() if k in Products.__table__.columns},
        **kwargs)

def create_price_object(dictionary: dict, **kwargs) -> Prices:
    return Prices(
        **{k:v for k,v in dictionary.items() if k in Prices.__table__.columns},
        **kwargs)

def get_or_create_product(dictionary: dict, db_session: Session) -> Products:
    try:
        prod_id = dictionary["PROD_ID"]
        smk_name = dictionary["SMK_NAME"]
    except KeyError as e:
        raise ValueError(f"Missing required key: {e.args[0]}")

    product = (
        db_session
        .query(Products)
        .filter_by(PROD_ID=prod_id, SMK_NAME=smk_name)
        .one_or_none()
    )

    if product is not None:
        return product

    product = create_product_object(dictionary)
    db_session.add(product)
    db_session.flush()

    return product

def get_pushed_products_id(db_session: Session, date: Union[str, datetime]):
    """
    Returns a list with IDs from products that were already pushed in the specified date.
    
    :param db_session: Database session object.
    :type db_session: Session
    :param date: Date
    :type date: Union[str, datetime]
    """
    return [price.PROD_FK 
    for price in 
    db_session.query(Prices.PROD_FK).filter(Prices.DATE==date).all()]

def is_json_parseable(response: requests.Response)-> bool:
    try:
        response.json()
        return True
    except JSONDecodeError:
        return False
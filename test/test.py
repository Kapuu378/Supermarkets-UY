from context import *
from utils.database import Products
from sqlalchemy import inspect

p = Products(
    PROD_UI  = "SDSF",
    PROD_ID = 30,
    CLUS_ID = 32234
)

def to_dict(obj):
    return {
        attr.key: getattr(obj, attr.key)
        for attr in inspect(obj).mapper.column_attrs
    }
toprint = to_dict(p)
print(toprint)
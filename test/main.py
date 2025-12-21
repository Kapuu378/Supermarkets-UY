from context import *
from sample.devoto import Devoto
from utils.database import Prices, Products, create_session
import os

db_session = create_session()

devoto = Devoto(
    path_to_clusters=os.path.join(ROOT_PATH, "utils/devoto_cluster_ids.plk"),
    base_url="https://www.devoto.com.uy/api/catalog_system/pub/products/search?&_from=0&_to=49&fq=productClusterIds:"
)

devoto.fetch_products(limit_clusters=1)
devoto.remove_duplicates(subset=['PROD_ID'])
devoto.merge_orm_objects(session=db_session, table=Products)
devoto.add_orm_objects(session=db_session, table=Prices, if_not_exists=True, match=['PROD_UI', 'DATE'])


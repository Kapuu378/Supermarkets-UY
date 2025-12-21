from context import *
from sample.devoto import Devoto
from utils.database import Prices, Products, create_session
import os

db_session = create_session()

devoto = Devoto(
    path_to_clusters=os.path.join(ROOT_PATH, "utils/devoto_cluster_ids.plk"),
    base_url="https://www.devoto.com.uy/api/catalog_system/pub/products/search?&_from=0&_to=49&fq=productClusterIds:"
)

block = 10
for index, cluster_id in enumerate(devoto.cluster_ids):
    if index % block == 0:
        devoto.remove_duplicates(subset=['PROD_ID'])
        devoto.merge_orm_objects(session=db_session, table=Products)
        devoto.add_orm_objects(session=db_session, table=Prices, if_not_exists=True, match=['PROD_UI', 'DATE'])
        devoto.container = []
        db_session.commit()
    devoto.fetch_product(cluster_id=cluster_id)


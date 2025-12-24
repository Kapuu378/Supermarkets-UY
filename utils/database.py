from context import *
import os

from sqlalchemy import create_engine, ForeignKey, Integer, String, Column
from sqlalchemy.types import DATETIME
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv

class Base(DeclarativeBase):
	pass

class Prices(Base):
	__tablename__ = "Prices"
	UNIT_P = Column(Integer)
	FULL_P = Column(Integer)
	FULL_P_ND = Column(Integer)
	# Compound primary key
	PROD_UI = Column(String, ForeignKey("Products.PROD_UI"),  primary_key=True)
	DATE = Column(DATETIME, primary_key=True)

	def __repr__(self):
		return (
			f"<Prices("
            f"PROD_UI_FK={self.PROD_UI}, "
			f"DATE={self.DATE}, "
			f"UNIT_P={self.UNIT_P}, "
			f"FULL_P={self.FULL_P},"
			f"FULL_P_ND={self.FULL_P_ND}"
			f")>"
		)
    
class Products(Base):
	__tablename__ = "Products"
	PROD_UI = Column(String, primary_key=True)
	PROD_ID = Column(Integer)
	CLUS_ID = Column(Integer)
	PROD_NAME = Column(String)
	BRAND = Column(String)
	LK_TEXT = Column(String)
	SMK_NAME = Column(String)

	def __repr__(self):
		return (
			f"<Products("
            f"PROD_UI={self.PROD_UI}, " 
			f"PROD_ID={self.PROD_ID}, "
			f"CLUS_ID={self.CLUS_ID}, "
			f"PROD_NAME={self.PROD_NAME}, "
			f"BRAND={self.BRAND}"
			f")>"
		)

def merge_orm_objects(data_list, session, table):
	if not issubclass(table, Base):
		raise TypeError("param: base should be an instance of Base mysqlalchemy class.")

	for data in data_list:
		object = table(**{k:v for k,v in data.items() if k in table.__table__.columns})
		session.merge(object)
	return None

def create_session():
	load_dotenv(
		dotenv_path=os.path.join(
		ROOT_PATH, 'utils/sql_credentials.env')
	)
	USERNAME = os.getenv('USERNAME')
	PASSWORD = os.getenv('PASSWORD')

	engine = create_engine(f"mysql://{USERNAME}:{PASSWORD}@FranciscoGibert.mysql.pythonanywhere-services.com/FranciscoGibert$default")
	Session = sessionmaker(bind=engine)
	session = Session()
	return session
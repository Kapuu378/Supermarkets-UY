from context import *
from dotenv import load_dotenv
import os

from typing import List
from typing import Optional
from sqlalchemy import create_engine, ForeignKey, select, and_, Integer, String, Float, Column
from sqlalchemy.types import DATETIME
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import NoResultFound

def create_session():
	load_dotenv(
		dotenv_path=os.path.join(
		ROOT_PATH, 'utils/sql_credentials.env'))
	USERNAME = os.getenv('USERNAME')
	PASSWORD = os.getenv('PASSWORD')

	engine = create_engine(f"mysql://{USERNAME}:{PASSWORD}@FranciscoGibert.mysql.pythonanywhere-services.com/FranciscoGibert$default")
	Session = sessionmaker(bind=engine)
	session = Session()
	return session

class Base(DeclarativeBase):
	pass

class Prices(Base):
	__tablename__ = "Prices"
	ID_PK = Column(Integer, primary_key=True)
	UNIT_P = Column(Integer)
	FULL_P = Column(Integer)
	FULL_P_ND = Column(Integer)
	PROD_UI = Column(String, ForeignKey("Products.PROD_UI"))
	DATE = Column(DATETIME)

	def __repr__(self):
		return (
			f"<Prices("
			f"ID_PK={self.ID_PK}, "
            f"PROD_UI_FK={self.PROD_UI_FK}, "
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

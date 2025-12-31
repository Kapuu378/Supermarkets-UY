from context import *

from sqlalchemy import create_engine, ForeignKey, Integer, String, Column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv

class Base(DeclarativeBase):
	pass

class Prices(Base):
	__tablename__ = "Prices"
	ID = Column(Integer, primary_key=True, autoincrement=True)
	UNIT_P = Column(Integer)
	FULL_P = Column(Integer)
	FULL_P_ND = Column(Integer)
	DATE = Column(String(100))

	PROD_FK = Column(String, ForeignKey("Products.ID"))

	def __repr__(self):
		return (
			f"<Prices("
            f"ID={self.ID}, "
			f"DATE={self.DATE}, "
			f"UNIT_P={self.UNIT_P}, "
			f"FULL_P={self.FULL_P},"
			f"FULL_P_ND={self.FULL_P_ND}",
			f"PROD_FK={self.PROD_FK}"
			f")>"
		)

class Products(Base):
	__tablename__ = "Products"
	ID = Column(Integer, primary_key=True, autoincrement=True)
	PROD_ID = Column(Integer)
	PROD_NAME = Column(String(100))
	BRAND = Column(String(50))
	LK_TEXT = Column(String(100))
	SMK_NAME = Column(String(50))

	def __repr__(self):
		return (
			f"<Products("
            f"ID={self.ID}, "
			f"PROD_ID={self.PROD_ID}, "
			f"PROD_NAME={self.PROD_NAME}, "
			f"BRAND={self.BRAND}"
			f")>"
		)

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
	Base.metadata.create_all(bind=engine)
	return session
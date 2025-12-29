from context import *

from sqlalchemy import create_engine, ForeignKey, Integer, String, Column
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker, Session

class Base(DeclarativeBase):
	pass

class Prices(Base):
	# I will create an index on date and prod_fk
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
	engine = create_engine(f"sqlite:///supermarkets.db")
	Session = sessionmaker(bind=engine)
	session = Session()
	Base.metadata.create_all(bind=engine)
	return session

def get_or_create_product(product, db_session: Session) -> Products:
	try:
		product = db_session.query(Products).filter_by(
			PROD_ID=product.PROD_ID,
			SMK_NAME=product.SMK_NAME).one()

	except NoResultFound:
		db_session.add(product)
		db_session.flush()

	except KeyError:
		print(f"Key error in data: {product}. Either PROD_ID or SMK_NAME it's missing.")

	finally:
		return product
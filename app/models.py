from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Date
from database import Base
from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base




Base = declarative_base()


class Sales(Base):
    __tablename__ = 'sales'

    sales_id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, index=True)
    quantity_sold = Column(Integer)
    sale_date = Column(Date)



    

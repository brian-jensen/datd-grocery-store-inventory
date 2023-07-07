from sqlalchemy import Integer, String, Date, ForeignKey
from sqlalchemy.orm import DeclarativeBase, mapped_column


class Base(DeclarativeBase):
    pass


class Brand(Base):
    __tablename__ = 'brands'
    brand_id = mapped_column(Integer, primary_key=True)
    brand_name = mapped_column(String)


class Product(Base):
    __tablename__ = 'products'
    product_id = mapped_column(Integer, primary_key=True)
    product_name = mapped_column(String)
    product_quantity = mapped_column(Integer)
    product_price = mapped_column(Integer)
    date_updated = mapped_column(Date)
    brand_id = mapped_column(Integer, ForeignKey('brands.brand_id'))

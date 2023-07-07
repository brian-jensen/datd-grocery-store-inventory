from datetime import datetime

from db.database import Session
from db.models import Brand, Product
from data import brands_csv, inventory_csv
from helpers import clean_price, clean_date

session = Session()


def add_brands():
    for row in brands_csv:
        brand_in_db = session.query(Brand).filter_by(brand_name=row[0]).first()
        if not brand_in_db:
            session.add(Brand(brand_name=row[0]))
    session.commit()


def add_products():
    for row in inventory_csv:
        product_in_db = session.query(Product).filter(
            Product.product_name == row[0]).one_or_none()
        if product_in_db:
            print(f'Product {row[0]} already exists')
        else:
            name = row[0]
            price = clean_price(row[1])
            quantity = row[2]
            date = clean_date(row[3], datetime)
            brand = row[4]
            brand_lookup = session.query(Brand).filter_by(
                brand_name=brand).first()
            if brand_lookup:
                brand_id = brand_lookup.brand_id
                print(name, price, quantity, date, brand, brand_id)


if __name__ == '__main__':
    add_brands()
    add_products()

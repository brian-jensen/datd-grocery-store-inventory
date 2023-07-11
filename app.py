from datetime import datetime

from db.database import engine, Session
from db.models import Base, Brand, Product
from data import brands_csv, inventory_csv
from helpers import (clean_price, clean_date,
                     clean_quantity, view_product, cls)

session = Session()


def add_brands():
    for row in brands_csv:
        brand_in_db = session.query(Brand).filter_by(brand_name=row[0]).first()
        if not brand_in_db:
            session.add(Brand(brand_name=row[0]))
    session.commit()


def add_products():
    brand_id = None
    for row in inventory_csv:
        product_in_db = session.query(Product).filter(
            Product.product_name == row[0]).one_or_none()
        if product_in_db:
            if product_in_db.date_updated < clean_date(row[3], datetime):
                product_in_db.product_price = clean_price(row[1])
                product_in_db.product_quantity = clean_quantity(row[2])
                product_in_db.date_updated = clean_date(row[3], datetime)
        else:
            name = row[0]
            price = clean_price(row[1])
            quantity = clean_quantity(row[2])
            date = clean_date(row[3], datetime)
            brand = row[4]
            brand_lookup = session.query(Brand).filter_by(
                brand_name=brand).first()
            if brand_lookup:
                brand_id = brand_lookup.brand_id
            product = Product(product_name=name, product_price=price,
                              product_quantity=quantity, date_updated=date,
                              brand_id=brand_id)
            session.add(product)
    session.commit()


def main_menu():
    cls()
    print('''
    \rPlease select one of the following options:\n
    \r V - View a single product's inventory
    \r N - Add a new product to the database
    \r A - View an analysis of the inventory
    \r B - Make a backup of the entire inventory
    \r Q - Quit
    ''')
    user_input = input('Enter your choice: ').lower()
    if user_input == 'v':
        view_product(session, Product, Brand, main_menu)
    elif user_input == 'n':
        print('Add a new product')
    elif user_input == 'a':
        print('View an analysis')
    elif user_input == 'b':
        print('Make a backup')
    elif user_input == 'q':
        print('Goodbye!')
    else:
        print(f'\n{user_input} is not a valid option. Please try again.')
        main_menu()


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
    add_brands()
    add_products()
    main_menu()

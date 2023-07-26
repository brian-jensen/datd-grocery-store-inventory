from datetime import datetime

from db.database import engine, Session, inspect
from db.models import Base, Brand, Product
from data import brands_csv, inventory_csv
from helpers import (clean_price, clean_date,
                     clean_quantity, search_products,
                     add_product, analyze_data, cls)

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
    \r Q - Quit the application
    ''')
    while True:
        user_input = input('Enter your choice: ').lower()
        match user_input:
            case 'v':
                cls()
                search_products(session, Product, Brand, main_menu)
                break
            case 'n':
                cls()
                add_product(session, Product, Brand, main_menu, datetime)
                break
            case 'a':
                cls()
                analyze_data(session, Product, Brand, main_menu)
                break
            case 'b':
                print('Make a backup')
                break
            case 'q':
                print('Goodbye!')
                break
            case _:
                print(f'{user_input} was not a valid option.\n')


if __name__ == '__main__':
    if inspect(engine).get_table_names() == []:
        Base.metadata.create_all(bind=engine)
        add_brands()
        add_products()
    main_menu()

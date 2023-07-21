from helpers import clean_price, clean_quantity


PRODUCT_NAME_PROMPT = 'Enter the product name: '
PRODUCT_QUANTITY_PROMPT = 'Enter the product quantity: '
PRODUCT_PRICE_PROMPT = 'Enter the product price (ex. 10.99): '
PRODUCT_BRAND_PROMPT = 'Enter the product brand: '


def add_product(session, product_model, brand_model, main_menu, datetime):
    print('\n- Add a new product to the database -\n')
    product_name = input(PRODUCT_NAME_PROMPT)
    product_quantity = input(PRODUCT_QUANTITY_PROMPT)
    while not product_quantity.replace(',', '').isdigit():
        print('Please enter a valid quantity (whole numbers only)')
        product_quantity = input(PRODUCT_QUANTITY_PROMPT)
    product_price = input(PRODUCT_PRICE_PROMPT)
    while not product_price.replace('$', '').replace('.', '').isdigit():
        print('Please enter a valid price.')
        product_price = input(PRODUCT_PRICE_PROMPT)
    product_brand = input(PRODUCT_BRAND_PROMPT)
    try:
        product_in_db = session.query(product_model).filter(
            product_model.product_name == product_name).one_or_none()
        brand_in_db = session.query(brand_model).filter(
            brand_model.brand_name.ilike(product_brand)).one_or_none()
        if product_in_db and brand_in_db:
            product_in_db.product_price = clean_price(product_price)
            product_in_db.product_quantity = clean_quantity(
                product_quantity)
            product_in_db.date_updated = datetime.now()
            product_in_db.brand_id = brand_in_db.id
            session.commit()
            print(
                f'\n{product_in_db.product_name} was updated successfully!')
        else:
            product = product_model(
                product_name=product_name,
                product_quantity=clean_quantity(product_quantity),
                product_price=clean_price(product_price),
                date_updated=datetime.now())
            if brand_in_db:
                product.brand_id = brand_in_db.brand_id
            else:
                brand = brand_model(brand_name=product_brand)
                session.add(brand)
                session.commit()
                product.brand_id = brand.brand_id
            session.add(product)
            session.commit()
            print(f'\n{product_name} was added successfully!')
            input('\nPress ENTER to return to the main menu...')
            main_menu()
    except ValueError:
        print('\nThere was an error adding the product, please try again.')
        add_product(session, product_model, brand_model, main_menu, datetime)

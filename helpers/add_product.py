from helpers import clean_price, clean_quantity, edit_product


PRODUCT_NAME_PROMPT = 'Enter the product name: '
PRODUCT_QUANTITY_PROMPT = 'Enter the product quantity: '
PRODUCT_PRICE_PROMPT = 'Enter the product price (ex. 10.99): '
PRODUCT_BRAND_PROMPT = 'Enter the product brand: '


def add_product(session, product_model, brand_model, main_menu, datetime):
    print('\n- Add a new product to the database -\n')
    product_name = input(PRODUCT_NAME_PROMPT)
    product_in_db = session.query(product_model).filter(
        product_model.product_name == product_name).one_or_none()
    if product_in_db:
        print(f"\n{product_name} is already in the database.")
        print(f'''
              \r  1 - Edit "{product_name}" instead.
              \r  2 - Enter a new product name.
              \r  3 - Return to the main menu''')
        choice = input('\nEnter your choice: ')
        if choice == '1':
            usd_price = float(product_in_db.product_price / 100)
            edit_product(session, product_in_db,
                         usd_price, main_menu)
        elif choice == '2':
            add_product(session, product_model,
                        brand_model, main_menu, datetime)
    else:
        product_quantity = input(PRODUCT_QUANTITY_PROMPT)
        while not product_quantity.replace(',', '').isdigit():
            print('Please enter a valid quantity (whole numbers only)')
            product_quantity = input(PRODUCT_QUANTITY_PROMPT)
        product_price = input(PRODUCT_PRICE_PROMPT)
        while not product_price.replace('$', '').replace('.', '').isdigit():
            print('Please enter a valid price.')
            product_price = input(PRODUCT_PRICE_PROMPT)
        product_brand = input(PRODUCT_BRAND_PROMPT)
        product = product_model(
            product_name=product_name,
            product_quantity=clean_quantity(product_quantity),
            product_price=clean_price(product_price),
            date_updated=datetime.now())
        brand_in_db = session.query(brand_model).filter(
            brand_model.brand_name.ilike(product_brand)).one_or_none()
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

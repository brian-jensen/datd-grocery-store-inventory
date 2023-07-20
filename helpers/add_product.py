from helpers import clean_price, clean_quantity


def add_product(session, Product, Brand, main_menu, datetime):
    print('\n- Add a new product to the database -\n')
    product_name = input('Enter the product name: ')
    product_quantity = input('Enter the product quantity: ')
    product_price = input('Enter the product price (ex. 10.99): ')
    product_brand = input('Enter the product brand: ')
    while not product_quantity.replace(',', '').isdigit():
        print('Please enter a valid quantity (whole numbers only)')
        product_quantity = input('Enter the product quantity: ')
    product_price = input('Enter the product price (ex. 10.99): ')
    while not product_price.replace('$', '').replace('.', '').isdigit():
        print('Please enter a valid price.')
        product_price = input('Enter the product price (ex. 10.99): ')
    try:
        product_in_db = session.query(Product).filter(
            Product.product_name == product_name).one_or_none()
        if product_in_db:
            product_in_db.product_price = clean_price(product_price)
            product_in_db.product_quantity = clean_quantity(
                product_quantity)
            product_in_db.date_updated = datetime.now()
            session.commit()
            print(
                f'\n{product_in_db.product_name} was updated successfully!')
        else:
            product = Product(
                product_name=product_name,
                product_quantity=clean_quantity(product_quantity),
                product_price=clean_price(product_price),
                date_updated=datetime.now())
            session.add(product)
            session.commit()
            print(f'\n{product_name} was added successfully!')
    except ValueError:
        print('\nThere was an error adding the product, please try again.')
        add_product(session, Product, Brand, main_menu, datetime)

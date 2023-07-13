from helpers.delete_product import delete_product
from helpers.edit_product import edit_product


def view_product(session, product_model, brand_model, menu):
    print('\n- View a single product\'s inventory -\n')
    while True:
        product_id = input('Enter the product ID: ')
        product = session.query(product_model).filter(
            product_model.product_id == product_id).one_or_none()
        if product:
            brand = session.query(brand_model).filter(
                brand_model.brand_id == product.brand_id).one_or_none()
            usa_date = product.date_updated.strftime('%B %d, %Y')
            usd_price = float(product.product_price / 100)
            border = '-' * 50
            print(f'''
                \r {border}
                \r Product Name: {product.product_name}
                \r Product Price: ${usd_price:.2f}
                \r Product Quantity: {product.product_quantity}
                \r Date Updated: {usa_date}
                \r Brand: {brand.brand_name}
                \r {border}
            ''')
            break
        else:
            print(f'Product ID {product_id} not found.\n')
    print('''
      \r e - Edit this product
      \r d - Delete this product
      \r q - Return to the main menu
    \n''')
    while True:
        user_input = input('Enter your choice: ').lower()
        if user_input == 'e':
            edit_product(session, product, usd_price, menu)
            break
        elif user_input == 'd':
            delete_product(session, product, menu)
        elif user_input == 'q':
            menu()
            break
        else:
            print(f'{user_input} is not a valid option.\n')

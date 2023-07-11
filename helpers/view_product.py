def view_product(session, product_model, brand_model, menu):
    while True:
        product_id = input('\nEnter the product ID: ')
        product = session.query(product_model).filter(
            product_model.product_id == product_id).one_or_none()
        if product:
            brand = session.query(brand_model).filter(
                brand_model.brand_id == product.brand_id).one_or_none()
            usa_date = product.date_updated.strftime('%B %d, %Y')
            usd_price = float(product.product_price / 100)
            print(f'''
            \r Product Name: {product.product_name}
            \r Product Price: ${usd_price:.2f}
            \r Product Quantity: {product.product_quantity}
            \r Date Updated: {usa_date}
            \r Brand: {brand.brand_name}
            ''')
            break
        else:
            print(f'\nProduct ID {product_id} not found.')
    print('\nPress ENTER to continue...')
    input()
    menu()

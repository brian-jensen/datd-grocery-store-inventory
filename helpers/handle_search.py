from helpers.view_product import view_product


def handle_search(session, product_model, brand_model, menu):
    while True:
        search = input('Enter the product name (e.g. "beans"): ')
        name_search = session.query(product_model).filter(
            product_model.product_name.ilike(f'%{search}%')).all()
        if name_search:
            if len(name_search) == 1:
                print()
                view_product(session, product_model, brand_model,
                             menu, name_search[0].product_id)
                break
            elif len(name_search) > 1:
                print(f'\nFound {len(name_search)} results for "{search}":\n')
                for product in name_search:
                    border = '-' * 50
                    print(f'''
                  \r {border}
                  \r Product Name: {product.product_name}
                  \r Product ID: {product.product_id}
                  \r {border}''')
                view_product(session, product_model,
                             brand_model, menu, None)
                break
        else:
            print(f'No results found for "{search}".\n')

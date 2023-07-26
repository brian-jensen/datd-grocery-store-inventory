from sqlalchemy import func

BORDER = '-' * 35


def analyze_data(session, product, brand, menu):
    print('- Inventory Analysis -\n')

    most_expensive = session.query(product).order_by(
        product.product_price.desc()).first()
    m_e_name = most_expensive.product_name
    m_e_price = round(most_expensive.product_price / 100, 2)
    print(f'''
        \rMOST EXPENSIVE PRODUCT
        \r{BORDER}
        \r{m_e_name} ~ ${m_e_price}
        ''')

    least_expensive = session.query(product).order_by(
        product.product_price).first()
    l_e_name = least_expensive.product_name
    l_e_price = round(least_expensive.product_price / 100, 2)
    print(f'''
          \rLEAST EXPENSIVE PRODUCT
          \r{BORDER}
          \r{l_e_name} ~ ${l_e_price}
          ''')

    top_brand = session.query(brand).join(
        product).group_by(brand.brand_name).order_by(
        func.count(product.product_id).desc()).first()
    t_b_name = top_brand.brand_name
    t_b_count = session.query(product).filter(
        product.brand_id == top_brand.brand_id).count()
    print(f'''
          \rTOP BRAND
          \r{BORDER}
          \r{t_b_name} ~ {t_b_count} products
          ''')

    single_product_brands = session.query(brand).outerjoin(
        product, brand.brand_id == product.brand_id
    ).group_by(
        brand.brand_id
    ).having(func.count(product.product_id) == 1).all()

    single_product_brands_string = ', '.join(
        [brand.brand_name for brand in single_product_brands])
    print(f'''
          \rSINGLE PRODUCT BRANDS
          \r{BORDER}
          \r{single_product_brands_string}
          ''')

    newest = session.query(product).order_by(
        product.date_updated.desc()).first()
    print(f'''
          \rNEWEST PRODUCT
          \r{BORDER}
          \r{newest.product_name} ~ {newest.date_updated.strftime('%B %d, %Y')}
          ''')

    input('\nPress ENTER to return to the main menu...')
    menu()

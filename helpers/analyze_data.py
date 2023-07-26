from sqlalchemy import func

BORDER = '-' * 35


def analyze_data(session, product_model, brand_model, main_menu):
    print('- Inventory Analysis -\n')

    most_expensive = session.query(product_model).order_by(
        product_model.product_price.desc()).first()
    m_e_name = most_expensive.product_name
    m_e_price = round(most_expensive.product_price / 100, 2)
    print(f'''
        \rMOST EXPENSIVE PRODUCT
        \r{BORDER}
        \r{m_e_name} ~ ${m_e_price}
        ''')

    least_expensive = session.query(product_model).order_by(
        product_model.product_price).first()
    l_e_name = least_expensive.product_name
    l_e_price = round(least_expensive.product_price / 100, 2)
    print(f'''
          \rLEAST EXPENSIVE PRODUCT
          \r{BORDER}
          \r{l_e_name} ~ ${l_e_price}
          ''')

    top_brand = session.query(brand_model).join(
        product_model).group_by(brand_model.brand_name).order_by(
        func.count(product_model.product_id).desc()).first()
    t_b_name = top_brand.brand_name
    t_b_count = session.query(product_model).filter(
        product_model.brand_id == top_brand.brand_id).count()
    print(f'''
          \rTOP BRAND
          \r{BORDER}
          \r{t_b_name} ~ {t_b_count} products
          ''')

    single_product_brands = session.query(brand_model).outerjoin(
        product_model, brand_model.brand_id == product_model.brand_id
    ).group_by(
        brand_model.brand_id
    ).having(func.count(product_model.product_id) == 1).all()

    single_product_brands_string = ', '.join(
        [brand.brand_name for brand in single_product_brands])
    print(f'''
          \rSINGLE PRODUCT BRANDS
          \r{BORDER}
          \r{single_product_brands_string}
          ''')

    newest = session.query(product_model).order_by(
        product_model.date_updated.desc()).first()
    print(f'''
          \rNEWEST PRODUCT
          \r{BORDER}
          \r{newest.product_name} ~ {newest.date_updated.strftime('%B %d, %Y')}
          ''')

    input('\nPress ENTER to return to the main menu...')
    main_menu()

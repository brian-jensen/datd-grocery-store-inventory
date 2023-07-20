from helpers.view_product import view_product
from helpers.handle_search import handle_search
from helpers.cls import cls


def search_products(session, product_model, brand_model, menu):
    print('\n- View a single product\'s inventory -\n')
    print('''
      \r 1 - Search for a product by ID to view
      \r 2 - Search for a product by name to view
    \n''')
    while True:
        user_input = input('Enter your choice: ')
        if user_input == '1':
            cls()
            view_product(session, product_model, brand_model, menu, None)
            break
        elif user_input == '2':
            handle_search(session, product_model, brand_model, menu)
            break
        else:
            print(f'{user_input} is not a valid option.\n')

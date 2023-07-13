from datetime import datetime

from helpers import clean_price, clean_quantity


def edit_product(session, product, usd_price, menu):
    print(f'\nEditing "{product.product_name}"\n')
    new_price = input(f' Enter the new price (${usd_price:.2f}): ')
    if new_price != '':
        while not new_price.replace('$', '').replace('.', '').isdigit():
            print('Please enter a valid price.')
            new_price = input(f' Enter the new price (${usd_price:.2f}): ')
    new_quantity = input(
        f' Enter the new quantity ({product.product_quantity}): ')
    if new_quantity != '':
        while not new_quantity.replace(',', '').isdigit():
            print('Please enter a valid quantity.')
            new_quantity = input(
                f' Enter the new quantity ({product.product_quantity}): ')
    if new_price:
        product.product_price = clean_price(new_price)
    if new_quantity:
        product.product_quantity = clean_quantity(new_quantity)
    if not new_price and not new_quantity:
        print('\nNo updates made.')
    else:
        product.date_updated = datetime.now()
        session.commit()
        print(f'\n"{product.product_name}" updated successfully!\n')
    input('\nPress ENTER to return to the main menu...')
    menu()

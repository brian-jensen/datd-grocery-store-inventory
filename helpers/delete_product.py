MENU_TEXT = '\nPress ENTER to return to the main menu...'


def delete_product(session, product, menu):
    while True:
        confirm = input(
            f'Delete "{product.product_name}"? (y/n): ').lower()
        if confirm == 'y':
            session.delete(product)
            session.commit()
            print(f'\n"{product.product_name}" deleted successfully!\n')
            input(MENU_TEXT)
            menu()
            break
        elif confirm == 'n':
            print('\nNo changes made.')
            input(MENU_TEXT)
            menu()
            break
        else:
            print(f'{confirm} is not a valid option.\n')

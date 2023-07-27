import csv
import os


def backup_data(session, product, brand, menu):
    with open('backup_brands.csv', 'w') as csv_file:
        brands_csv = csv.writer(csv_file)
        brands_csv.writerow(['brand_name'])
        for row in session.query(brand.brand_name).all():
            brands_csv.writerow(row)

    with open('backup_inventory.csv', 'w') as csv_file:
        inventory_csv = csv.writer(csv_file)
        inventory_csv.writerow(
            ['product_name', 'product_price',
             'product_quantity', 'date_updated',
             'brand_name'])
        for row in session.query(
                product.product_name, product.product_price,
                product.product_quantity, product.date_updated,
                brand.brand_name).join(brand).all():
            row = list(row)
            row[1] = f'${row[1] / 100:.2f}'
            row[3] = row[3].strftime(
                '%#m/%#d/%Y' if os.name == 'nt' else '%-m/%-d/%Y')
            inventory_csv.writerow(row)

    print('\nBackup complete!')
    input('\nPress ENTER to return to the main menu...')
    menu()

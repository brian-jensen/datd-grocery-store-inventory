def clean_quantity(quantity_str):
    quantity_str = quantity_str.replace(',', '')
    return int(quantity_str)

def clean_price(price_str):
    price_str = price_str.replace('$', '')
    price_float = float(price_str)
    return int(price_float * 100)

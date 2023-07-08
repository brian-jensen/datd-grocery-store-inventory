def clean_price(price_str):
    price_float = float(price_str.replace('$', '')) * 100
    return int(round(price_float))

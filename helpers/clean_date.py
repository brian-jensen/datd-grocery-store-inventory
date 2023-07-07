def clean_date(date_str, datetime):
    date_obj = datetime.strptime(date_str, '%m/%d/%Y').date()
    return date_obj

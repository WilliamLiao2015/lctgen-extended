def is_number(x):
    try: return float(x) is not None
    except ValueError: return False

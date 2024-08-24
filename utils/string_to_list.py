def string_to_list(s):
    s = s.strip('[]')
    items = s.split(',')
    items = [item.strip("' ") for item in items]
    return items

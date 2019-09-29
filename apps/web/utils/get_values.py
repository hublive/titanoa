# encoding: utf-8

def get_values(status):
    data_list = []
    for item in status:
        for key, value in item.items():
            data_list.append(value)
    return list(set(data_list))

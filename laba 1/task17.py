def func(dict1, dict2):
    result = dict1.copy()

    for key in dict2:
        if key in result and isinstance(result[key], dict) and isinstance(dict2[key], dict):
            result[key] = func(result[key], dict2[key])
        else:
            result[key] = dict2[key]

    return result


a = {"имя": "Богдан", "информация": {"возраст": 19}}
b = {"город": "Минск", "информация": {"занятость": "студент"}}

print(func(a, b))
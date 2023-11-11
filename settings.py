import json

# Ваш список со словарями
list_of_dicts = [
    {"name": "Яндекс",
     "id": 1740},
    {"name": "Авито",
     "id": 84585},
    {"name": "Росатом",
     "id": 577743},
    {"name": "Софтлайн",
     "id": 2381},
    {"name": "СБЕР",
     "id": 3529},
    {"name": "Kaspersky",
     "id": 1057},
    {"name": "АйТеко",
     "id": 115},
    {"name": "Газпром автоматизация",
     "id": 903111},
    {"name": "Айтеко Технолоджи",
     "id": 4167790},
    {"name": "ИКС Холдинг",
     "id": 16206}
]

# Преобразование списка словарей в кортеж с кортежами
tuple_of_tuples = tuple(tuple(d.values()) for d in list_of_dicts)

# Вывод результата
print(tuple_of_tuples)
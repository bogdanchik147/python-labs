products = [
    {"name": "Телефон Samsung Galaxy S25Ultra", "price": 20000, "quantity": 5},
    {"name": "Ноутбук", "price": 50000, "quantity": 3},
    {"name": "Телефон Samsung Galaxy S25", "price": 20000, "quantity": 2},
    {"name": "Наушники", "price": 3000, "quantity": 10}
]

doxod = {}

for product in products:
    name = product["name"]
    total = product["price"] * product["quantity"]

    if name in doxod:
        doxod[name] = doxod[name] + total
    else:
        doxod[name] = total

print("Выручка по товарам:")

for name in doxod:
    print(name, "-", doxod[name], "руб.")

best = max(doxod, key=doxod.get)

print("Самый прибыльный товар:", best)

# Количество уникальных товаров
print("Количество уникальных товаров:", len(doxod))
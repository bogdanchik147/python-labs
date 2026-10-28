print("Тип измерения:")
print("1 - Длина")
print("2 - Масса")
print("3 - Температура")
print("4 - Время")

choice = input("Выберите тип: ")

if choice == "1":
    A = {
        "м": 1,
        "км": 1000,
        "см": 0.01,
        "мм": 0.001
    }

elif choice == "2":
    A = {
        "кг": 1,
        "г": 0.001,
        "т": 1000
    }

elif choice == "3":
    A = {
        "C": 1,
        "F": 2
    }

elif choice == "4":
    A = {
        "сек": 1,
        "мин": 60,
        "ч": 3600
    }

else:
    print("Неправильный выбор")
    exit()

print("Доступные единицы:", ", ".join(A.keys()))

source = input("Из какой хочешь: ")
target = input("В какую хочешь: ")
value = float(input("Введите значение: "))

if source not in A or target not in A:
    print("Неверная единица измерения")

elif choice == "3":
    if source == "C" and target == "F":
        result = value * 1.8 + 32
    elif source == "F" and target == "C":
        result = (value - 32) * 1.8
    else:
        result = value

    print(f"Результат: {result:.2f} {target}")

else:
    result = value * A[source] / A[target]

    print(f"Результат: {result:.2f} {target}")
numbers = list(map(float, input("Введите числа: ").split()))

unique = []

for number in numbers:
    if numbers.count(number) == 1:
        unique.append(number)

print("Уникальные числа:", unique)

repeat = []

for number in numbers:
    if numbers.count(number) > 1 and number not in repeat:
        repeat.append(number)

print("Повторяющиеся числа:", repeat)

even = []
odd = []

for number in numbers:
    if number.is_integer():
        if number % 2 == 0:
            even.append(number)
        else:
            odd.append(number)

print("Четные числа:", even)
print("Нечетные числа:", odd)

negative = []

for number in numbers:
    if number < 0:
        negative.append(number)

print("Отрицательные числа:", negative)

floatnum = []

for number in numbers:
    if not number.is_integer():
        floatnum.append(number)

print("Числа с плавающей точкой:", floatnum)

total = 0

for number in numbers:
    if number % 5 == 0:
        total = total + number

print("Сумма чисел, кратных 5:", total)

print("Самое большое число:", max(numbers))

print("Самое маленькое число:", min(numbers))
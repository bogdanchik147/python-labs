a = float(input("Введите первое число: "))
b = float(input("Введите второе число: "))

print("Сумма:", a + b)
print("Разность:", a - b)
print("Произведение:", a * b)
print("Степень:", a ** b)

if b != 0:
    print("Деление:", a / b)
    print("Остаток:", a % b)
else:
    print("На ноль делить нельзя")
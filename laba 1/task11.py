age = int(input("Введите возраст заемщика: "))
if age <=18:
    print("Надо быть совершенно летним, чтобы получить кредит")
    exit()
income = float(input("Введите ежемесячный доход: "))
loan = float(input("Введите сумму кредита: "))
months = int(input("Введите срок кредита в месяцах: "))

history = input("Введите кредитную историю (отличная/хорошая/удовлетворительная/плохая): ")
guarantor = input("Есть ли поручитель? (да/нет): ")
collateral = input("Есть ли залог? (да/нет): ")

soot = loan / income

print(f"\nСоотношение кредита к доходу: {soot:.2f}")

if months <= 12:
    risksoot = soot
elif months <= 36:
    risksoot = soot + 5
else:
    risksoot = soot + 10

if history == "отличная" and risksoot <= 10:
    risk = "низкий"
    rate = 8

elif history == "хорошая" and risksoot <= 20:
    risk = "средний"
    rate = 12

elif history == "плохая" or risksoot > 30:
    risk = "критический"
    rate = 25

else:
    risk = "высокий"
    rate = 18

if guarantor == "да":
    rate = rate - 1

if collateral == "да":
    rate = rate - 2

print(f"Категория риска: {risk}")
print(f"Процентная ставка: {rate}%")

if risk == "низкий" or risk == "средний":
    print("Кредит можно одобрить")

elif risk == "высокий":
    print("Требуется дополнительные проверки")

else:
    print("Кредит рекомендуется отклонить")
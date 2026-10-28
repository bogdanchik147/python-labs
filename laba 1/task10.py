price = float(input("Сумма покупки: "))
age = int(input("Ваш возраст: "))
birthday = input("Сегодня ваш день рождения? (да/нет): ")
vip = input("Вы VIP-клиент? (да/нет): ")

discount = 0

if price > 1000:
    discount = discount + 10

if age >= 63:
    discount = discount + 5

if birthday == "да":
    discount = discount + 5

if vip == "да" :
    discount =  max(discount, 15)

if discount > 25:
    discount = 25

finalprice = price * (100 - discount) / 100

print("Скидка:", discount, "%")
print("Итоговая цена:", round(finalprice, 2))
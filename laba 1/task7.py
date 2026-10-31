start = 24.99

minutes = int(input("Введите количество минут: "))
sms = int(input("Введите количество SMS: "))
internet = float(input("Введите интернет трафик в МБ: "))

extramin = 0
extrasms = 0
extrainternet = 0

if minutes > 60:
    extramin = (minutes - 60) * 0.89

if sms > 30:
    extrasms = (sms - 30) * 0.59

if internet > 1024:
    extrainternet = (internet - 1024) * 0.79

total = start + extramin + extrasms + extrainternet

nalog = total * 0.02

final = total + nalog

print(f"\nБазовая сумма: {start:.2f} руб.")

if extramin > 0:
    print(f"Дополнительные минуты: {extramin:.2f} руб.")

if extrasms > 0:
    print(f"Дополнительные SMS: {extrasms:.2f} руб.")

if extrainternet > 0:
    print(f"Дополнительный интернет: {extrainternet:.2f} руб.")

print(f"Налог 2%: {nalog:.2f} руб.")
print(f"Итоговая сумма: {final:.2f} руб.")
cash = int(input("Введите сумму: "))

for coin in [100, 50, 10, 5, 2, 1]:
    count = cash // coin
    money = cash % coin
    print(coin,"по", count)
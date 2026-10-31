def financial_assistant():
    income = {}
    expenses = {}

    count = int(input("Сколько источников дохода? "))

    for i in range(count):
        category = input("Источник дохода (например: зарплата): ")
        summa = float(input("Сумма дохода: "))
        income[category] = income.get(category, 0) + summa

    count = int(input("Сколько источников расходов? "))

    for i in range(count):
        category = input("Источник расхода (жильё, питание, транспорт и т.д.): ")
        summa = float(input("Сумма расхода: "))
        expenses[category] = expenses.get(category, 0) + summa

    totalincome = sum(income.values())
    totalexpenses = sum(expenses.values())
    balance = totalincome - totalexpenses

    print(f"Общий доход: {totalincome:.2f} руб.")
    print(f"Общие расходы: {totalexpenses:.2f} руб.")
    print(f"Остаток средств: {balance:.2f} руб.")

    print("\nДоходы:")
    for category, amount in income.items():
        print(f"{category}: {amount:.2f} руб.")

    print("\nРасходы:")
    for category, amount in expenses.items():
        print(f"{category}: {amount:.2f} руб.")

    print("\nРекомендации:")

    if totalincome > 0:
        rate = balance / totalincome * 100
        print(f"Доля оставшихся средств: {rate:.1f}%")

        if balance < 0:
            print("Расходы превышают доходы")
            print("Просмотри необязательные покупки")
        elif balance == 0:
            print("Отложить нечего, попробуй сократить необязательные расходы")
        else:
            print(f"Можно отложить (20% от остатка): {balance * 0.2:.2f} руб.")

    if totalexpenses > 0:
        for category, amount in expenses.items():
            share = amount / totalexpenses * 100
            print(f"{category}: {share:.1f}% всех расходов")

            if share > 30:
                print(f"Рекомендация: посмотри, можно ли сократить расходы на {category}.")

    print("\nРасчет крупной покупки")
    goal = input("Введите название цели: ")
    goalsum = float(input("Сколько денег нужно накопить? "))

    saving = float(input("Сколько планируете откладывать в месяц? "))

    if saving > 0:
        months = goalsum / saving
        print(f"Цель {goal}: потребуется примерно {months:.1f} месяца.")

financial_assistant()
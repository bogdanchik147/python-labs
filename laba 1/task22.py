def type_check(*types):
    def decorator(func):
        def wrapper(*args):
            for i in range(len(args)):
                if not isinstance(args[i], types[i]):
                    raise TypeError(
                        f"Ошибка: аргумент {i + 1} должен быть типа {types[i].name}"
                    )

            return func(*args)

        return wrapper
    return decorator

@type_check(int, int)
def summa(a, b):
    return a + b


print("Результат сложения:", summa(5, 3))

print("Результат сложения:", summa(6, '7'))
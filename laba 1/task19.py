def cache(func):
    results = {}

    def wrapper(*args):
        if args in results:
            print("Взят из кэша")
            return results[args]

        result = func(*args)
        results[args] = result

        print("Сохранён в кэше")
        return result

    return wrapper


# Пример использования
@cache
def schet(a, b):
    print("Сохранение в кэщ")
    return a * b

print("Первый выз:", schet(5, 3))
print("Второй вызов:", schet(4, 8))

import time

def timing(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()

        result = func(*args, **kwargs)

        end = time.perf_counter()

        taken = (end - start) * 1000

        print(f"Время выполнения функции {func.__name__}: {taken:.3f} мс")

        return result

    return wrapper


# Пример использования
@timing
def summa(a, b):
    return a + b


result = summa(10, 20)

print("Результат вычисления:", result)
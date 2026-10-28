import time

def log_calls(filename):
    def decorator(func):
        def wrapper(*args, **kargs):
            current_time = time.strftime("%Y-%m-%d %H:%M:%S")

            with open(filename, "a", encoding="utf-8") as file:
                file.write(f"Время: {current_time}, Функция: {func.__name__}, Аргументы: {args}, {kargs}\n")

            return func(*args, **kargs)

        return wrapper
    return decorator

@log_calls("file.txt")
def summa(a, b):
    return a + b


print("Результат:", summa(5, 3))
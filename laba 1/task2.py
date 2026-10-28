password = input("Введите пароль: ")

if len(password) < 16:
    print("Пароль слишком короткий")
elif password.isalpha():
    print("слабый пароль, добавьте цифры в пароль")
elif password.isdigit():
    print("слабый пароль, добавьте буквы в пароль")
else:
    print("Надежный пароль")
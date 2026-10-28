import random

number = random.randint(1, 100)

while True:
    guess = int(input("Угадай число от 1 до 100 "))

    if guess < number:
        print("Загаданное число больше")
    elif guess > number:
        print("Загаданное число меньше")
    else:
        print("Ты угадал")
        break
text = input("Введите слово: ")
text = text.lower()
if text == text[::-1]:
    print("Это палиндром")
else:
    print("Это не палиндром")
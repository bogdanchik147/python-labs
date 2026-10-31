text = input("Введите текст: ")

words = text.lower().split()

print("Количество слов:", len(words))

if len(words) > 0:
    print("Самое короткое слово:", min(words, key=len))
    print("Самое длинное слово:", max(words, key=len))

    short_words = []

    for word in words:
        if len(word) < 3:
            short_words.append(word)

    print("Слова короче 3 букв:", short_words)

    for word in set(words):
        print(word, "-", words.count(word), "раз")
else:
    print("Текст пустой")
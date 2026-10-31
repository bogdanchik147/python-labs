def spisok(lst):
    i = 0

    while i < len(lst):
        if isinstance(lst[i], list):
            nested = lst.pop(i)

            for item in reversed(nested):
                lst.insert(i, item)

            spisok(lst)
        else:
            i += 1

list_a = [1, 2, 3, [4], 5, [6, [7, [], 8, [9]]]]
print("До:",list_a )
spisok(list_a)
print("После:", list_a)
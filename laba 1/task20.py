def unique_elements(list_a):
    result = []

    def func(lst):
        for element in lst:
            if isinstance(element, list):
                func(element)
            else:
                if element not in result:
                    result.append(element)

    func(list_a)

    return result

list_a = [1, 2, 3, [4, 3, 1], 5, [6, [7, [10], 8, [9, 2, 3]]]]
print("До:",list_a)
print("После:", unique_elements(list_a))

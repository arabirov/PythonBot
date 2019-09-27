def fibonacci(a):
    """расчёт чисел фибоначчи,
    возвращается кортеж
    """
    b = []
    c = 0
    d = 1
    i = 0
    while i < a:
        b[i:i + 1] = [c]
        c, d = d, c + d
        i += 1
        if i >= a:
            return b


if __name__ == "__main__":
    """проверка на выполнение как главной программы
    т.к. модуль может вызываться в других местах
    """
    your_number = input("Enter number: \n")
    if your_number.isdigit() and int(your_number) > 0:
        print("Sequence: ", fibonacci(int(your_number)), "\n")
    else:
        print("Please, use only positive digits")

def digit_sum(number):
    if type(number) is not int:
        raise ValueError("Ожидается целое число")
    # Знак не является цифрой: для отрицательного числа считаем цифры его модуля.
    number = abs(number)
    total = 0
    while number:
        number, digit = divmod(number, 10)
        total += digit
    return total


def main():
    try:
        print(digit_sum(int(input())))
    except (ValueError, EOFError):
        print("Ошибка: введите целое число")


if __name__ == "__main__":
    main()

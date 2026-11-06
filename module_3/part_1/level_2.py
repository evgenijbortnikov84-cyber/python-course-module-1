MESSAGE = "for - частный случай цикла while"


def repeat_message(count):
    if type(count) is not int or count <= 0:
        raise ValueError("Количество повторений должно быть положительным целым числом")
    while count > 0:
        print(MESSAGE)
        count -= 1


def main():
    try:
        repeat_message(int(input()))
    except (ValueError, EOFError):
        print("Ошибка: введите положительное целое число")


if __name__ == "__main__":
    main()

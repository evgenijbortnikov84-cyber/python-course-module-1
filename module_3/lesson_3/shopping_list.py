"""Модуль 3, урок 3: список покупок с разделением программы на функции."""

from math import isfinite


def add_position(shopping_list, name, quantity):
    """Добавить количество к новой или существующей позиции."""
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Название не должно быть пустым")
    if (type(quantity) not in (int, float) or quantity <= 0
            or isinstance(quantity, float) and not isfinite(quantity)):
        raise ValueError("Количество должно быть положительным конечным числом")
    name = name.strip()
    total = shopping_list.get(name, 0) + quantity
    if isinstance(total, float):
        if not isfinite(total):
            raise ValueError("Слишком большое количество")
        if total.is_integer():
            total = int(total)
    shopping_list[name] = total


def remove_position(shopping_list, name):
    """Удалить позицию целиком; отсутствие позиции не является ошибкой."""
    shopping_list.pop(name, None)


def show_shopping_list(shopping_list):
    """Показать покупки в лексикографическом порядке названий."""
    if not shopping_list:
        print("Список пуст.")

    for name in sorted(shopping_list):
        print(name, shopping_list[name])


def show_help():
    print("Команды: добавить, удалить, показать, выход")


def add_many_positions(shopping_list):
    """Вводить позиции подряд, пока пользователь не введёт пустую строку."""
    while True:
        position = input(
            "Название и количество; Enter - закончить: "
        ).strip()

        if not position:
            break

        # Отделяем количество справа: название может содержать пробелы.
        try:
            name, quantity = position.rsplit(maxsplit=1)
            add_position(shopping_list, name, float(quantity))
        except ValueError:
            print("Ошибка: введите название и положительное число, например хлеб 2")


def handle_command(command, shopping_list):
    """Обработать команду; False означает завершение программы."""
    if command == "добавить":
        add_many_positions(shopping_list)
    elif command == "удалить":
        name = input("Что удалить: ").strip()
        remove_position(shopping_list, name)
    elif command == "показать":
        show_shopping_list(shopping_list)
    elif command == "выход":
        return False
    else:
        show_help()

    return True


def main():
    shopping_list = {}
    show_help()

    while True:
        command = input("Введите команду: ").strip().lower()
        if not handle_command(command, shopping_list):
            break


if __name__ == "__main__":
    main()

"""Модуль 3, урок 3: список покупок с разделением программы на функции."""


def add_position(shopping_list, name, quantity):
    """Добавить количество к новой или существующей позиции."""
    shopping_list[name] = shopping_list.get(name, 0) + quantity


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
            "Название и количество; Enter — закончить: "
        ).strip()

        if not position:
            break

        # Отделяем количество справа: название может содержать пробелы.
        name, quantity = position.rsplit(maxsplit=1)
        add_position(shopping_list, name, float(quantity))


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

from functools import cmp_to_key


def compare(left, right):
    # Для соседних частей сравниваем оба порядка склейки.
    # Выгодный обмен увеличивает общее число, не меняя остальных частей.
    first = left + right
    second = right + left
    return (second > first) - (second < first)


def largest_number(numbers):
    numbers = list(numbers)
    if not numbers:
        raise ValueError("Введите хотя бы одно число")
    if any(type(number) is not int or number < 0 for number in numbers):
        raise ValueError("Разрешены только неотрицательные целые числа")
    parts = sorted(map(str, numbers), key=cmp_to_key(compare))
    return int("".join(parts))


def main():
    try:
        print(largest_number(map(int, input("Неотрицательные целые через пробел: ").split())))
    except (ValueError, EOFError) as error:
        print(f"Ошибка: {error}")


if __name__ == "__main__":
    main()

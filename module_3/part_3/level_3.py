from functools import cmp_to_key


def compare(left, right):
    # Ставим впереди ту часть, которая даёт большее число при склейке.
    first = left + right
    second = right + left
    return (second > first) - (second < first)


def largest_number(numbers):
    parts = sorted(map(str, numbers), key=cmp_to_key(compare))
    return int("".join(parts) or "0")


if __name__ == "__main__":
    print(largest_number(map(int, input("Неотрицательные целые через пробел: ").split())))

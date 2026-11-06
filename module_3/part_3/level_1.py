from math import isfinite, sqrt


def area(a, b, c):
    if not all(isfinite(side) for side in (a, b, c)):
        raise ValueError("Стороны должны быть конечными числами")
    shortest, middle, longest = sorted((a, b, c))
    if shortest <= 0 or shortest + middle <= longest:
        raise ValueError("Такие стороны не образуют треугольник")
    half = (a + b + c) / 2
    result = sqrt(half * (half - a) * (half - b) * (half - c))
    if not isfinite(result):
        raise ValueError("Числа слишком велики для вычисления площади")
    return result


def main():
    try:
        sides = input("Три стороны через пробел: ").split()
        if len(sides) != 3:
            raise ValueError("Введите ровно три стороны")
        print(area(*map(float, sides)))
    except (ValueError, OverflowError, EOFError) as error:
        print(f"Ошибка: {error}")


if __name__ == "__main__":
    main()

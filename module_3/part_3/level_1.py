from math import sqrt


def area(a, b, c):
    shortest, middle, longest = sorted((a, b, c))
    if shortest <= 0 or shortest + middle <= longest:
        raise ValueError("Такие стороны не образуют треугольник")
    half = (a + b + c) / 2
    return sqrt(half * (half - a) * (half - b) * (half - c))


if __name__ == "__main__":
    print(area(*map(float, input("Три стороны через пробел: ").split())))

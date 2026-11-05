"""Часть 1, уровень 3: максимум двух чисел через сравнение и умножение."""

first = float(input())
second = float(input())

# True при умножении равен 1, False равен 0.
# При равных числах выбираем первое, чтобы не сложить их дважды.
maximum = first * (first >= second) + second * (second > first)
print(maximum)

import json
from math import isfinite


def matrix_max(matrix):
    """Максимум числовой матрицы. Пустые матрицы и строки отклоняются."""
    if not matrix or any(not row for row in matrix):
        raise ValueError("Матрица и каждая её строка должны содержать числа")
    for row in matrix:
        for value in row:
            if (type(value) not in (int, float)
                    or isinstance(value, float) and not isfinite(value)):
                raise ValueError("Элементы матрицы должны быть конечными числами")
    # Генератор выдаёт максимумы строк по одному, без промежуточного списка.
    return max(max(row) for row in matrix)


def main():
    try:
        matrix = json.loads(input("Матрица в формате JSON: "))
        if not isinstance(matrix, list) or any(not isinstance(row, list) for row in matrix):
            raise ValueError("Ожидается список строк")
        print(matrix_max(matrix))
    except (ValueError, TypeError, EOFError):
        print("Ошибка: нужна непустая числовая матрица без пустых строк")


if __name__ == "__main__":
    main()

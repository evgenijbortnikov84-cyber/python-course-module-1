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


if __name__ == "__main__":
    # Можно заменить числа в этом примере или вызвать matrix_max со своей матрицей.
    matrix = [[9, 70], [100, 1]]
    print(matrix_max(matrix))

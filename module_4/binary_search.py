def binary_search(numbers, target):
    """Вернуть индекс совпадения или -1, если цель отсутствует.

    Список должен быть отсортирован по возрастанию; порядок не проверяется.
    При повторах возвращается любое найденное вхождение.
    Время: O(1) в лучшем случае, O(log n) в худшем. Память: O(1).
    """
    left, right = 0, len(numbers) - 1
    while left <= right:
        middle = (left + right) // 2
        if numbers[middle] == target:
            return middle
        if numbers[middle] < target:
            left = middle + 1
        else:
            right = middle - 1
    return -1


if __name__ == "__main__":
    print(binary_search([2, 4, 7, 11, 16], 11))  # 3

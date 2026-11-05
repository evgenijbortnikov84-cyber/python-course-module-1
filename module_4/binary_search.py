def binary_search(numbers, target):
    """Вернуть индекс цели в списке по возрастанию или -1, если её нет."""
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

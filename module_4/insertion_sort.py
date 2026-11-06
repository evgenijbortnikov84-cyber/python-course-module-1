def insertion_sort(numbers):
    """Стабильно отсортировать список на месте по возрастанию.

    Возвращает None. Использует обычное сравнение элементов, без key/reverse.
    Время: O(n) для упорядоченного списка, O(n²) в среднем и худшем случае.
    Дополнительная память: O(1).
    """
    for index in range(1, len(numbers)):
        value = numbers[index]
        position = index
        # Строгое > сохраняет взаимный порядок равных элементов.
        while position > 0 and numbers[position - 1] > value:
            numbers[position] = numbers[position - 1]
            position -= 1
        numbers[position] = value


if __name__ == "__main__":
    numbers = [5, -2, 5, 1]
    insertion_sort(numbers)
    print(numbers)

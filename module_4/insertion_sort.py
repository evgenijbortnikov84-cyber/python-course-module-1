def insertion_sort(numbers):
    """Отсортировать список на месте по возрастанию и вернуть его."""
    for index in range(1, len(numbers)):
        value = numbers[index]
        position = index
        # Сдвигаем большие элементы уже отсортированной части вправо.
        while position > 0 and numbers[position - 1] > value:
            numbers[position] = numbers[position - 1]
            position -= 1
        numbers[position] = value
    return numbers


if __name__ == "__main__":
    print(insertion_sort([5, -2, 5, 1]))  # [-2, 1, 5, 5]

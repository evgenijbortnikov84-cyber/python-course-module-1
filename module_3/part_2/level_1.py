def find_duplicates(items):
    """Повторы с учётом типа: 1, True и 1.0 считаются разными элементами."""
    counts = {}
    for item in items:
        key = (type(item), item)
        counts[key] = counts.get(key, 0) + 1
    return [value for (_, value), count in counts.items() if count > 1]


if __name__ == "__main__":
    # Пример легко изменить; функция принимает любой набор хешируемых элементов.
    items = [1, 4, 1, 6, "hello", "a", 5, "hello"]
    print(find_duplicates(items))

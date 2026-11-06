import json
from collections import Counter


def find_duplicates(items):
    """Повторяющиеся хешируемые элементы в порядке первого появления, O(n)."""
    counts = Counter(items)
    return [item for item, count in counts.items() if count > 1]


def main():
    try:
        items = json.loads(input("Список в формате JSON: "))
        if not isinstance(items, list):
            raise ValueError("Ожидается список")
        print(find_duplicates(items))
    except (ValueError, TypeError, EOFError):
        print("Ошибка: нужен JSON-список чисел, строк или других хешируемых значений")


if __name__ == "__main__":
    main()

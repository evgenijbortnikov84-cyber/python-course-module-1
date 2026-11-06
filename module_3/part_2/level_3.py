import json


def group_names_by_id(users):
    """Каждому id соответствует список имён: совпадения не теряются."""
    names_by_id = {}
    for name, identifier in users.items():
        names_by_id.setdefault(identifier, []).append(name)
    return names_by_id


def main():
    try:
        users = json.loads(input("Словарь имя: id в формате JSON: "))
        if not isinstance(users, dict) or any(
                not isinstance(identifier, str) for identifier in users.values()):
            raise ValueError("Идентификаторы должны быть строками")
        print(group_names_by_id(users))
    except (ValueError, TypeError, EOFError):
        print("Ошибка: нужен JSON-словарь имён со строковыми id")


if __name__ == "__main__":
    main()

def group_names_by_id(users):
    """Принимает пары (имя, id) либо готовый словарь. Сохраняет все пары."""
    pairs = users.items() if isinstance(users, dict) else users
    names_by_id = {}
    for name, identifier in pairs:
        names_by_id.setdefault(identifier, []).append(name)
    return names_by_id


if __name__ == "__main__":
    # Список пар сохраняет даже повтор имени с другим id. Числовые id допустимы.
    users = [("Анна", 1), ("Иван", 1), ("Анна", 2)]
    print(group_names_by_id(users))

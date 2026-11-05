users = {"name1": "id1", "name2": "id2", "name3": "id3"}
names_by_id = {identifier: name for name, identifier in users.items()}
print(names_by_id)

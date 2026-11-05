items = [1, 4, 1, 6, "hello", "a", 5, "hello"]
duplicates = []
for item in items:
    if items.count(item) > 1 and item not in duplicates:
        duplicates.append(item)
print(duplicates)

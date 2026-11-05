number = abs(int(input()))
total = 0
while number:
    number, digit = divmod(number, 10)
    total += digit
print(total)

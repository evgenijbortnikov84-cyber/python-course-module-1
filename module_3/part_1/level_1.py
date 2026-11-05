from decimal import Decimal, ROUND_FLOOR

balance = Decimal(input())
target = Decimal(input())
rate = Decimal(input())
years = 0
while balance < target:
    updated = (balance * (1 + rate / 100)).quantize(Decimal("0.01"), rounding=ROUND_FLOOR)
    if updated <= balance:
        print("Цель недостижима")
        break
    balance = updated
    years += 1
else:
    print(years)

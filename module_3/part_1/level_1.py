from decimal import Decimal, DecimalException, ROUND_FLOOR

CENT = Decimal("0.01")


def years_to_target(balance, target, rate):
    """Число лет с ежегодным округлением вниз до копеек; None, если роста нет."""
    balance, target, rate = (Decimal(str(value)) for value in (balance, target, rate))
    if not all(value.is_finite() for value in (balance, target, rate)):
        raise ValueError("Введите конечные числа")
    if balance < 0 or target < 0:
        raise ValueError("Суммы не должны быть отрицательными")
    years = 0
    if balance >= target:
        return years
    # При нулевом вкладе или неположительной ставке цель выше вклада недостижима.
    if balance == 0 or rate <= 0:
        return None
    while balance < target:
        updated = (balance * (1 + rate / 100)).quantize(CENT, rounding=ROUND_FLOOR)
        if updated <= balance:
            return None
        balance = updated
        years += 1
    return years


def main():
    try:
        years = years_to_target(input(), input(), input())
        print("Цель недостижима" if years is None else years)
    except (ValueError, DecimalException, EOFError):
        print("Ошибка: введите три конечных числа; суммы не должны быть отрицательными")


if __name__ == "__main__":
    main()

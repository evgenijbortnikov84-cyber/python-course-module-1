from decimal import Decimal, DecimalException, ROUND_FLOOR

CENT = Decimal("0.01")
MAX_YEARS = 10_000


def years_to_target(balance, target, rate, max_years=MAX_YEARS):
    """Возвращает int. ValueError: нет роста; RuntimeError: исчерпан лимит."""
    if type(max_years) is not int or max_years < 0:
        raise ValueError("Лимит лет должен быть неотрицательным целым числом")
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
        raise ValueError("Цель недостижима при заданных условиях")
    while balance < target:
        if years >= max_years:
            raise RuntimeError(f"Цель не достигнута за {max_years} лет; расчёт остановлен")
        updated = (balance * (1 + rate / 100)).quantize(CENT, rounding=ROUND_FLOOR)
        if updated <= balance:
            raise ValueError("Цель недостижима при заданных условиях")
        balance = updated
        years += 1
    return years


def main():
    try:
        years = years_to_target(input(), input(), input())
        print(years)
    except (ValueError, RuntimeError) as error:
        print(f"Ошибка: {error}")
    except (DecimalException, EOFError):
        print("Ошибка: введите три конечных числа; суммы не должны быть отрицательными")


if __name__ == "__main__":
    main()

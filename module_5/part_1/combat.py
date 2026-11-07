"""Общий контракт случайности и данные одного удара."""
import random
from dataclasses import dataclass
from typing import Protocol, runtime_checkable


@runtime_checkable
class RandomProvider(Protocol):
    def choose_action(self) -> str: ...
    def roll_damage(self, bounds: tuple[int, int]) -> int: ...


class RandomSource:
    def __init__(self, seed=None):
        self._random = random.Random(seed)

    def choose_action(self):
        return self._random.choice(("атака", "защита"))

    def roll_damage(self, bounds):
        return self._random.randint(*bounds)


def check_source(source):
    if (not isinstance(source, RandomProvider)
            or not callable(source.choose_action) or not callable(source.roll_damage)):
        raise TypeError("Источник должен предоставлять choose_action и roll_damage")
    return source


@dataclass(frozen=True)
class Attack:
    power: int
    exhausted: bool = False

    def __post_init__(self):
        if type(self.power) is not int or self.power < 0 or type(self.exhausted) is not bool:
            raise ValueError("Удар: неотрицательная целая сила и признак истощения bool")

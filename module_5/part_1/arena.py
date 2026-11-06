import random
from dataclasses import dataclass

if __package__:
    from .warrior import Warrior
else:
    from warrior import Warrior

START_ARMOR = 100
START_ENDURANCE = 100
ATTACK_COST = 10
DEFEAT_HEALTH = 10
ATTACK = "атака"
DEFEND = "защита"
NORMAL_DAMAGE = (10, 30)
PROTECTED_DAMAGE = (0, 20)
EXHAUSTED_DAMAGE = (0, 10)
ARMOR_DAMAGE = (0, 10)


class RandomSource:
    """Источник случайности: choose_action() и roll_damage(bounds)."""

    def __init__(self, seed=None):
        self._random = random.Random(seed)

    def choose_action(self):
        return self._random.choice((ATTACK, DEFEND))

    def roll_damage(self, bounds):
        return self._random.randint(*bounds)


@dataclass(frozen=True)
class Hit:
    normal: int
    protected: int
    armor: int


class ArenaWarrior(Warrior):
    """Расширяет общего воина бронёй, защитой и выносливостью."""

    def __init__(self, name):
        super().__init__(name)
        self._armor = START_ARMOR
        self._endurance = START_ENDURANCE
        self._defending = False

    @property
    def armor(self):
        return self._armor

    @property
    def endurance(self):
        return self._endurance

    @property
    def defending(self):
        return self._defending

    def start_round(self):
        self._defending = False

    def defend(self):
        self._defending = True

    def prepare_hit(self, source):
        exhausted = self._endurance == 0
        self._endurance = max(0, self._endurance - ATTACK_COST)
        if exhausted:
            damage = source.roll_damage(EXHAUSTED_DAMAGE)
            return Hit(damage, damage, source.roll_damage(ARMOR_DAMAGE))
        return Hit(source.roll_damage(NORMAL_DAMAGE),
                   source.roll_damage(PROTECTED_DAMAGE),
                   source.roll_damage(ARMOR_DAMAGE))

    def take_damage(self, amount):
        if isinstance(amount, Hit):
            if any(type(value) is not int or value < 0
                   for value in (amount.normal, amount.protected, amount.armor)):
                raise ValueError("Параметры удара должны быть целыми и неотрицательными")
            protected = self.defending and self.armor > 0
            if protected:
                self._armor = max(0, self._armor - amount.armor)
            amount = amount.protected if protected else amount.normal
        return super().take_damage(amount)

    def attack(self, opponent, source):
        return opponent.take_damage(self.prepare_hit(source))


@dataclass(frozen=True)
class BattleResult:
    winner: Warrior | None
    losers: tuple


class Arena:
    """Бой ровно двух воинов. Ввод и печать находятся вне правил игры."""

    def __init__(self, warriors, source=None, defeat_health=DEFEAT_HEALTH):
        self.warriors = tuple(warriors)
        if (len(self.warriors) != 2 or self.warriors[0] is self.warriors[1]
                or not all(isinstance(w, ArenaWarrior) for w in self.warriors)):
            raise ValueError("Нужны два разных воина арены")
        if type(defeat_health) is not int or not 0 <= defeat_health < 100:
            raise ValueError("Порог поражения должен быть от 0 до 99")
        self.source = source if source is not None else RandomSource()
        self.defeat_health = defeat_health

    def result(self):
        losers = tuple(w for w in self.warriors if w.health <= self.defeat_health)
        if not losers:
            return None
        winner = None
        for warrior in self.warriors:
            if warrior not in losers:
                winner = warrior
        return BattleResult(winner, losers)

    def round(self):
        if self.result() is not None:
            raise ValueError("Партия уже закончена")
        actions = [self.source.choose_action() for _ in self.warriors]
        if any(action not in (ATTACK, DEFEND) for action in actions):
            raise ValueError("Неизвестное действие")
        for warrior, action in zip(self.warriors, actions):
            warrior.start_round()
            if action == DEFEND:
                warrior.defend()
        # Все удары подготовлены до изменения здоровья. Ответный удар
        # состоится даже при поражении атакующего в этом же раунде.
        hits = [w.prepare_hit(self.source) if action == ATTACK else None
                for w, action in zip(self.warriors, actions)]
        events = []
        for index, hit in enumerate(hits):
            if hit is not None:
                attacker = self.warriors[index]
                opponent = self.warriors[1 - index]
                damage = opponent.take_damage(hit)
                events.append((attacker.name, opponent.name, damage))
        return events

    def play(self, max_rounds=10000):
        if type(max_rounds) is not int or max_rounds < 1:
            raise ValueError("Число раундов должно быть положительным")
        for _ in range(max_rounds):
            result = self.result()
            if result is not None:
                return result
            self.round()
        result = self.result()
        if result is None:
            raise RuntimeError("Лимит раундов исчерпан; победитель не определён")
        return result


def main():
    arena = Arena((ArenaWarrior("Первый"), ArenaWarrior("Второй")))
    for _ in range(10000):
        if arena.result() is not None:
            break
        for attacker, opponent, damage in arena.round():
            print(f"{attacker} атакует {opponent}, урон {damage}")
    result = arena.result()
    if result is None:
        print("Лимит раундов исчерпан")
        return
    print(f"Победил {result.winner.name}" if result.winner else "Ничья")
    for loser in result.losers:
        answer = input(f"Убить {loser.name}? да/нет: ").strip().lower()
        while answer not in ("да", "нет"):
            answer = input("Введите да или нет: ").strip().lower()
        loser.finish(spare=answer == "нет")
        print(f"{loser.name}: здоровье {loser.health}")


if __name__ == "__main__":
    main()

from dataclasses import dataclass

if __package__:
    from .warrior import Warrior
    from .combat import Attack, RandomProvider, RandomSource, check_source
else:
    from warrior import Warrior
    from combat import Attack, RandomProvider, RandomSource, check_source

START_ARMOR = 100
START_ENDURANCE = 100
ATTACK_COST = 10
DEFEAT_HEALTH = 10
ATTACK = "атака"
DEFEND = "защита"
NORMAL_DAMAGE = (10, 30)
EXHAUSTED_DAMAGE = (0, 10)


class ArenaWarrior(Warrior):
    """Расширяет общего воина бронёй, защитой и выносливостью."""

    # Только получатель знает правила защиты и потери брони.
    DEFENSE_REDUCTION = 10
    ARMOR_DAMAGE = (0, 10)

    def __init__(self, name, source: RandomProvider | None = None):
        super().__init__(name, source)
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

    def prepare_attack(self):
        exhausted = self.endurance == 0
        bounds = EXHAUSTED_DAMAGE if exhausted else NORMAL_DAMAGE
        power = self._source.roll_damage(bounds)
        if type(power) is not int or not bounds[0] <= power <= bounds[1]:
            raise ValueError("Источник вернул урон вне заданного диапазона")
        self._endurance = max(0, self.endurance - ATTACK_COST)
        return Attack(power, exhausted)

    def receive_attack(self, attack: Attack):
        damage = attack.power
        if self.defending and self.armor > 0:
            loss = self._source.roll_damage(self.ARMOR_DAMAGE)
            if type(loss) is not int or not self.ARMOR_DAMAGE[0] <= loss <= self.ARMOR_DAMAGE[1]:
                raise ValueError("Источник вернул потерю брони вне диапазона")
            if not attack.exhausted:
                # Равномерный урон 10..30 превращается в 0..20.
                damage = max(0, damage - self.DEFENSE_REDUCTION)
            self._armor = max(0, self.armor - loss)
        return self.take_damage(damage)


@dataclass(frozen=True)
class BattleResult:
    winner: Warrior | None
    losers: tuple


class Arena:
    """Бой ровно двух воинов. Ввод и печать находятся вне правил игры."""

    def __init__(self, warriors, source: RandomProvider | None = None, defeat_health=DEFEAT_HEALTH):
        self.warriors = tuple(warriors)
        if (len(self.warriors) != 2 or self.warriors[0] is self.warriors[1]
                or not all(isinstance(w, ArenaWarrior) for w in self.warriors)):
            raise ValueError("Нужны два разных воина арены")
        if type(defeat_health) is not int or not 0 <= defeat_health < 100:
            raise ValueError("Порог поражения должен быть от 0 до 99")
        self.source = check_source(source if source is not None else RandomSource())
        for warrior in self.warriors:
            warrior.set_random_source(self.source)
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
        # Решения приняты до ударов. Вызываем обе атаки даже после поражения
        # одного участника: сила в этой модели не зависит от текущего здоровья.
        # Для подкласса с зависимостью силы от здоровья понадобятся снимки раунда.
        first, second = self.warriors
        events = []
        for attacker, opponent, action in ((first, second, actions[0]),
                                           (second, first, actions[1])):
            if action == ATTACK:
                damage = attacker.attack(opponent)
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

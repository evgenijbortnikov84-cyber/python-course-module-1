import random

if __package__:
    from .combat import Attack, RandomProvider, RandomSource, check_source
else:
    from combat import Attack, RandomProvider, RandomSource, check_source

START_HEALTH = 100
SIMPLE_DAMAGE = 20


class Warrior:
    def __init__(self, name, source: RandomProvider | None = None):
        self.name = name
        self._health = START_HEALTH
        self.set_random_source(source if source is not None else RandomSource())

    @property
    def health(self):
        return self._health

    def take_damage(self, amount):
        if not isinstance(amount, int) or isinstance(amount, bool) or amount < 0:
            raise ValueError("Урон должен быть целым неотрицательным числом")
        lost = min(self._health, amount)
        self._health -= lost
        return lost

    def set_random_source(self, source: RandomProvider):
        self._source = check_source(source)

    def prepare_attack(self):
        return Attack(SIMPLE_DAMAGE)

    def receive_attack(self, attack: Attack):
        return self.take_damage(attack.power)

    def attack(self, opponent):
        return opponent.receive_attack(self.prepare_attack())

    def finish(self, *, spare):
        self._health = max(1, self._health) if spare else 0


def main():
    rng = random.Random()
    warriors = [Warrior("Первый"), Warrior("Второй")]
    winner = None
    while winner is None:
        attacker, opponent = rng.sample(warriors, 2)
        damage = attacker.attack(opponent)
        print(f"{attacker.name} атаковал: урон {damage}, здоровье {opponent.name}: {opponent.health}")
        if opponent.health == 0:
            winner = attacker
    print(f"Победил {winner.name}")


if __name__ == "__main__":
    main()

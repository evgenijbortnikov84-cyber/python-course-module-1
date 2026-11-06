import random


class Warrior:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.armor = 100
        self.endurance = 100
        self.defending = False

    def defend(self):
        self.defending = True

    def attack(self, opponent, rng=random):
        exhausted = self.endurance == 0
        self.endurance = max(0, self.endurance - 10)
        if exhausted:
            damage = rng.randint(0, 10)
        elif opponent.defending and opponent.armor > 0:
            damage = rng.randint(0, 20)
        else:
            damage = rng.randint(10, 30)
        if opponent.defending and opponent.armor > 0:
            opponent.armor = max(0, opponent.armor - rng.randint(0, 10))
        opponent.health = max(0, opponent.health - damage)
        return damage


def play_round(first, second, rng=random):
    warriors = (first, second)
    actions = [rng.choice(("атака", "защита")) for _ in warriors]
    for warrior, action in zip(warriors, actions):
        warrior.defending = False
        if action == "защита":
            warrior.defend()
    # Решения принимаются до ударов, обе атаки одного раунда выполняются.
    for attacker, opponent, action in zip(warriors, reversed(warriors), actions):
        if action == "атака":
            damage = attacker.attack(opponent, rng)
            print(f"{attacker.name} атакует {opponent.name}, урон {damage}")
    for warrior, action in zip(warriors, actions):
        print(f"{warrior.name}: {action}, здоровье {warrior.health}, "
              f"броня {warrior.armor}, выносливость {warrior.endurance}")


def main():
    warriors = (Warrior("Первый"), Warrior("Второй"))
    while all(warrior.health > 10 for warrior in warriors):
        play_round(*warriors)
    losers = [warrior for warrior in warriors if warrior.health <= 10]
    if len(losers) == 2:
        print("Ничья")
    else:
        winner = next(warrior for warrior in warriors if warrior not in losers)
        print(f"Победил {winner.name}")
    for loser in losers:
        answer = input(f"Убить {loser.name}? да/нет: ").strip().lower()
        while answer not in ("да", "нет"):
            answer = input("Введите да или нет: ").strip().lower()
        loser.health = 0 if answer == "да" else max(1, loser.health)
        print(f"{loser.name}: здоровье {loser.health}")


if __name__ == "__main__":
    main()

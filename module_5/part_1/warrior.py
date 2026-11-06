import random


class Warrior:
    def __init__(self, name):
        self.name = name
        self.health = 100

    def attack(self, opponent):
        opponent.health = max(0, opponent.health - 20)
        print(f"{self.name} атаковал. Здоровье {opponent.name}: {opponent.health}")


def main():
    warriors = [Warrior("Первый"), Warrior("Второй")]
    while all(warrior.health > 0 for warrior in warriors):
        attacker, opponent = random.sample(warriors, 2)
        attacker.attack(opponent)
    print(f"Победил {attacker.name}")


if __name__ == "__main__":
    main()

from abc import ABC, abstractmethod


class Prototype(ABC):
    @abstractmethod
    def clone(self):
        pass


class Warrior(Prototype):
    def __init__(self, height, age, defense, attack):
        self.height = height
        self.age = age
        self.defense = defense
        self.attack = attack

    def clone(self):
        return Warrior(
            self.height,
            self.age,
            self.defense,
            self.attack
        )

    def __str__(self):
        return f"Warrior(height={self.height}, age={self.age}, defense={self.defense}, attack={self.attack})"


w1 = Warrior(180, 25, 80, 100)
w2 = w1.clone()

print(w1)
print(w2)
print(w1 is w2)
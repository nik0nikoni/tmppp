from abc import ABC, abstractmethod
# Prototype
class Prototype(ABC):

    @abstractmethod
    def clone(self):
        pass
# Concrete Prototype
class Character(Prototype):

    def __init__(self, name, hp):
        self.name = name
        self.hp = hp

    def clone(self):
        return Character(self.name, self.hp)
def main():

    hero = Character("Warrior", 100)

    hero_copy = hero.clone()

    print(hero.name, hero.hp)
    print(hero_copy.name, hero_copy.hp)

# наследники
from typing import Iterable


class Ingredient:
    def __init__(self, weight: float, calorage: int) -> None:
        self._weight = weight
        self._calorage = calorage

    def get_weight(self):
        return self._weight

    def get_calorage(self):
        return self._calorage

    def prepare(self):
        pass


class Bread(Ingredient):
    def prepare(self):
        print("Bread servered")
        pass


class Tomato(Ingredient):
    def prepare(self):
        print("Tomato fried")
        self._weight *= 0.8
        self._calorage *= 1.1


class Potato(Ingredient):
    def prepare(self):
        print("Potato saited")
        self._weight += 10
        self._calorage = self._calorage


class Berries(Ingredient):
    def __init__(self, count: int, weight: float, calorage: int):
        super().__init__(weight, calorage)
        self._count = count


potato, tomato, bread = Potato(0.3, 500), Tomato(0.4, 200), Bread(0.1, 100)


def make_dinner(ingredients: Iterable[Ingredient]):
    calorage = 0
    for ingredient in ingredients:
        ingredient.prepare()
        calorage += ingredient.get_calorage()
    print(f'The dinner is ready, his calorage is {calorage}')


make_dinner([potato, bread, tomato])

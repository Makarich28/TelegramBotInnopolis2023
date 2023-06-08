#rectangle - прямоугольник (длина, ширина) -> периметр и площадь
#square - квадрат (длина) -> периметр и площадь

#circle - круг (радиус) -> площадь и длина окружности

from math import pi

class Square:
    def __init__(self, width: float):
        self._width = width
        self._length = self._width

    def area(self):
        return self._width * self._length

    def perimetr(self):
        return 2 * (self._width + self._length)

class Recangle(Square):
    def __init__(self, width: float, length: float):
        super().__init__(width)
        self._length = length


square = Square(3)
recangle = Recangle(1, 2)
print(f'area of a recangle {recangle.area()}, perimetr of a recangle {recangle.perimetr()}')
print(f'area of a square {square.area()}, perimetr of a square {square.perimetr()}')



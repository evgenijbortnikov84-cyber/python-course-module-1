from math import hypot


class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def distance_to(self, other):
        return hypot(self.x - other.x, self.y - other.y)

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

    def __eq__(self, other):
        if not isinstance(other, Point):
            return NotImplemented
        return (self.x, self.y) == (other.x, other.y)


if __name__ == "__main__":
    point = Point(3, 4)
    print(point.distance_to(Point()))
    point.move(1, -2)
    print(point)

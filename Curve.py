import itertools
import random


class Curve:
    def __init__(self):
        self.points = []
        self.curve = None

    def add_point(self, point):
        self.points.append(point)

    def draw(self, canvas, colour):
        # If there is no curve, create one, else update the current one
        if self.curve == None:
            self.curve = canvas.create_line(self.points, fill=random.choice(colour))
        else:
            canvas.coords(self.curve, *itertools.chain.from_iterable(self.points))

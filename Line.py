import math


class Line:
    def __init__(self, x1, y1, x2, y2, speed, canvas, lineColour):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.speed = math.radians(speed)
        self.angle = 0
        self.line = canvas.create_line(
            self.x1, self.y1, self.x2, self.y2, fill=lineColour, stipple="gray50"
        )

    def update(self):
        self.angle += self.speed

    # Compares itself with another line and returns the intersection (will always be a vertical compared to a horizontal)
    def comp(self, other, canvas):
        x = canvas.coords(self.line)
        y = canvas.coords(other.line)
        x = x[0]
        y = y[1]
        return (x, y)

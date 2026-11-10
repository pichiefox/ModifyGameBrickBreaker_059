
import tkinter as tk
import random


# ==========================================
# CLASS INDUK: GAME OBJECT
# ==========================================

class GameObject:
    def __init__(self, canvas, item):
        self.canvas = canvas
        self.item = item

    def get_position(self):
        return self.canvas.coords(self.item)

    def move(self, x, y):
        self.canvas.move(self.item, x, y)

    def delete(self):
        self.canvas.delete(self.item)

# CLASS BALL
class Ball(GameObject):
    def __init__(self, canvas, x, y):
        self.radius = 10
        self.dx = 4
        self.dy = -4
        self.speed = 4

        item = canvas.create_oval(
            x - self.radius,
            y - self.radius,
            x + self.radius,
            y + self.radius,
            fill="white",
            outline="black"
        )

        super().__init__(canvas, item)

    def update(self):
        self.move(self.dx, self.dy)

        coords = self.get_position()
        width = self.canvas.winfo_width()

        # Pantulan dinding kanan dan kiri
        if coords[0] <= 0:
            self.dx = abs(self.dx)

        elif coords[2] >= width:
            self.dx = -abs(self.dx)

        # Pantulan dinding atas
        if coords[1] <= 0:
            self.dy = abs(self.dy)

    def bounce_x(self):
        self.dx *= -1

    def bounce_y(self):
        self.dy *= -1

    def increase_speed(self):
        self.dx *= 1.05
        self.dy *= 1.05

# CLASS PADDLE

class Paddle(GameObject):
    def __init__(self, canvas, x, y):
        self.width = 100
        self.height = 12
        self.ball = None

        item = canvas.create_rectangle(
            x - self.width / 2,
            y - self.height / 2,
            x + self.width / 2,
            y + self.height / 2,
            fill="yellow",
            outline="black"
        )

        super().__init__(canvas, item)

    def set_ball(self, ball):
        self.ball = ball

    def move(self, offset):
        coords = self.get_position()
        width = self.canvas.winfo_width()

        if coords[0] + offset >= 0 and coords[2] + offset <= width:
            super().move(offset, 0)

            # Bola ikut bergerak ketika belum dimulai
            if self.ball is not None:
                self.ball.move(offset, 0)

# CLASS BRICK

class Brick(GameObject):

    COLORS = {
        1: "#f4a9a9",
        2: "#a0d3f5",
        3: "#FEF7F7"
    }

    def __init__(self, canvas, x, y, hits):
        self.width = 70
        self.height = 20
        self.hits = hits

        item = canvas.create_rectangle(
            x - self.width / 2,
            y - self.height / 2,
            x + self.width / 2,
            y + self.height / 2,
            fill=self.COLORS[hits],
            outline="white",
            tags="brick"
        )

        super().__init__(canvas, item)

    def hit(self):
        self.hits -= 1

        if self.hits <= 0:
            self.delete()
            return True

        self.canvas.itemconfig(
            self.item,
            fill=self.COLORS[self.hits]
        )

        return False


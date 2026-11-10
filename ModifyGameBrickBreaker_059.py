
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
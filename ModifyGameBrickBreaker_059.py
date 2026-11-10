
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

# CLASS GAME
class Game(tk.Frame):

    def __init__(self, master):
        super().__init__(master)

        self.width = 610
        self.height = 450

        self.lives = 3
        self.score = 0

        self.state = "ready"
        self.items = {}
        self.ball = None

        self.canvas = tk.Canvas(
            self,
            width=self.width,
            height=self.height,
            bg="#1e272e",
            highlightthickness=0
        )

        self.canvas.pack()
        self.pack()

        # Membuat paddle
        self.paddle = Paddle(
            self.canvas,
            self.width / 2,
            410
        )

        # HUD
        self.hud = self.canvas.create_text(
            70, 20,
            text="Lives: 3",
            fill="white",
            font=("Arial", 14, "bold")
        )

        self.score_text = self.canvas.create_text(
            520, 20,
            text="Score: 0",
            fill="white",
            font=("Arial", 14, "bold")
        )

        # Membuat balok
        self.create_bricks()

        # Membuat bola
        self.add_ball()

        # Pesan awal
        self.message = self.draw_text(
            305, 220,
            "PRESS SPACE TO START",
            22
        )

        # Kontrol keyboard
        self.canvas.focus_set()

        self.canvas.bind(
            "<Left>",
            lambda event: self.paddle.move(-20)
        )

        self.canvas.bind(
            "<Right>",
            lambda event: self.paddle.move(20)
        )

        self.canvas.bind(
            "<space>",
            self.start_game
        )

        self.canvas.bind(
            "<p>",
            self.pause_game
        )

        self.canvas.bind(
            "<r>",
            self.restart_game
        )

        self.canvas.bind(
            "<R>",
            self.restart_game
        )

    # MEMBUAT BALOK
    def create_bricks(self):
        self.items = {}

        for x in range(45, self.width - 30, 80):

            self.add_brick(x, 65, 3)
            self.add_brick(x, 90, 2)
            self.add_brick(x, 115, 1)

    def add_brick(self, x, y, hits):
        brick = Brick(
            self.canvas,
            x,
            y,
            hits
        )

        self.items[brick.item] = brick

    # MEMBUAT BOLA

    def add_ball(self):
        if self.ball is not None:
            self.ball.delete()

        coords = self.paddle.get_position()

        x = (coords[0] + coords[2]) / 2
        y = coords[1] - 15

        self.ball = Ball(
            self.canvas,
            x,
            y
        )

        self.paddle.set_ball(self.ball)

    # MENAMPILKAN TEKS
    def draw_text(self, x, y, text, size=20):
        return self.canvas.create_text(
            x,
            y,
            text=text,
            fill="white",
            font=("Arial", size, "bold")
        )

    # UPDATE HUD   
    def update_hud(self):
        self.canvas.itemconfig(
            self.hud,
            text=f"Lives: {self.lives}"
        )

        self.canvas.itemconfig(
            self.score_text,
            text=f"Score: {self.score}"
        )

    # MEMULAI GAME

    def start_game(self, event=None):

        if self.state in ("running", "won", "lost"):
            return

        if self.state == "paused":
            self.state = "running"

        else:
            self.state = "running"

        self.canvas.delete(self.message)

        # Bola tidak lagi mengikuti paddle
        self.paddle.set_ball(None)

        self.game_loop()

    # PAUSE GAME

    def pause_game(self, event=None):

        if self.state == "running":
            self.state = "paused"

            self.message = self.draw_text(
                305, 220,
                "PAUSED - PRESS P TO RESUME",
                18
            )

        elif self.state == "paused":
            self.canvas.delete(self.message)
            self.state = "running"
            self.game_loop()
    # RESTART GAME

    def restart_game(self, event=None):

        self.state = "ready"

        self.canvas.delete("all")

        self.lives = 3
        self.score = 0
        self.ball = None

        # Membuat ulang paddle
        self.paddle = Paddle(
            self.canvas,
            self.width / 2,
            410
        )

        # Membuat ulang HUD
        self.hud = self.canvas.create_text(
            70, 20,
            text="Lives: 3",
            fill="white",
            font=("Arial", 14, "bold")
        )

        self.score_text = self.canvas.create_text(
            520, 20,
            text="Score: 0",
            fill="white",
            font=("Arial", 14, "bold")
        )

        self.create_bricks()
        self.add_ball()

        self.message = self.draw_text(
            305, 220,
            "PRESS SPACE TO START",
            22
        )

    # --------------------------------------
    # GAME LOOP
    # --------------------------------------

    def game_loop(self):

        if self.state != "running":
            return

        self.check_collisions()

        # Cek kemenangan
        if len(self.canvas.find_withtag("brick")) == 0:
            self.state = "won"

            self.draw_text(
                305, 220,
                "YOU WIN!",
                35
            )

            return

        # Update posisi bola
        self.ball.update()

        # Cek apakah bola jatuh
        if self.ball.get_position()[3] >= self.height:

            self.lives -= 1
            self.update_hud()

            if self.lives <= 0:
                self.state = "lost"

                self.draw_text(
                    305, 220,
                    "GAME OVER!",
                    35
                )

                return

            # Reset posisi bola
            self.add_ball()

            self.message = self.draw_text(
                305, 220,
                "PRESS SPACE TO CONTINUE",
                18
            )

            self.state = "ready"
            return

        # Jalankan ulang setelah 16 ms
        self.after(16, self.game_loop)

    # DETEKSI COLLISION

    def check_collisions(self):

        ball_coords = self.ball.get_position()

        previous_bottom = ball_coords[3] - self.ball.dy

        # Deteksi objek yang bersentuhan dengan bola
        overlapping = self.canvas.find_overlapping(
            *ball_coords
        )

        for item in overlapping:

            # Tabrakan dengan paddle
            if item == self.paddle.item:

                paddle_coords = self.paddle.get_position()

                if (
                    self.ball.dy > 0
                    and previous_bottom <= paddle_coords[1] + 5
                ):

                    self.ball.dy = -abs(self.ball.dy)

                    # Arah bola berdasarkan posisi pantulan
                    ball_center = (
                        ball_coords[0] + ball_coords[2]
                    ) / 2

                    paddle_center = (
                        paddle_coords[0] + paddle_coords[2]
                    ) / 2

                    offset = (
                        ball_center - paddle_center
                    ) / (self.paddle.width / 2)

                    self.ball.dx = offset * 6

                    if abs(self.ball.dx) < 1:
                        self.ball.dx = random.choice([-1, 1])

                continue

            # Tabrakan dengan brick
            if item in self.items:

                brick = self.items[item]

                destroyed = brick.hit()

                # Pantulkan bola
                self.ball.dy *= -1

                # Tambahkan skor
                if destroyed:
                    self.score += 10

                else:
                    self.score += 5

                self.update_hud()

                # Hanya proses satu tabrakan per frame
                break

# MAIN PROGRAM
if __name__ == "__main__":

    root = tk.Tk()

    root.title("Brick Breaker Game")

    root.resizable(False, False)

    game = Game(root)

    game.mainloop()

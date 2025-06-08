import pyxel
import random

class SnakeGame:
    def __init__(self):
        pyxel.init(160, 120, title="Pyxel Snake")
        self.reset()
        pyxel.run(self.update, self.draw)

    def reset(self):
        self.snake = [(10, 10), (9, 10)]
        self.dir = (1, 0)
        self.food = self.random_food()
        self.game_over = False
        self.timer = 0
        self.speed = 5  # Lower is faster

    def random_food(self):
        while True:
            pos = (random.randint(0, 19), random.randint(0, 14))
            if pos not in self.snake:
                return pos

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if self.game_over:
            if pyxel.btnp(pyxel.KEY_R):
                self.reset()
            return

        if pyxel.btnp(pyxel.KEY_UP) and self.dir != (0, 1):
            self.dir = (0, -1)
        elif pyxel.btnp(pyxel.KEY_DOWN) and self.dir != (0, -1):
            self.dir = (0, 1)
        elif pyxel.btnp(pyxel.KEY_LEFT) and self.dir != (1, 0):
            self.dir = (-1, 0)
        elif pyxel.btnp(pyxel.KEY_RIGHT) and self.dir != (-1, 0):
            self.dir = (1, 0)

        self.timer += 1
        if self.timer % self.speed == 0:
            head = self.snake[0]
            new_head = (head[0] + self.dir[0], head[1] + self.dir[1])

            # Check collision
            if (new_head in self.snake or
                not 0 <= new_head[0] < 20 or
                not 0 <= new_head[1] < 15):
                self.game_over = True
                return

            self.snake = [new_head] + self.snake
            if new_head == self.food:
                self.food = self.random_food()
            else:
                self.snake.pop()

    def draw(self):
        pyxel.cls(0)
        for (x, y) in self.snake:
            if (x, y) == self.snake[0]:
                pyxel.rect(x * 8, y * 8, 8, 8, 3)
            else:
                pyxel.rect(x * 8, y * 8, 8, 8, 11)
        fx, fy = self.food
        pyxel.rect(fx * 8, fy * 8, 8, 8, 8)

        if self.game_over:
            pyxel.text(50, 56, "GAME OVER", 8)
            pyxel.text(42, 66, "Press R to Restart", 7)

SnakeGame()

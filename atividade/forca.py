import os
import pyglet
import string
from pyglet import shapes
import random

dir_path = os.path.dirname(os.path.realpath(__file__))

window = pyglet.window.Window(width=1280, height=720, caption="Jogo da Forca")

logo = pyglet.image.load(os.path.join(dir_path, "icon.png"))
window.set_icon(logo)


class Game:
    def __init__(self, correct_word):
        self.wrong = 0
        self.tried = []
        self.correct_word = correct_word.lower()
        self.word = ["_" for letter in self.correct_word]
        self.background = pyglet.image.load(os.path.join(dir_path, "background.png"))
        self.word_label = None
        self.tried_label = None
        self.__update_label()

    def draw_hang(self):
        x = window.width // 2 - 300
        y = window.height // 2 - 120
        self.hang = pyglet.graphics.Batch()
        
        self.__hang_1 = shapes.Rectangle(x, y, 5, 300, color=(255, 255, 255), batch=self.hang)
        self.__hang_2 = shapes.Rectangle(x, y + 295, 100, 5, color=(255, 255, 255), batch=self.hang)
        self.__hang_3 = shapes.Rectangle(x + 95, y + 270, 5, 30, color=(255, 255, 255), batch=self.hang)
        self.hang.draw()

    def draw_hangman(self):
        x = window.width // 2 - 200
        y = window.height // 2 + 120
        self.hangman = pyglet.graphics.Batch()

        if self.wrong > 0:
            self.__head = shapes.Circle(x, y, 30, color=(255, 255, 255), batch=self.hangman)

        if self.wrong > 1:
            self.__body = shapes.Rectangle(x - 2, y - 100, 5, 120, color=(255, 255, 255), batch=self.hangman)

        if self.wrong > 2:
            self.__arm_1 = shapes.Rectangle(x - 5, y - 50, 70, 5, color=(255, 255, 255), batch=self.hangman)
        
        if self.wrong > 3:
            self.__arm_2 = shapes.Rectangle(x + 3, y - 50,- 70, 5, color=(255, 255, 255), batch=self.hangman)
        
        if self.wrong > 4:
            self.__leg_1 = shapes.Rectangle(x - 5, y - 170, 5, 80, color=(255, 255, 255), batch=self.hangman)
        
        if self.wrong > 5:
            self.__leg_2 = shapes.Rectangle(x + 3, y - 170, 5, 80, color=(255, 255, 255), batch=self.hangman)

        self.hangman.draw()

    def __update_label(self):
        self.word_label = pyglet.text.Label(
            " ".join(self.word),
            font_name="Arial",
            font_size=56,
            x=window.width // 2,
            y=window.height // 2 - 120,
            anchor_x="center",
            anchor_y="center",
        )
        self.tried_label = pyglet.text.Label(
            " ".join(list(self.tried)),
            font_name="Arial",
            font_size=48,
            color=(255, 46, 52, 255),
            x=window.width // 2,
            y=window.height // 2 - 220,
            anchor_x="center",
            anchor_y="center",
        )

    def press(self, key):
        if self.wrong <= 5:
            found = False
            for i in range(len(self.correct_word)):
                if self.correct_word[i] == key:
                    self.word[i] = key
                    found = True
            if not found:
                if key not in self.tried:
                    self.tried.append(key)
                self.wrong += 1
            self.__update_label()

    def run(self):
        self.background.blit(0, 0)
        self.draw_hang()
        self.draw_hangman()
        self.word_label.draw()
        self.tried_label.draw()


selected_word = ""
with open(os.path.join(dir_path, "words.txt")) as file:
    possible = [word for word in file.read().split("\n") if word.strip()]
    selected_word = random.choice(possible)

game = Game(selected_word)


@window.event
def on_draw():
    window.clear()
    game.run()


@window.event
def on_key_press(symbol, modifiers):
    global game, selected_word

    if chr(symbol) in string.ascii_lowercase:
        game.press(chr(symbol))
    elif symbol == ord('/'):
        selected_word = random.choice(possible)
        game = Game(selected_word)


if __name__ == "__main__":
    pyglet.app.run()
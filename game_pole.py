import random
import pygame
from tile import Tile
from button import Button
from settings import *


class GamePole:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.sprites = pygame.sprite.Group()
        self.pole = []
        self.mines_count = MINES_COUNT
        self.create_map()
        self.new_game_button = Button(
            (
                self.display_surface.get_rect().centerx - (BTN_SIZE[0] / 2),
                self.display_surface.get_rect().bottom - BTN_SIZE[1] - 50
            ),
            [self.sprites]
        )
        self.game_ended = False

    def run(self):
        self.sprites.draw(self.display_surface)

        if not self.game_ended:
            self.check_end_game()

    def create_map(self):
        """Рисуем карту"""
        self.pole = [[0] * FIELD_SIZE for _ in range(FIELD_SIZE)]
        for i in range(FIELD_SIZE):
            for j in range(FIELD_SIZE):
                x = i * TILE_SIZE
                y = j * TILE_SIZE
                self.pole[i][j] = Tile((x, y), [self.sprites])

        for _ in range(self.mines_count):
            self.set_mine()

    def set_mine(self):
        while True:
            x, y = random.randint(0, FIELD_SIZE - 1), random.randint(0, FIELD_SIZE - 1)
            tile = self.pole[x][y]
            if not tile.is_mine:
                tile.is_mine = True
                self.set_around_mines(x, y)
                return

    def set_around_mines(self, x, y):
        tiles_around = self.get_tiles_around(x, y)
        for x, y in tiles_around:
            self.pole[x][y].around_mines += 1

    def get_tiles_around(self, x, y):
        tiles_around = []
        if x - 1 >= 0:
            if y - 1 >= 0:
                tiles_around.append((x - 1, y - 1))
            if y + 1 < FIELD_SIZE:
                tiles_around.append((x - 1, y + 1))
            tiles_around.append((x - 1, y))
        if x + 1 < FIELD_SIZE:
            if y - 1 >= 0:
                tiles_around.append((x + 1, y - 1))
            if y + 1 < FIELD_SIZE:
                tiles_around.append((x + 1, y + 1))
            tiles_around.append((x + 1, y))
        if y - 1 >= 0:
            tiles_around.append((x, y - 1))
        if y + 1 < FIELD_SIZE:
            tiles_around.append((x, y + 1))

        return tiles_around

    def open_around(self, x, y):
        tile = self.pole[x][y]
        tiles_around = self.get_tiles_around(x, y)
        if tile.around_mines != 0:
            for x1, y1 in tiles_around:
                tile = self.pole[x1][y1]
                if tile.around_mines == 0 and not tile.fl_open and not tile.is_mine:
                    tile.set_fl_open()
                    self.open_around(x1, y1)
        else:
            for x1, y1 in tiles_around:
                tile = self.pole[x1][y1]
                if not tile.fl_open and not tile.is_mine:
                    tile.set_fl_open()
                    self.open_around(x1, y1)

    def open_tile(self, x, y):
        tile = self.pole[x][y]

        if not tile.fl_open:
            if tile.is_mine:
                # если там мина - ты проиграл!
                self.end_game()

            tile.set_fl_open()
            if tile.around_mines:
                # если там цифра, то открываем эту клетку и всё
                return

            # если там 0, то открываем вокруг рекурсивно
            self.open_around(x, y)

    def end_game(self):
        # Открываем все тайлы
        for i in range(FIELD_SIZE):
            for j in range(FIELD_SIZE):
                self.pole[i][j].set_fl_open()
        self.new_game_button.set_visible()
        self.game_ended = True

    def win(self):
        print('You won!')
        self.end_game()

    def check_end_game(self):
        number_of_closed_tiles = 0
        number_of_flags = 0
        flagged_mines = 0

        for i in range(FIELD_SIZE):
            for j in range(FIELD_SIZE):
                tile = self.pole[i][j]
                if not tile.fl_open:
                    number_of_closed_tiles += 1

                if tile.is_flagged:
                    number_of_flags += 1
                    if tile.is_mine:
                        flagged_mines += 1

        if number_of_closed_tiles == MINES_COUNT or \
                (flagged_mines == MINES_COUNT and number_of_flags == MINES_COUNT):
            self.win()

import sys
import pygame
import random
from button import Button
from tile import Tile
from settings import *


class Game:
    def __init__(self):
        # base
        pygame.init()
        pygame.display.set_caption("SwineMapper")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.screen_rect = self.screen.get_rect()
        self.clock = pygame.time.Clock()
        self.dt = 0

        # drawing
        self.all_group = pygame.sprite.Group()
        self.tiles_group = pygame.sprite.Group()
        self.field = []
        self.new_game_button = None
        self.create_map()

        self.game_ended = False

        # managing click hold
        self.last_mouse_buttons = None

    def update(self):
        if not self.game_ended:
            self.check_end_game()

        self.last_mouse_buttons = pygame.mouse.get_pressed()

    def reset(self):
        self.all_group = pygame.sprite.Group()
        self.field = []
        self.new_game_button = None
        self.create_map()
        self.game_ended = False

    def create_map(self):
        # drawing map
        self.field = [[0] * FIELD_SIZE for _ in range(FIELD_SIZE)]
        for i in range(FIELD_SIZE):
            for j in range(FIELD_SIZE):
                x = i * TILE_SIZE
                y = j * TILE_SIZE
                self.field[i][j] = Tile(
                    self, i, j, (x, y), [self.all_group, self.tiles_group]
                )

        for _ in range(MINES_COUNT):
            self.set_mine()

    def set_mine(self):
        while True:
            x, y = random.randint(0, FIELD_SIZE - 1), random.randint(0, FIELD_SIZE - 1)
            tile = self.field[x][y]
            if not tile.is_mine:
                tile.is_mine = True
                self.set_around_mines(tile)
                return

    def set_around_mines(self, tile):
        tiles_around = tile.get_tiles_around()
        for tile in tiles_around:
            tile.around_mines += 1

    def end_game(self):
        # Открываем все тайлы
        for tile in self.tiles_group:
            tile.set_is_open()

        self.new_game_button = Button(
            self,
            (
                self.screen_rect.centerx - (BTN_SIZE[0] / 2),
                self.screen_rect.bottom - BTN_SIZE[1] - 50,
            ),
            [self.all_group],
        )
        self.game_ended = True

    def win(self):  # TODO finish win scenario
        print("You won!")
        self.end_game()

    def check_end_game(self):
        number_of_closed_tiles = 0
        number_of_flags = 0
        flagged_mines = 0

        for tile in self.tiles_group:
            if not tile.is_open:
                number_of_closed_tiles += 1

            if tile.is_flagged:
                number_of_flags += 1
                if tile.is_mine:
                    flagged_mines += 1

        if number_of_closed_tiles == MINES_COUNT or (
            flagged_mines == MINES_COUNT and number_of_flags == MINES_COUNT
        ):
            self.win()

    def run(self):
        while True:
            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # framerate limit
            self.dt = self.clock.tick(120) / 1000

            # update
            self.screen.fill("black")
            self.all_group.update()
            self.update()

            # drawing
            self.all_group.draw(self.screen)

            # final frame
            pygame.display.update()


if __name__ == "__main__":
    Game().run()

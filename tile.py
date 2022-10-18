import pygame
from settings import *


class Tile(pygame.sprite.Sprite):
    image_path = {
        "default": "./graphics/tile_default.png",
        "tile_down": "./graphics/tile_down.png",
        "piggy": "./graphics/piggy.png",
        "flag": "./graphics/flag.png",
        "number_1": "./graphics/number_1.png",
        "number_2": "./graphics/number_2.png",
        "number_3": "./graphics/number_3.png",
        "number_4": "./graphics/number_4.png",
        "number_5": "./graphics/number_5.png",
        "number_6": "./graphics/number_6.png",
        "number_7": "./graphics/number_7.png",
        "number_8": "./graphics/number_8.png",
    }

    def __init__(self, game, i, j, pos, groups):
        super().__init__(groups)
        self.game = game
        self.i = i
        self.j = j
        self.image = pygame.image.load(self.image_path["default"]).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.around_mines = 0
        self.is_mine = False
        self.is_open = False
        self.is_flagged = False

    def update(self):
        if not self.game.game_ended:
            mouse_buttons_pressed = pygame.mouse.get_pressed()
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                if self.game.last_mouse_buttons != mouse_buttons_pressed:
                    # left click
                    if mouse_buttons_pressed[0]:
                        self.open_tile()

                    # right click
                    if mouse_buttons_pressed[2]:
                        print(self.game.last_mouse_buttons, mouse_buttons_pressed)
                        print("clicl")
                        self.swap_flag()

                self.image.set_alpha(230)
            else:
                self.image.set_alpha(255)

    def open_tile(self):
        if not self.is_open and not self.is_flagged:
            if self.is_mine:
                self.game.end_game()

            self.set_is_open()
            if self.around_mines:
                # If has mines around then just open the tile
                return

            # if not mines around then open around tiles
            self.open_around()

    def open_around(self):
        tiles_around = self.get_tiles_around()
        if self.around_mines != 0:
            for tile in tiles_around:
                if tile.around_mines == 0 and not tile.is_open and not tile.is_mine:
                    tile.set_is_open()
                    tile.open_around()
        else:
            for tile in tiles_around:
                if not tile.is_open and not tile.is_mine:
                    tile.set_is_open()
                    tile.open_around()

    def get_tiles_around(self):  # TODO refactor tiles around logic
        tiles_around = []
        if self.i - 1 >= 0:
            if self.j - 1 >= 0:
                tiles_around.append(self.game.field[self.i - 1][self.j - 1])
            if self.j + 1 < FIELD_SIZE:
                tiles_around.append(self.game.field[self.i - 1][self.j + 1])
            tiles_around.append(self.game.field[self.i - 1][self.j])
        if self.i + 1 < FIELD_SIZE:
            if self.j - 1 >= 0:
                tiles_around.append(self.game.field[self.i + 1][self.j - 1])
            if self.j + 1 < FIELD_SIZE:
                tiles_around.append(self.game.field[self.i + 1][self.j + 1])
            tiles_around.append(self.game.field[self.i + 1][self.j])
        if self.j - 1 >= 0:
            tiles_around.append(self.game.field[self.i][self.j - 1])
        if self.j + 1 < FIELD_SIZE:
            tiles_around.append(self.game.field[self.i][self.j + 1])

        return tiles_around

    def set_is_open(self):
        self.is_open = True
        self.is_flagged = False
        if self.is_mine:
            self.image = pygame.image.load(self.image_path["piggy"]).convert_alpha()
        else:
            if self.around_mines:
                self.image = pygame.image.load(
                    self.image_path[f"number_{self.around_mines}"]
                ).convert_alpha()
            else:
                self.image = pygame.image.load(
                    self.image_path["tile_down"]
                ).convert_alpha()

    def swap_flag(self):
        if not self.is_open:
            if self.is_flagged:
                self.is_flagged = False
                self.image = pygame.image.load(
                    self.image_path["default"]
                ).convert_alpha()
            else:
                self.is_flagged = True
                self.image = pygame.image.load(self.image_path["flag"]).convert_alpha()

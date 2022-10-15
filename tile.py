import pygame


class Tile(pygame.sprite.Sprite):
    image_path = {
        'default': './graphics/tile_default.png',
        'tile_down': './graphics/tile_down.png',
        'piggy': './graphics/piggy.png',
        'flag': './graphics/flag.png',
        'number_1': './graphics/number_1.png',
        'number_2': './graphics/number_2.png',
        'number_3': './graphics/number_3.png',
        'number_4': './graphics/number_4.png',
        'number_5': './graphics/number_5.png',
        'number_6': './graphics/number_6.png',
        'number_7': './graphics/number_7.png',
        'number_8': './graphics/number_8.png'
    }

    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load(self.image_path['default']).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.around_mines = 0
        self.is_mine = False
        self.fl_open = False
        self.is_flagged = False

    def hover(self):
        self.image.set_alpha(230)

    def hover_out(self):
        self.image.set_alpha(255)

    def set_fl_open(self):
        self.fl_open = True
        self.is_flagged = False
        if self.is_mine:
            self.image = pygame.image.load(self.image_path['piggy']).convert_alpha()
        else:
            if self.around_mines:
                self.image = pygame.image.load(self.image_path[f'number_{self.around_mines}']).convert_alpha()
            else:
                self.image = pygame.image.load(self.image_path['tile_down']).convert_alpha()

    def swap_flag(self):
        if not self.fl_open:
            if self.is_flagged:
                self.is_flagged = False
                self.image = pygame.image.load(self.image_path['default']).convert_alpha()
            else:
                self.is_flagged = True
                self.image = pygame.image.load(self.image_path['flag']).convert_alpha()


import pygame


class Button(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image_path = {
            'default': './graphics/new_game_btn.png',
            'hover': './graphics/new_game_btn_hover.png',
        }
        self.image = pygame.image.load(self.image_path['default']).convert_alpha()
        self.image.set_alpha(0)
        self.rect = self.image.get_rect(topleft=pos)
        self.is_visible = False

    def set_visible(self):
        self.is_visible = True
        self.image.set_alpha(255)

    def hover(self):
        self.image = pygame.image.load(self.image_path['hover']).convert_alpha()

    def hover_out(self):
        self.image = pygame.image.load(self.image_path['default']).convert_alpha()


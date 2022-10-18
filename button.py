import pygame


class Button(pygame.sprite.Sprite):
    image_path = {
        "default": "graphics/new_game_btn.png",
        "hover": "graphics/new_game_btn_hover.png",
    }

    def __init__(self, game, pos, groups):
        super().__init__(groups)
        self.game = game
        self.image = pygame.image.load(self.image_path["default"]).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)

    def update(self):
        if pygame.mouse.get_pressed()[0]:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                mouse_buttons_pressed = pygame.mouse.get_pressed()
                if self.game.last_mouse_buttons != mouse_buttons_pressed:
                    # left click
                    if mouse_buttons_pressed[0]:
                        self.game.reset()

        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.image = pygame.image.load(self.image_path["hover"]).convert_alpha()
        else:
            self.image = pygame.image.load(self.image_path["default"]).convert_alpha()

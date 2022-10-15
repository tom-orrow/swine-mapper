import os
import sys
import pygame
from game_pole import GamePole
from settings import *


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('SwineMapper')
        self.clock = pygame.time.Clock()
        self.pole_game = GamePole()

    def run(self):
        while True:
            for event in pygame.event.get():
                # Выход
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                mouse_pos = pygame.mouse.get_pos()

                if not self.pole_game.game_ended:
                    for i in range(FIELD_SIZE):
                        for j in range(FIELD_SIZE):
                            tile = self.pole_game.pole[i][j]
                            if tile.rect.collidepoint(mouse_pos):
                                # Левый клик на тайл
                                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                                    self.pole_game.open_tile(i, j)

                                # Правый клик на тайл
                                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                                    tile.swap_flag()

                                # Наведение на тайл
                                tile.hover()
                            else:
                                tile.hover_out()
                else:
                    new_game_btn = self.pole_game.new_game_button
                    if new_game_btn.rect.collidepoint(mouse_pos):
                        # Клик на кнопку
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            self.pole_game = GamePole()

                        # Наведение на кнопку
                        new_game_btn.hover()
                    else:
                        new_game_btn.hover_out()

            self.screen.fill('black')
            self.pole_game.run()
            pygame.display.update()
            self.clock.tick(FPS)

            # try:
            #     os.system('cls')
            #     pole_game.show()
            #     pole_game.get_input()
            # except EndGame as e:
            #     os.system('cls')
            #     pole_game.show()
            #     print(e)
            #     sys.exit(0)


if __name__ == '__main__':
    game = Game()
    game.run()

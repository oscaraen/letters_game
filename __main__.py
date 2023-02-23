"""
Main script controlling game dynamics
The game will score kids with medals by measuring
time, also will store the times to check if the kid is learning
to detect the typing fast (collecting some data)

The game must ask at first the username (register the name if not exists)
and then log the player to its scores and record the times and number of achieved letters

"""
import sys
import pygame as pg
import pygame.display
from pygame.locals import *
from config import config
from letters.environment import Background, Player

main_window = pg.display.set_mode((config.WIDTH, config.HEIGHT))
main_window.fill((255, 255, 255))
pg.display.set_caption("Juego de las letras")
FPS_CLOCK = pg.time.Clock()
background = Background()
player = Player()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pg.KEYDOWN:
            print(event)

    # render bg
    player.move()
    background.render(main_window)
    main_window.blit(player.image, player.rect)
    pygame.display.update()
    FPS_CLOCK.tick(config.GAME_FPS)

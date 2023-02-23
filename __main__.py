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
from letters.environment import Background, Player, Ground

main_window = pg.display.set_mode((config.WIDTH, config.HEIGHT))
pg.display.set_caption("Juego de las letras")
FPS_CLOCK = pg.time.Clock()
background = Background()
player = Player()
ground = Ground()
ground_group = pg.sprite.Group()
ground_group.add(ground)
while True:
    player.gravity_check(player, ground_group)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                player.jump(ground_group)
            if event.key == pg.K_ESCAPE:
                pygame.quit()
                sys.exit()

    # render bg
    player.move()
    background.render(main_window)
    ground.render(main_window)
    main_window.blit(player.image, player.rect)
    pygame.display.update()
    FPS_CLOCK.tick(config.GAME_FPS)

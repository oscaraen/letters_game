from pygame.sprite import Sprite
from pygame.image import load
from pygame import display
from skimage import io, transform
from config import config
import numpy as np
from pygame.math import Vector2 as vec
import pygame as pg
from pygame.locals import *

class Background(Sprite):
    def __init__(self):
        super().__init__()
        # todo: unhardcode paths
        self.prepare_background_img("assets/imgs/background.png")
        if self.original_bg:
            self.image = load("assets/imgs/background.png")
        else:
            self.image = load("assets/imgs/res_background.png")
        self.bgY = 0
        self.bgX = 0

    def prepare_background_img(self, img_path):
        """
        Method to fix background size prior to drawing it wrong
        :param img_path:
        :return:
        """
        img = io.imread(img_path)
        if img.shape == np.array((config.WIDTH, config.HEIGHT)):
            self.original_bg = True
        else:
            resized = transform.resize(img, (config.HEIGHT, config.WIDTH))
            resized_int = (resized * 255).round().astype(np.uint8)
            io.imsave("assets/imgs/res_background.png", resized_int)
            self.original_bg = False

    def render(self, window: display) -> None:
        window.blit(self.image, (self.bgX, self.bgY))


class Ground(Sprite):
    def __init__(self):
        super(Ground, self).__init__()


class Player(Sprite):
    def __init__(self):

        super(Player, self).__init__()
        self.image = load("assets/imgs/kamu.png")
        self.rect = self.image.get_rect()

        # position
        self.vx = 0
        self.pos = vec(340, 240)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.direction = "RIGHT"

    def move(self):
        if abs(self.vel.x) > 0.3:
            self.running = True
        else:
            self.running = False

        pressed_keys = pg.key.get_pressed()
        if pressed_keys[K_LEFT]:
            self.acc.x = -config.ACC
        elif pressed_keys[K_RIGHT]:
            self.acc.x = config.ACC

        # Formulas to calculate velocity while accounting for friction
        self.acc.x += self.vel.x * config.FRICC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc  # Updates Position with new values

    # This causes character warping from one point of the screen to the other
        if self.pos.x > config.WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = config.WIDTH

        self.rect.midbottom = self.pos  # Update rect with new pos

    def update(self):
        pass

    def attack(self):
        pass

    def jump(self):
        pass


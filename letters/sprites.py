import random

import pygame.sprite
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
        self.prepare_background_img("assets/imgs/ground.png")
        if self.original_bg:
            self.image = load("assets/imgs/ground.png")
        else:
            self.image = load("assets/imgs/res_ground.png")
        self.rect = self.image.get_rect(center=(config.WIDTH // 2, (((1080 - 195 // 4) / 1080) * config.HEIGHT)))


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
            resized = transform.resize(img, (config.HEIGHT - ((1080 - 195 // 2) / 1080) * config.HEIGHT, config.WIDTH))
            resized_int = (resized * 255).round().astype(np.uint8)
            io.imsave("assets/imgs/res_ground.png", resized_int)
            self.original_bg = False

    def render(self, window: display) -> None:
        window.blit(self.image, (self.rect.x, self.rect.y))


class LetterContainer(Sprite):
    """
    Container to show the letters
    """

    def __init__(self):
        super().__init__()
        self.current_letter = None
        self.image = load("assets/imgs/container_letter.png")
        self.rect = self.image.get_rect(center=(config.WIDTH // 2, config.HEIGHT // 2))
        self.letters = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
        self.img_bkup = self.image.copy()

    def render(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))

    def generate_letter(self):
        self.current_letter = random.choice(self.letters)
        font = pg.font.SysFont("Arial", 130)
        font_color = pg.Color("black")
        letra = self.current_letter
        self.image = self.img_bkup.copy()
        text_surface = font.render(letra, True, font_color)
        center = list(self.image.get_rect().center)
        center[1]-=50
        textrect = text_surface.get_rect(center=center)
        self.image.blit(text_surface, textrect)
        self.rect = self.image.get_rect(center=(config.WIDTH // 2, config.HEIGHT // 2))
        self.play_letter_sound()

    def play_letter_sound(self):
        letter_sound = pg.mixer.Sound(f"assets/sounds/{self.current_letter}.wav")
        pg.mixer.Sound.play(letter_sound)
        pg.mixer.music.stop()


    def play_success_sound(self):
        sound = pg.mixer.Sound(f"assets/sounds/felicitacion.wav")
        pg.mixer.Sound.play(sound)
        pg.mixer.music.stop()

    def play_error_sound(self):
        sound = pg.mixer.Sound(f"assets/sounds/no_no.wav")
        pg.mixer.Sound.play(sound)
        pg.mixer.music.stop()

    def play_instruction_sound(self):
        sound = pg.mixer.Sound(f"assets/sounds/instruccion.wav")
        pg.mixer.Sound.play(sound)
        pg.mixer.music.stop()
        pg.time.delay(3000)
        self.generate_letter()

    def update(self, pressed_key):
        print(pressed_key)
        pressed_name = pg.key.name(pressed_key)
        print(str(pressed_name).lower())
        print(self.current_letter)
        if self.current_letter is not None:
            if pressed_name in self.letters.lower():
                if pressed_name == self.current_letter.lower():
                    # lo logró, cambiar
                    self.play_success_sound()
                    pg.time.delay(3000)
                    self.generate_letter()
                else:
                    self.play_error_sound()

                    # aumentar y registrar score

                    # poner sonido de bien y globos o algo



class Player(Sprite):
    def __init__(self):
        super().__init__()
        self.image = load("assets/imgs/kamu.png")
        self.rect = self.image.get_rect(center=(10, 10 + ((1080 - 195 // 2) / 1080) * config.HEIGHT))
        # position
        self.vx = 0
        self.pos = vec(10, 570)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.direction = "RIGHT"
        # movement
        self.jumping = False
        self.jump_count = 0
        self.running = False
        self.move_frame = 0

    def move(self):
        if self.jumping:
            self.acc += vec(0, 0.5)
        else:
            self.acc = vec(0, 0.5)


        if abs(self.vel.x) > 0.25:
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

    def update(self, col_group):
        # Return to base frame if at end of movement sequence
        #if self.move_frame > 6:
        #    self.move_frame = 0
        #    return

        # Move the character to the next frame if conditions are met
        if self.jumping is False and self.running is True:
            if self.vel.x >= 0:
                # self.image = run_ani_R[self.move_frame]
                self.direction = "RIGHT"
            else:
                # self.image = run_ani_L[self.move_frame]
                self.direction = "LEFT"
            #self.move_frame += 1

        # Returns to base frame if standing still and incorrect frame is showing
        # if abs(self.vel.x) < 0.2 and self.move_frame != 0:
        #    self.move_frame = 0
        #    if self.direction == "RIGHT":
        #        pass
        #        #self.image = run_ani_R[self.move_frame]
        #    elif self.direction == "LEFT":
        #        pass
        #        #self.image = run_ani_L[self.move_frame]

    def attack(self):
        pass

    def jump(self, ground_group):
        self.rect.x += 1
        # Check to see if payer is in contact with the ground
        hits = pg.sprite.spritecollide(self, ground_group, False)
        self.rect.x -= 1
        # If touching the ground, and not currently jumping, cause the player to jump.
        if hits and not self.jumping:
            self.jumping = True
            self.acc.y = -3

    def gravity_check(self, ground_group):
        hits = pg.sprite.spritecollide(self, ground_group, False)
        if self.vel.y > 0:
            if hits:
                lowest = hits[0]
                if self.pos.y < lowest.rect.bottom:
                    self.pos.y = lowest.rect.top +1
                    self.vel.y = 0
                    self.jumping = False

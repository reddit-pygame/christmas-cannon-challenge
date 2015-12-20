from random import randint, choice

import pygame as pg

import tools
import prepare
from angles import project
from tools import strip_from_sheet as stripfrom

GRAVITY = 9.8


class Gift(pg.sprite.Sprite):
    """Ammunition for the Christmas Cannon."""
    base_colors = [(127, 201, 255), (0, 148, 255)]
    sheet  =prepare.GFX["gift-colors"]
    top_colors = [img.get_at((0, 0)) for img in stripfrom(sheet, (0, 0), (8, 8), 12)]
    bottom_colors = [img.get_at((0, 0)) for img in stripfrom(sheet, (0, 8), (8, 8), 12)]
    color_schemes = list(zip(top_colors, bottom_colors))
                                
    def __init__(self, pos, angle, speed, * groups):
        super(Gift, self).__init__(*groups)
        num = randint(1, 4)
        image = prepare.GFX["gift{}".format(num)]
        colors = choice(self.color_schemes)
        swaps = {orig: swap for orig, swap in zip(self.base_colors, colors)}
        self.image = tools.color_swap(image, swaps)
        self.rect = self.image.get_rect(center=pos)
        self.last_pos = self.rect.center
        
        #REMOVE FOR CHALLENGE
        self.origin = pos
        self.initial_x_velocity, self.initial_y_velocity = project((0, 0), angle, speed)
        self.initial_y_velocity *= -1
        
        self.time_elapsed = 0

    def update(self, dt):
        """
        Place gift at correct position based on time since being fired using
        the formula for trajectory of a projectile. Setting self.last_pos before
        moving the gift's position is necessary for checking collisions with
        chimney caps.
        """
        self.last_pos = self.rect.center
        self.time_elapsed += dt
        
        #REMOVE FOR CHALLENGE
        t = self.time_elapsed / 100.
        dx = (self.initial_x_velocity * t)
        dy = (self.initial_y_velocity * t) - (.5 * GRAVITY * t**2)
        self.pos = self.origin[0] + dx, self.origin[1] - dy
        self.rect.center = self.pos
        
        if self.pos[1] > prepare.SCREEN_SIZE[1] + 50:
            self.kill()


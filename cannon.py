from math import degrees, pi, cos, sin
import pygame as pg

import prepare
from angles import get_angle, project
from gift import Gift


class Cannon(pg.sprite.Sprite):
    """A candy cane cannon that tracks the mouse."""
    def __init__(self, midbottom, *groups):
        super(Cannon, self).__init__(*groups)
        self.turret_base = pg.transform.scale(prepare.GFX["turret-base"], (75, 75))
        self.base_rect = self.turret_base.get_rect(midbottom=midbottom)
        self.barrel = prepare.GFX["cane-cannon"]
        self.fire_speed = 125
        
    def fire(self):
        """
        Return a Gift object positioned at the end of the cannon barrel.
        """
        prepare.SFX["explosion"].play()
        pos = project(self.base_rect.center, self.angle, 38)
        return Gift(pos, self.angle, self.fire_speed)
        
    def update(self, mouse_pos):
        """
        Set self.angle to the angle to the mouse unless mouse is underneath
        the turrret. Set self.image to the correctly rotated image.
        """
        angle = get_angle(self.base_rect.center, mouse_pos)
        if 1.75 * pi >= angle >= 1.5 * pi:
            angle = 1.75 * pi
        elif 1.25 * pi <= angle < 1.5 * pi:
            angle = 1.25 * pi
        self.angle = angle

        rotated_barrel = pg.transform.rotate(self.barrel, degrees(self.angle))
        barrel_rect = rotated_barrel.get_rect()
        surf = pg.Surface(barrel_rect.size)
        surf.fill((255, 0, 255))
        surf.set_colorkey((255, 0, 255))
        rect = pg.Rect((0, 0), self.base_rect.size)
        rect.center = barrel_rect.center
        surf.blit(rotated_barrel, (0, 0))
        surf.blit(self.turret_base, rect)
        self.image = surf
        self.rect = self.image.get_rect(center=self.base_rect.center)
        self.barrel_rect = barrel_rect
        self.barrel_rect.center = self.base_rect.center
        


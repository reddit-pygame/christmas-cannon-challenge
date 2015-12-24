from math import pi
from random import randint, choice

import pygame as pg

import prepare
from angles import project
from animation import Animation


names = ("darkgreen", "darkred", "antiquewhite",
                "green", "red")
COLORS = [pg.Color(name) for name in names]


class Firework(pg.sprite.Sprite):
    """A single firework that spawns particles when it explodes."""
    def __init__(self, pos, *groups):
        super(Firework, self).__init__(*groups)
        self.color = choice(COLORS)
        self.image = pg.Surface((3, 3))
        self.image.fill(self.color)
        self.rect = self.image.get_rect(center=pos)

    def explode(self, animations, fireworks, all_sprites):
        """Create a ring of firework particles that shoot outward and fade away."""
        prepare.SFX["explosion"].play()
        angles =  [.125 * x * pi for x in range(16)]
        duration = randint(750, 1500)
        distance =randint(150, 300)
        for angle in angles:
            destination = project(self.rect.center, angle, distance)
            dest = int(destination[0]), int(destination[1])
            shot = FireworkShot(self.rect.center, self.color, fireworks, all_sprites)
            move = Animation(centerx=dest[0], centery=dest[1], duration=duration, round_values=True)
            move.start(shot.rect)
            fade = Animation(alpha=0, duration=duration, round_values=True)
            fade.callback = shot.kill
            fade.start(shot)
            animations.add(move, fade)
        self.kill()


class FireworkShot(pg.sprite.Sprite):
    """A firework particle that fades out."""
    def __init__(self, pos, color, *groups):
        super(FireworkShot, self).__init__(*groups)
        self.image = pg.Surface((5, 5))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=pos)
        self.alpha = 255
        self.last_alpha = self.alpha

    def update(self):
        if self.last_alpha != self.alpha:
            self.image.set_alpha(self.alpha)
        self.last_alpha = self.alpha




from random import randint

import pygame as pg

from state_engine import GameState
import prepare
from labels import Label
from animation import Animation, Task
from level import Level
from cannon import Cannon
from building import Building
from fireworks import Firework


class Gameplay(GameState):
    """The gameplay pahse of the game."""
    def __init__(self):
        super(Gameplay, self).__init__()
        
    def startup(self, persistent):
        """
        Load the correct level based on the player's level attribute.
        """
        self.persist = persistent
        self.player = self.persist["player"]
        self.level = Level(self.player.level)
        pg.display.set_caption("{} - Level {}".format(prepare.ORIGINAL_CAPTION, self.player.level))
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.cannon = Cannon(self.level.turret_midbottom, self.all_sprites)
        self.gifts = pg.sprite.Group()
        self.make_buildings(self.level.building_info)
        self.all_sprites.clear(prepare.SCREEN, self.level.background)
        self.fireworks = pg.sprite.Group()
        self.animations = pg.sprite.Group()
        self.level_beat = False
        
    def make_buildings(self, building_info):
        self.buildings = pg.sprite.Group()
        for building_type, pos in building_info:
            Building(building_type, pos, self.buildings, self.all_sprites)
        
    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYUP:
            if event.key == pg.K_ESCAPE:
                self.quit = True
        elif event.type == pg.MOUSEBUTTONUP:
            if self.level_beat:
                self.leave_state()
            else:
                self.fire()
            
    def leave_state(self):
        self.done = True
        self.next_state = "LEVEL_COMPLETE"
    
    def fire(self):
        """Fire the cannon and add resulting Gift, if any, to the appropriate groups."""
        gift = self.cannon.fire()
        if gift:
            self.gifts.add(gift)
            self.all_sprites.add(gift)
            
    def update(self, dt):
        self.animations.update(dt)
        mouse_pos = pg.mouse.get_pos()
        self.cannon.update(mouse_pos)
        self.gifts.update(dt)
        self.buildings.update(dt, self.gifts)
        self.fireworks.update()
        for sprite in self.all_sprites:
            self.all_sprites.change_layer(sprite, sprite.rect.bottom)
        for gift in self.gifts:
            self.all_sprites.change_layer(gift, gift.rect.bottom + 1000)
        for firework in self.fireworks:
            self.all_sprites.change_layer(firework, firework.rect.bottom + 2000)
        if not self.level_beat and all((building.has_gift for building in self.buildings)):
            self.level_beat = True
            self.make_fireworks()
            if self.player.level > 1:
                task = Task(self.make_fireworks, 1500, self.player.level - 1)
                self.animations.add(task)
            finish = Task(self.leave_state, 5000 + (1500 * (self.player.level - 1)))
            self.animations.add(finish)
            
    def make_fireworks(self):
        for building in self.buildings:
            for _ in range(randint(3, 5)):
                pos = building.chimney_cap.center
                dest = pos[0] + randint(-30, 30), pos[1] - randint(200, 400)
                duration = randint(1000, 2000)
                delay = randint(0, 500)
                firework = Firework(pos, self.fireworks, self.all_sprites)
                ani = Animation(centerx=dest[0], centery=dest[1], duration=duration,
                                        delay=delay, round_values=True, transition="out_sine")
                ani.start(firework.rect)
                task = Task(firework.explode, (duration + delay) - 50,
                                   args=(self.animations, self.fireworks, self.all_sprites))
                self.animations.add(ani, task)
        
    def draw(self, surface):
        surface.blit(self.level.background, (0, 0))
        self.all_sprites.draw(surface)

        
        

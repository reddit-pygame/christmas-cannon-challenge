from random import choice, randint
from itertools import cycle

import pygame as pg

import tools
import prepare
from animation import Task

BASE_COLORS = {"siding": (192, 192, 192),
                            "seams": (168, 168, 168),
                            "moulding": (79, 90, 158)}
COLOR_SCHEMES = [
            ((183, 115, 69), (165, 104, 62), (24, 63, 7)),
            ((183, 115, 69), (165, 104, 62), (107, 18, 18)),
            ((255, 233, 127), (224, 203, 112), (107, 18, 18)),
            ((255, 233, 127), (224, 203, 112), (26, 86, 0))]

class Window(object):
    def __init__(self, rect):
        self.image = pg.Surface(rect.size)
        self.rect = rect
        self.image.fill(pg.Color("gray15"))
        
    def light_up(self):
        self.image.fill(pg.Color("goldenrod"))
        
    def draw(self, surface):
        surface.blit(self.image, self.rect)
        
        
class Building(pg.sprite.Sprite):
    building_info = {
            "ranch": {
                    "interior": (15, 61),
                    "chimney": ((78, 7), (22, 5)),
                    "lights": (2, 53),
                    "windows": []},
            "colonial": {
                    "interior": (14, 67),
                    "chimney": ((75, 8), (22, 5)),
                    "lights": (14, 67),
                    "windows": []},
            "gambrel": {
                    "interior": (11, 73),
                    "chimney": ((52, 1), (22, 5)),
                    "lights": (12, 73),
                    "windows": [(39, 39, 17, 17)]}        
            }            

    def __init__(self, building_type, midbottom, *groups):
        super(Building, self).__init__(*groups)
        d = self.building_info[building_type]
        img = prepare.GFX[building_type]
        
        num = randint(0, len(COLOR_SCHEMES))
        if num:
            colors = COLOR_SCHEMES[num - 1]
            names = "siding", "seams", "moulding"
            swaps = {BASE_COLORS[name]: color 
                           for name, color in zip(names, colors)} 
            self.body = tools.color_swap(img, swaps)
        else:
            self.body = img        
        self.rect = self.body.get_rect(midbottom=midbottom)
        
        interior = prepare.GFX["interior-{}".format(building_type)]
        self.interior_rect = interior.get_rect(topleft=d["interior"])
        self.dim_interior = pg.Surface(self.interior_rect.size)
        self.bright_interior = self.dim_interior.copy()
        self.dim_interior.fill(pg.Color("gray15"))
        self.bright_interior.fill(pg.Color("goldenrod"))
        self.dim_interior.blit(interior, (0, 0))
        self.bright_interior.blit(interior, (0, 0))
        self.interior = self.dim_interior
        windows = [pg.Rect(info) for info in d["windows"]]
        self.windows = [Window(rect) for rect in windows]
        self.bulbs = cycle([prepare.GFX["bulbs-dim-{}".format(building_type)],
                                    prepare.GFX["bulbs-bright-{}".format(building_type)]])
        self.bulb_img = next(self.bulbs)
        self.lights_rect = self.bulb_img.get_rect(topleft=d["lights"])
        x, y  = self.rect.topleft
        self.chimney_cap = pg.Rect((x + d["chimney"][0][0], 
                                                    y + d["chimney"][0][1]), 
                                                    d["chimney"][1])
        self.big_cap = self.chimney_cap.inflate(80, 80)
        self.bright = False
        self.animations = pg.sprite.Group()
        task = Task(self.blink_lights, randint(140, 170), -1)
        self.animations.add(task)
        self.blink_lights()
        
        self.has_gift = False

    def update(self, dt, gifts):
        self.animations.update(dt)
        for gift in gifts:
            if self.big_cap.colliderect(gift.rect):
                if self.chimney_cap.colliderect(gift.rect):
                    self.recieve_gift()
                    gift.kill()
                else:
                    oldx, oldy = gift.last_pos
                    newx, newy = gift.rect.center
                    dx = newx - oldx
                    dy = newy - oldy
                    width = abs(dx)
                    height = abs(dy)
                    rect = pg.Rect(oldx, oldy, width, height)
                    if dx < 0:
                        rect.move_ip(dx, 0)
                    if dy < 0:
                        rect.move_ip(0, dy)
                    if rect.colliderect(self.chimney_cap):
                        self.recieve_gift()
                        gift.kill()
                    
    def blink_lights(self):
        self.bulb_img = next(self.bulbs)
        self.make_image()
        
        
    def make_image(self):
        surf = pg.Surface(self.rect.size)
        surf.fill((255, 0, 255))
        surf.set_colorkey((255, 0, 255))
        surf.blit(self.interior, self.interior_rect)
        for window in self.windows:
            window.draw(surf)
        surf.blit(self.body, (0, 0))
        surf.blit(self.bulb_img, self.lights_rect)
        self.image = surf
        
    def recieve_gift(self):
        self.has_gift = True
        self.interior = self.bright_interior
        for window in self.windows:
            window.light_up()
        
        self.make_image()

        
    def draw(self, surface):
        surface.blit(self.image, self.rect)

import pygame as pg

import prepare
from state_engine import GameState
from labels import Label
from player import Player


class Splash(GameState):
    """
    Initial state of the game. Displays the title and adds a Player
    to the persistent dict.
    """
    def __init__(self):
        super(Splash, self).__init__()
        self.next_state = "GAMEPLAY"
        self.labels = pg.sprite.Group()
        centerx = prepare.SCREEN_RECT.centerx
        Label("Christmas Cannon", {"midtop": (centerx, 100)},
                self.labels, font_size=128, text_color="darkred")
        Label("Click anywhere to start playing", {"midbottom": (centerx, prepare.SCREEN_RECT.h - 50)},
                 self.labels, text_color="darkgreen", font_size=64)
        
    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYUP:
            if event.key == pg.K_ESCAPE:
                self.quit = True            
        elif event.type == pg.MOUSEBUTTONUP:
            self.done = True
            self.persist["player"] = Player()
        
    def draw(self, surface):
        surface.fill(pg.Color("white"))
        self.labels.draw(surface)
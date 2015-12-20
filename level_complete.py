import pygame as pg

import prepare
from state_engine import GameState
from labels import Label
from level import LEVELS


class LevelComplete(GameState):
    def __init__(self):
        super(LevelComplete, self).__init__()
        self.next_state = "GAMEPLAY"
        
    def startup(self, persistent):
        self.persist = persistent
        player = self.persist["player"]
        level_passed = player.level
        player.level += 1
        max_level = max(LEVELS)
        if player.level > max_level:
            player.level = 1
            
        screen_rect = prepare.SCREEN_RECT    
        self.labels = pg.sprite.Group()
        text = "Level {} Complete!".format(level_passed)
        Label(text, {"midtop": (screen_rect.centerx, 100)}, 
                self.labels, text_color="darkred", font_size=64)
        Label("Click anywhere to start the next level", 
                {"midtop": (screen_rect.centerx, 650)}, 
                self.labels, text_color="darkgreen", font_size=32)
                
    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.MOUSEBUTTONUP:
            self.done = True
            
    def update(self, dt):
        pass
        
    def draw(self, surface):
        surface.fill(pg.Color("antiquewhite"))
        self.labels.draw(surface)
        return prepare.SCREEN_RECT
        
        
import sys
import pygame as pg

from state_engine import Game, GameState
import prepare
import splash, gameplay, level_complete

states = {"SPLASH": splash.Splash(),
              "GAMEPLAY": gameplay.Gameplay(),
              "LEVEL_COMPLETE": level_complete.LevelComplete()}
game = Game(prepare.SCREEN, states, "SPLASH")
game.run()
pg.quit()
sys.exit()
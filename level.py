import pygame as pg

import prepare


LEVELS = {
        2: ((50, 500), 10, 100,  
            [("ranch", (1210, 382)),
             ("colonial", (953, 406)),
             ("gambrel", (1082, 489)),
             ("ranch", (872, 533)),
             ("ranch", (1195, 633)),
             ("ranch", (984, 667)),
             ("ranch", (754, 673))]),
        3: ((50, 235), 10, 100,
            [("ranch", (574, 519)),
             ("ranch", (1052, 491)),
             ("ranch", (557, 688)),
             ("ranch", (760, 690)),
             ("ranch", (1194, 621)),
             ("colonial", (395, 556)),
             ("colonial", (1034, 700)),
             ("gambrel", (804, 546)),
             ("gambrel", (1216, 459))]),
        1: ((50, 650), 10, 100,
            [("ranch", (537, 700)),
             ("ranch", (889, 690)),
             ("ranch", (1030, 658)),
             ("colonial", (1190, 646)),
             ("colonial", (714, 676))]),   
        4: ((55, 660), 10, 100,
           [("ranch", (470, 700)),
             ("ranch", (535, 504)),
             ("ranch", (827, 542)),
             ("ranch", (831, 694)),
             ("ranch", (1012, 691)),
             ("ranch", (1006, 511)),
             ("ranch", (1183, 480)),
             ("ranch", (1200, 296)),
             ("colonial", (769, 398)),
             ("colonial", (996, 341)),
             ("colonial", (1185, 692)),
             ("gambrel", (674, 693))]),
        5: ((640, 700), 10, 100,
           [("ranch", (232, 288)),
             ("ranch", (66, 576)),
             ("ranch", (79, 706)),
             ("ranch", (272, 713)),
             ("ranch", (1196, 203)),
             ("ranch", (1066, 293)),
             ("ranch", (1202, 573)),
             ("ranch", (1175, 703)),
             ("colonial", (66, 278)),
             ("colonial", (93, 444)),
             ("colonial", (388, 630)),
             ("colonial", (975, 703)),
             ("colonial", (990, 491)),
             ("gambrel", (318, 418)),
             ("gambrel", (1170, 438))])
    }             


class Level(object):
    def __init__(self, level_num): 
        self.level_num = level_num
        L = LEVELS[level_num]
        self.turret_midbottom = L[0]
        self.num_shots = L[1]
        self.ball_bonus = L[2]
        self.building_info = L[3]
        self.make_background()
        
    def make_background(self):    
        self.background = pg.Surface(prepare.SCREEN_SIZE)
        r, g, b = 5, 5, 10
        for y in range(0, 721, 10):
            rect = pg.Rect(0, y, 1280, 10)
            self.background.fill((r, g, b), rect)
            r += 1
            g += 1
            b += 2
        ground = prepare.GFX["level{}".format(self.level_num)]
        ground_rect = ground.get_rect()
        ground_rect.bottom = self.background.get_size()[1]
        self.background.blit(ground, ground_rect)
        
    def check_high_score(self, player):
        score = sum((b.score for b in self.buildings))
        score += player.shots_left * self.ball_bonus
        high = self.high_scores.get(self.level_num, 0)
        
        

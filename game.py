import pygame as pg
import sys
import time
from bird import Bird
pg.init()

# 600 , 768

class Game:
    def __init__(self):
        # setting window config
        self.width = 400 
        self.height = 512
        self.scale_factor=1
        self.win = pg.display.set_mode((self.width, self.height))
        self.clock = pg.time.Clock()
        self.move_speed=150
        self.bird=Bird(self.scale_factor)
        self.is_enter_pressed=False
        self.setUpBgAndGround()

        self.gameLoop()

    def gameLoop(self):
        last_time = time.time()
        while True:
            # calculating delta time
            new_time = time.time()
            delta_time = new_time - last_time
            last_time = new_time
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if event.key==pg.K_RETURN:
                        self.is_enter_pressed=True
                    if event.key==pg.K_SPACE and self.is_enter_pressed:#start flapping only game has started
                        self.bird.flap(delta_time)

            self.updateEverything(delta_time)
            self.drawEverything()
            pg.display.update()
            # limit fps to 60 to control gameloop
            self.clock.tick(60)


    def updateEverything(self,delta_time):
        if self.is_enter_pressed:
            self.ground1_rect.x -= self.move_speed*delta_time
            self.ground2_rect.x -= self.move_speed*delta_time

            if(self.ground1_rect.right<0):
                self.ground1_rect.x=self.ground2_rect.right
            if(self.ground2_rect.right<0):
                self.ground2_rect.x=self.ground1_rect.right

            self.bird.update(delta_time)


    def drawEverything(self):
        self.win.blit(self.bg_img, (0,-200))
        self.win.blit(self.ground1_img, self.ground1_rect)
        self.win.blit(self.ground2_img, self.ground2_rect)
        self.win.blit(self.bird.image, self.bird.rect)

    def setUpBgAndGround(self):
         # loading img for bg and ground
        self.bg_img=pg.transform.scale_by(pg.image.load("assets/bg.png").convert(),self.scale_factor)
        self.ground1_img=pg.transform.scale_by(pg.image.load("assets/ground.png").convert(),self.scale_factor)
        self.ground2_img=pg.transform.scale_by(pg.image.load("assets/ground.png").convert(),self.scale_factor)
        # getting rect of ground
        self.ground1_rect=self.ground1_img.get_rect()
        self.ground2_rect=self.ground2_img.get_rect()

        self.ground1_rect.x=0
        self.ground2_rect.x=self.ground1_rect.right

        self.ground1_rect.y=379
        self.ground2_rect.y=379
        

game=Game()
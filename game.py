import pygame as pg
import sys
import time
from bird import Bird
from pipe import Pipe

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
        self.pipes = []
        self.pipe_generate_counter = 71
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
                        self.bird.update_on=True
                    if event.key==pg.K_SPACE and self.is_enter_pressed:#start flapping only game has started
                        self.bird.flap(delta_time)

            self.updateEverything(delta_time)
            self.checkCollision()
            self.drawEverything()
            pg.display.update()
            # limit fps to 60 to control gameloop
            self.clock.tick(60)

    def checkCollision(self):
        # if pipes are available in list then start checking collision
        if len(self.pipes):
        # stop when we hit bottom or we hit pipes
            if self.bird.rect.bottom>379:
                self.bird.update_on=False #stop applying gravity
                self.is_enter_pressed=False
            if (self.bird.rect.colliderect(self.pipes[0].rect_up) or
            self.bird.rect.colliderect(self.pipes[0].rect_down)):
                self.is_enter_pressed=False

    def updateEverything(self,delta_time):
        if self.is_enter_pressed:
            self.ground1_rect.x -= self.move_speed*delta_time
            self.ground2_rect.x -= self.move_speed*delta_time
            # Logic to move ground
            if(self.ground1_rect.right<0):
                self.ground1_rect.x=self.ground2_rect.right
            if(self.ground2_rect.right<0):
                self.ground2_rect.x=self.ground1_rect.right
            # Generating pipes
            if(self.pipe_generate_counter>70):
                self.pipes.append(Pipe(self.scale_factor, self.move_speed))
                self.pipe_generate_counter=0
            self.pipe_generate_counter+=1
            # Moving the pipes
            for pipe in self.pipes:
                pipe.update(delta_time)
            # Removing pipes that are out of screen
            if len(self.pipes) != 0:
                if self.pipes[0].rect_up.right<0:
                    self.pipes.pop(0)
        # Moving the bird
        self.bird.update(delta_time)


    def drawEverything(self):
        self.win.blit(self.bg_img, (0,-200))
        for pipe in self.pipes:
            pipe.drawPipe(self.win)
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
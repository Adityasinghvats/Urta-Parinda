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
        self.title = pg.display.set_caption("Flappy Bird")
        self.clock = pg.time.Clock()
        self.move_speed=150
        self.bird=Bird(self.scale_factor)
        self.start_monitoring = False
        self.is_enter_pressed=False
        self.is_game_started=True
        self.score=0
        self.font=pg.font.Font("assets/arial.ttf",20)
        self.score_text=self.font.render("Score: 0 ", True, (255,255,255))
        self.score_rect=self.score_text.get_rect(center=(70,25))
        self.restart_text=self.font.render("RESTART", True, (0,0,0))
        self.restart_text_rect=self.score_text.get_rect(center=(200,460))
        self.start_text=self.font.render("PRESS ENTER TO START", True, (0,0,0))
        self.start_text_rect=self.score_text.get_rect(center=(110,460))
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
                if event.type == pg.KEYDOWN and self.is_game_started:
                    if event.key==pg.K_RETURN:
                        self.is_enter_pressed=True
                        self.bird.update_on=True
                    if event.key==pg.K_SPACE and self.is_enter_pressed:#start flapping only game has started
                        self.bird.flap(delta_time)
                if event.type == pg.MOUSEBUTTONUP:
                    if self.restart_text_rect.collidepoint(pg.mouse.get_pos()):
                        self.restartGame()

            self.updateEverything(delta_time)
            self.checkCollision()
            self.checkScore()
            self.drawEverything()
            pg.display.update()
            # limit fps to 60 to control gameloop
            self.clock.tick(60)


    def restartGame(self):
        self.score=0
        self.score_text=self.font.render("Score: 0 ", True, (255,255,255))
        self.is_enter_pressed=False
        self.is_game_started=True
        self.bird.resetPosition()
        self.pipes.clear()
        self.pipe_generate_counter=71
        self.bird.update_on=False

    def checkScore(self):
        if len(self.pipes):
            # check if bird is inside the pipe
            if (self.bird.rect.left > self.pipes[0].rect_down.left and
            self.bird.rect.right < self.pipes[0].rect_down.right and
            not self.start_monitoring):
                self.start_monitoring=True
            if self.bird.rect.left > self.pipes[0].rect_down.right and self.start_monitoring:
                self.start_monitoring=False
                self.score += 1
                self.score_text = self.font.render(f"Score: {self.score}", True, (255,255,255))

    def checkCollision(self):
        # if pipes are available in list then start checking collision
        if len(self.pipes):
        # stop when we hit bottom or we hit pipes
            if self.bird.rect.bottom>379:
                self.bird.update_on=False #stop applying gravity
                self.is_enter_pressed=False
                self.is_game_started=False
            if (self.bird.rect.colliderect(self.pipes[0].rect_up) or
            self.bird.rect.colliderect(self.pipes[0].rect_down)):
                self.is_enter_pressed=False
                self.is_game_started=False

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
        self.win.blit(self.score_text,self.score_rect)
        if not self.is_enter_pressed and self.is_game_started:
            self.win.blit(self.start_text, self.start_text_rect)
        if not self.is_game_started:
            self.win.blit(self.restart_text, self.restart_text_rect)

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
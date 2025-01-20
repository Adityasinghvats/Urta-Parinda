import pygame as pg


class Bird(pg.sprite.Sprite):
    def __init__(self,scale_factor):
        super().__init__()
        # convert_alpha to convert with transparency
        self.scale_factor=scale_factor
        self.img_list = [pg.transform.scale_by(pg.image.load("assets/birdup.png").convert_alpha(),self.scale_factor),
                        pg.transform.scale_by(pg.image.load("assets/birddown.png").convert_alpha(),self.scale_factor)]
        self.img_idx=0 # 0 for up and 1 for down
        self.image=self.img_list[self.img_idx]
        self.rect = self.image.get_rect(center=(100,100))
        self.y_velocity=0
        self.gravity=10
        self.flap_speed=250
        self.anim_counter=0

    def update(self, delta_time):
        self.playAnimation()
        self.applyGravity(delta_time)

        if self.rect.y<=0:
            self.rect.y=0
            self.flap_speed=0
        elif self.rect.y>=0 and self.flap_speed==0:
            self.flap_speed=250

    def applyGravity(self, delta_time):
        self.y_velocity += self.gravity*delta_time
        self.rect.y += self.y_velocity

    # responsible for sending up on keypress
    def flap(self, dt):
        self.y_velocity =-self.flap_speed*dt

    def playAnimation(self):
        if(self.anim_counter==5):
            self.image=self.img_list[self.img_idx]
            if self.img_idx==0: self.img_idx=1
            else: self.img_idx=0
            self.anim_counter=0
        self.anim_counter+=1

import pygame
import random

pygame.init()
screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
clock=pygame.time.Clock()
width,height=screen.get_size()
length=500
bg=pygame.image.load("physics/bg.jpg")
bg=pygame.transform.scale(bg,(width,height))
# simulation thingys
fps=60
frame_count = 0

class Ball:
    def __init__(self):
        self.x,self.y,self.z=width//2,height//2,length//2
        self.vx,self.vy,self.vz=0,0,0
        self.color=(random.randint(0,255),random.randint(0,255),random.randint(0,255))  
        self.rect=None
        self.radius=15
    def update(self):
        self.x+=self.vx
        self.y+=self.vy
        self.z+=self.vz

        # boundries
        if self.x<self.radius or self.x>width-self.radius:
            self.vx=0
            self.x=max(self.radius,min(self.x,width-self.radius))
        if self.y<self.radius or self.y>height-self.radius:
            self.vy=0
            self.y=max(self.radius,min(self.y,height-self.radius))
        if self.z<self.radius or self.z>length-self.radius:
            self.vz=0
            self.z=max(self.radius,min(self.z,length-self.radius))
            self.y-=self.vy
    def display(self,screen:'pygame.Surface'):
        self.radius=0.5*self.z+10
        self.rect=pygame.draw.circle(screen,self.color,(self.x,self.y),self.radius)


ball=Ball()
running=True
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT: running=False
        if(event.type==pygame.KEYDOWN):
            if(event.key==pygame.K_SPACE):
                ball.vy=-20 # jump
            if(event.key==pygame.K_LSHIFT):
                ball.vy=20
            # wasd
            if(event.key==pygame.K_w):
                ball.vz-=10
                ball.vy=-1
            if(event.key==pygame.K_s):
                ball.vz+=10
                ball.vy=1
            if(event.key==pygame.K_a):
                ball.vx-=10
            if(event.key==pygame.K_d):
                ball.vx+=10
        if(event.type==pygame.KEYUP):
            if(event.key==pygame.K_w or event.key==pygame.K_s):
                ball.vz=0
                ball.vy=0
            if(event.key==pygame.K_a or event.key==pygame.K_d):
                ball.vx=0
            if(event.key==pygame.K_SPACE or event.key==pygame.K_LSHIFT):
                ball.vy=0
    screen.blit(bg,(0,0))
    ball.update()
    ball.display(screen)
    pygame.display.flip()
    clock.tick(fps)
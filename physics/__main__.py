import pygame
import random

pygame.init()
screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
clock=pygame.time.Clock()
width,height=screen.get_size()

# simulation thingys
fps=60
frame_count = 0
g=5
radius=20

class Ball:
    def __init__(self):
        self.x,self.y=width//2,height//2
        self.vx,self.vy=random.randint(-50,50),random.randint(-50,50)
        self.color=(random.randint(0,255),random.randint(0,255),random.randint(0,255))  
        self.rect=None
    def update(self):
        global g
        self.vx*=0.99
        self.vy+=g
        self.vy*=0.99
        self.x+=self.vx
        self.y+=self.vy
        if self.x <= radius:
            self.x = radius
            self.vx *= -0.9
        elif self.x >= width-radius:
            self.x = width-radius
            self.vx *= -0.9

        if self.y <= radius:
            self.y = radius
            self.vy *= -0.9
        elif self.y >= height-radius:
            self.y = height-radius
            self.vy *= -0.9
    def display(self,screen:'pygame.Surface'):
        self.rect=pygame.draw.circle(screen,self.color,(self.x,self.y),radius)


balls=[]
running=True
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT: running=False
        if(event.type==pygame.KEYDOWN):
            if(event.key==pygame.K_SPACE):
                balls.append(Ball())
    screen.fill("#1D1D1D")
    for ball in balls:
        ball.update()
        ball.display(screen)
    pygame.display.flip()
    clock.tick(fps)
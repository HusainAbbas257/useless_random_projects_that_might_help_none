import math

import pygame
import random

pygame.init()
screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
clock=pygame.time.Clock()
width,height=screen.get_size()

# simulation thingys
fps=60
frame_count = 0
g=500

class Ball:
    def __init__(self):
        self.x,self.y=width//2,height//2
        self.vx,self.vy=random.randint(-500,500),random.randint(-500,500)
        self.color=(random.randint(0,255),random.randint(0,255),random.randint(0,255))  
        self.radius=random.randint(10,30)
        self.rect=None
        self.mass=self.radius**3 * 0.001
    def update(self,fps=fps):
        global g
        self.vx*=0.999
        self.vy+=g*(1/fps)
        self.vy*=0.999
        self.x+=self.vx*(1/fps)
        self.y+=self.vy*(1/fps)
        if self.x <= self.radius:
            self.x = self.radius
            self.vx *= -0.99
        elif self.x >= width-self.radius:
            self.x = width-self.radius
            self.vx *= -0.99

        if self.y <= self.radius:
            self.y = self.radius
            self.vy *= -0.99
        elif self.y >= height-self.radius:
            self.y = height-self.radius
            self.vy *= -0.99
    def collision(self,other:'Ball'):
        # i have to write a beatifull collision algorithm here
        # but for now just push them apart a bit and assume a perfectly elastic collision
        dx=self.x-other.x
        dy=self.y-other.y
        distance=math.sqrt(dx**2+dy**2)
        if distance<self.radius+other.radius:
            # push them apart 
            overlap=self.radius+other.radius-distance
            self.x+=overlap*(dx/distance)/2
            self.y+=overlap*(dy/distance)/2
            other.x-=overlap*(dx/distance)/2
            other.y-=overlap*(dy/distance)/2
            
            self.vx,other.vx=other.vx,self.vx
            self.vy,other.vy=other.vy,self.vy
            # i just realised that mass is not being used at all, so i will just ignore it for now
    def display(self,screen:'pygame.Surface'):
        self.rect=pygame.draw.circle(screen,self.color,(self.x,self.y),self.radius)


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
        ball.update(clock.get_fps())
        
        for other in balls:
            if ball!=other:
                ball.collision(other)
        ball.display(screen)
    # a simple fps counter
    screen.blit(pygame.font.Font(None, 30).render(f"FPS: {int(clock.get_fps())},    Balls: {len(balls)}", True, (255, 255, 255)), (10, 10))
    pygame.display.flip()
    clock.tick(fps)
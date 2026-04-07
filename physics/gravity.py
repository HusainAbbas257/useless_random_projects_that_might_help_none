# imports
import math
import pygame
import random
from vector import *

# pygame setup-
pygame.init()
screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
clock=pygame.time.Clock()
width,height=screen.get_size()

# helper funciton 
def color(prev:tuple[int,int,int])->tuple[int,int,int]:
    color = pygame.Color(prev)
    hsva=(color.hsva)
    hue=hsva[0]+random.randint(5,10)
    hue=hue%360
    color.hsva=(hue,hsva[1],100,hsva[3])
    return color.r,color.g,color.b

# simulation thingys
fps=60
frame_count = 0
g=700
class Ball:
    '''A ball class to implement all the basic properties of the ball'''
    def __init__(self,x,y,r=5):
        '''initializes the ball with random velocity and color and mass based on radius'''
        
        self.pos=position(x,y) # start from the center top of the screen
        
        self.vel=velocity(random.randint(-20,20),random.randint(-20,20))
        self.color=(random.randint(0,255),random.randint(0,255),random.randint(0,255))
        self.radius=r
        self.mass=(4/3)*math.pi*self.radius**3*0.0001
        self.force=force(0,0)
        
    def update(self,fps=fps):
        '''updates the position and velocity of the ball based on gravity and friction and also checks for collision with walls'''
        fps=max(fps,0.001) # to avoid /0
        # change color for rainbow effect
        self.color=color(self.color)
        acc=self.force/self.mass
        self.vel+=acc*(1/fps)
        self.force=force(0,0)
        # distance=speed*time so:
        self.pos.x+=self.vel.x*(1/fps)
        self.pos.y+=self.vel.y*(1/fps)
        
    def collision(self,other:'Ball'):
        '''handles collision between two balls and also checks if they are on top of each other to apply normal force'''
        
        # distance between the centers of the two balls
        dx=self.pos.x-other.pos.x
        dy=self.pos.y-other.pos.y
        distance=math.sqrt(dx**2+dy**2)
        distance=max(distance,0.001) #to avoid /0
        
        if distance<self.radius+other.radius:#check for collison
            self.vel*=0.5
            other.vel*=0.5
            self.radius=min((self.radius**3+other.radius**3)**(1/3),10) # increase the radius of the ball to make it look like they merged
            self.mass=(4/3)*math.pi*self.radius**3*0.0001
            return True
        return False
            
            
    def display(self,screen:'pygame.Surface'):
        '''displays the ball on the screen'''
        self.rect=pygame.draw.circle(screen,self.color,(self.pos.x,self.pos.y),self.radius)


balls=[] # list to store all the balls
blackhole=Ball(width//2,height//2,30) # a big ball in the center to act as a black hole that attracts all the other balls with its gravity
blackhole.vel=velocity(0,0) # it should not move
running=True

while running:#mainloop
    
    # event handling
    for event in pygame.event.get():
        if event.type==pygame.QUIT: running=False
        # check for click
        if event.type==pygame.MOUSEBUTTONDOWN:
            x,y=pygame.mouse.get_pos()
            balls.append(Ball(x,y))
                    
    # background
    screen.fill("#1D1D1D")
    
    # ball handling
    for ball in balls[:]:
        ball.update(clock.get_fps())
        for other in balls[:]+[blackhole]:
            if ball!=other:
                # add its gravity force to it
                direction=other.pos-ball.pos
                distance=direction.scaler()
                if distance>0:
                    force_magnitude=g*ball.mass*other.mass/(distance/5)**2
                    ball.force+=direction.unit()*force_magnitude
                c=ball.collision(other)
                if c:
                    balls.remove(ball if ball.radius<other.radius else other) 
        ball.display(screen)
        blackhole.update(clock.get_fps())
        blackhole.display(screen)
        
    # a simple fps counter
    screen.blit(pygame.font.Font(None, 30).render(f"FPS: {int(clock.get_fps())},    Balls: {len(balls)}", True, (255, 255, 255)), (10, 10))
    
    # update the display and tick the clock
    pygame.display.flip()
    clock.tick(fps)
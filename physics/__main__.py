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
g=acceleration(0,600)
class Ball:
    '''A ball class to implement all the basic properties of the ball'''
    def __init__(self):
        '''initializes the ball with random velocity and color and mass based on radius'''
        
        self.pos=position(width//2,height//4) # start from the center top of the screen
        
        self.vel=velocity(random.randint(-500,500),random.randint(-500,500)) # random velocity in both x and y direction
        self.color=(random.randint(0,255),random.randint(0,255),random.randint(0,255))  # random color for the ball later it gets the rainbow effect
        
        # since mass logic is yet to be implemed make radius constant
        self.radius=15
        
        self.rect=None #stored rect thinking i would use it but found out that it is not needed but still keeping it for absoluely no reason
        
        self.mass=(4/3)*math.pi*self.radius**3*0.0001 #basic formula for mass of a sphere with density 0.0001 to make it look good
        
        self.normal=False #wether a normal force acting on it or not
        
    def update(self,fps=fps):
        '''updates the position and velocity of the ball based on gravity and friction and also checks for collision with walls'''
        global g
        
        # change color for rainbow effect
        self.color=color(self.color)
        
        self.vel*=0.99 # air resistance
        
        # gravity gets cancelled out by the normal force when the ball is on the ground so only apply gravity when it is not on the ground
        if not self.normal:
            self.vel+=g*(1/fps)
        
        # checking if its on ground
        if(self.pos.x<=self.radius*1.1 ): #a little more to take in the edge cases
            # apply friction
            self.normal=True
            
            self.vel.x*=0.85 # assuming friction only effects x direction for simplicity
        else:
            self.normal=False
        
        # distance=speed*time so:
        self.pos.x+=self.vel.x*(1/fps)
        self.pos.y+=self.vel.y*(1/fps)
        
        # boundry collision:
        if self.pos.x <= self.radius:# left wall
            self.pos.x = self.radius
            self.vel.x *= -0.9
        elif self.pos.x >= width-self.radius:# right wall
            self.pos.x = width-self.radius
            self.vel.x *= -0.9

        if self.pos.y <= self.radius:# top wall
            self.pos.y = self.radius
            self.vel.y *= -0.9
        elif self.pos.y >= height-self.radius:# bottom wall
            self.pos.y = height-self.radius
            self.vel.y *= -0.9
        
        # rounding off to avoid jitter
        self.vel.roundoff()
    def collision(self,other:'Ball'):
        '''handles collision between two balls and also checks if they are on top of each other to apply normal force'''
        
        # distance between the centers of the two balls
        dx=self.pos.x-other.pos.x
        dy=self.pos.y-other.pos.y
        distance=math.sqrt(dx**2+dy**2)
        distance=max(distance,0.001) #to avoid /0
        
        if distance<self.radius+other.radius:#check for collison
            
            # normal vector 
            normal_vec=(other.pos-self.pos)/distance 
            # tangent vector
            tangent_vec=normal_vec.tangent()
            
            # decomposing the velocity of both balls into normal and tangent components
            normal_component_self=self.vel.dot(normal_vec)
            normal_component_other=other.vel.dot(normal_vec)
            tangent_component_self=self.vel.dot(tangent_vec)
            tangent_component_other=other.vel.dot(tangent_vec)
            
            # damping velocity is unrealisti just damp normal component to make it look better
            normal_component_other*=0.8
            normal_component_self*=0.8
            
            
            # new formulas assuming masses are same and perfectly elastic
            self.vel.x=tangent_component_self*tangent_vec.x+normal_component_other*normal_vec.x
            self.vel.y=tangent_component_self*tangent_vec.y+normal_component_other*normal_vec.y
            other.vel.x=tangent_component_other*tangent_vec.y+normal_component_self*normal_vec.y
            other.vel.y=tangent_component_other*tangent_vec.y+normal_component_self*normal_vec.y
            
            
            # push them apart 
            overlap=self.radius+other.radius-distance
            self.pos.x+=overlap*(dx/distance)/2
            self.pos.y+=overlap*(dy/distance)/2
            other.pos.x-=overlap*(dx/distance)/2
            other.pos.y-=overlap*(dy/distance)/2
            
            # check if it is on top of other :
            if(self.pos.y>other.pos.y and distance*1.01<self.radius+other.radius and abs(dx)<self.radius+other.radius and abs(dy)<self.radius+other.radius):
                self.normal=other.normal
            else:
                self.normal=False
            if(other.pos.y>self.pos.y and abs(dx)<self.radius+other.radius and abs(dy)<self.radius+other.radius and distance*1.01<self.radius+other.radius):
                other.normal=self.normal
            else:
                other.normal=False
            
    def display(self,screen:'pygame.Surface'):
        '''displays the ball on the screen'''
        self.rect=pygame.draw.circle(screen,self.color,(self.pos.x,self.pos.y),self.radius)


balls=[] # list to store all the balls
running=True
while running:#mainloop
    
    # event handling
    for event in pygame.event.get():
        if event.type==pygame.QUIT: running=False
        if(event.type==pygame.KEYDOWN):
            if(event.key==pygame.K_SPACE):# space for 5 balls
                for _ in range(5):
                    balls.append(Ball())
                    
    # background
    screen.fill("#1D1D1D")
    
    # ball handling
    for ball in balls:
        ball.update(clock.get_fps())
        for other in balls:
            if ball!=other:
                ball.collision(other)
        ball.display(screen)
        
    # a simple fps counter
    screen.blit(pygame.font.Font(None, 30).render(f"FPS: {int(clock.get_fps())},    Balls: {len(balls)}", True, (255, 255, 255)), (10, 10))
    
    # update the display and tick the clock
    pygame.display.flip()
    clock.tick(fps)
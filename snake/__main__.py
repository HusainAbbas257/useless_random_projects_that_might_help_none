import pygame
pygame.init()
import random
import math

screen = pygame.display.set_mode((985,745))
width,height=screen.get_size()
clock = pygame.time.Clock()
fps=120



class Board:
    def __init__(self,x,y):
        self.x,self.y=x,y
        self.board=[[0 for i in range(x)] for j in range(y)]
        self.w,self.h=24,24
        self.snakes=[]
    def update(self):
        self.board=[[0 for i in range(self.x)] for j in range(self.y)]
        n_empty=[]
        for s in self.snakes:
            s.update()
            n_empty.extend(s.body)
        for b in n_empty:
            self.board[b[0]][b[1]]=1
            
        
    def display(self,screen:'pygame.Surface'):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):

                r=pygame.Rect(0,0,self.w,self.h)
                r.center=(self.w*(i)+self.w,self.h*(j)+self.h)
                pygame.draw.rect(screen, '#ffffff'if self.board[i][j]==0 else '#000000', r)
class Snake:
    def __init__(self,x=1,y=1):
        
        self.head=[x,y]
        self.body=[self.head,[1,0]]
        self.direction='s'
    def update(self):
        for i in range(len(self.body)):
            match self.direction:
                case 's':
                    self.body[i][1]+=1
                case 'w':
                    self.body[i][1]-=1
                case 'a':
                    self.body[i][0]-=1
                case 'd':
                    self.body[i][0]+=1

            if self.body[i][0]<0:
                self.body[i][0]=40+self.body[i][0]
            if self.body[i][0]>=40:
                self.body[i][0]=40-self.body[i][0]

            if self.body[i][1]<0:
                self.body[i][1]=30+self.body[i][1]
            if self.body[i][1]>=30:
                self.body[i][1]=30-self.body[i][1]
    
s=Snake()
b=Board(30,40)
b.snakes=[s]
running=True
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT: running=False
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_w:
                s.direction='w'
            if event.key==pygame.K_s:
                s.direction='s'
            if event.key==pygame.K_a:
                s.direction='a'
            if event.key==pygame.K_d:
                s.direction='d'
    screen.fill("#3f2fce")
    b.update()
    b.display(screen)
    pygame.display.flip()
    clock.tick(fps)

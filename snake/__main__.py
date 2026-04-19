import pygame
pygame.init()
import random
import math

screen = pygame.display.set_mode((985,745))
width,height=screen.get_size()
clock = pygame.time.Clock()
fps=30



class Board:
    def __init__(self,x,y):
        self.x,self.y=x,y
        self.board=[[((i+j)%2) for i in range(x)] for j in range(y)]
        self.w,self.h=24,24
    def display(self,screen:'pygame.Surface'):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):

                self.board[i][j]=0 if self.board[i][j]==1 else 1
                r=pygame.Rect(0,0,self.w,self.h)
                r.center=(self.w*(i)+self.w,self.h*(j)+self.h)
                pygame.draw.rect(screen, '#ffffff'if self.board[i][j]==0 else '#000000', r)
class Snake:
    def __init__(self,x=1,y=1):
        self.head=(x,y)
        self.body=[self.head,]
        self.direction='s'
    

b=Board(30,40)
running=True
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT: running=False
    screen.fill("#3f2fce")
    b.display(screen)
    pygame.display.flip()
    clock.tick(fps)

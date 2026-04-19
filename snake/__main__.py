import pygame
pygame.init()
import random
import math

screen = pygame.display.set_mode((985,745))
width,height=screen.get_size()
clock = pygame.time.Clock()
fps=15


class Board:
    def __init__(self,x,y):
        self.x,self.y=x,y
        self.board=[[0 for i in range(x)] for j in range(y)]
        self.w,self.h=24,24
        self.snakes:list['Snake']=[]
        self.apple=[random.randint(0,39),random.randint(0,29)]
    def update(self):
        self.board=[[0 for i in range(self.x)] for j in range(self.y)]
        n_empty=[]
        for s in self.snakes:
            n_empty.extend(s.update())
            if(s.head.pos==self.apple):
                 print('eating one apple')
                 s.eat()
                 self.apple=[random.randint(0,39),random.randint(0,29)]
                 print(self.apple)
        for b in n_empty:
            self.board[b[0]][b[1]]=1
        self.board[self.apple[0]][self.apple[1]]=5
        
    def display(self,screen:'pygame.Surface'):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):

                r=pygame.Rect(0,0,self.w,self.h)
                r.center=(self.w*(i)+self.w,self.h*(j)+self.h)
                pygame.draw.rect(screen,{0:"#7f748d",1:"#2B8D3C",5:"#813131"}[self.board[i][j]], r)
class cell:
    def __init__(self,x,y,next,direction=None):
        self.pos:list[int,int]=[x,y]
        self.direction=direction
        self.next=next
    def update(self):
        match self.direction:
                case 's':
                    self.pos[1]+=1
                case 'w':
                    self.pos[1]-=1
                case 'a':
                    self.pos[0]-=1
                case 'd':
                    self.pos[0]+=1

        if self.pos[0]<0:
                self.pos[0]=40+self.pos[0]
        if self.pos[0]>=40:
                self.pos[0]=40-self.pos[0]

        if self.pos[1]<0:
                self.pos[1]=30+self.pos[1]
        if self.pos[1]>=30:
                self.pos[1]=30-self.pos[1]
class Snake:
    def __init__(self,x=1,y=1):
        
        self.head=cell(0,5,None,'s')
        self.tail=cell(0,1,self.head,'s')
        self.body=[self.head]
        for i in range(2,10):
            c=cell(0,i,self.body[-1],'s')
            self.body.append(c)
            self.tail=c
        self.direction='s'
    def update(self):
        # only updating head and making others follow their next
        c=self.tail
        while c.next!=None:
            c.pos=c.next.pos.copy()
            c=c.next
        self.head.update()
        return [c.pos for c in self.body]
    def eat(self):
        c=cell(self.tail.pos[0],self.tail.pos[1]+1,self.body[-1],'s')
        c.update()
        self.body.append(c)
        self.tail=c
    
s=Snake()
b=Board(30,40)
b.snakes=[s]
running=True
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT: running=False
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_w and s.head.direction!='s':
                s.head.direction='w'
            if event.key==pygame.K_s and s.head.direction!='w'  :
                s.head.direction='s'
            if event.key==pygame.K_a and s.head.direction!='d'  :
                s.head.direction='a'
            if event.key==pygame.K_d and s.head.direction!='a':
                s.head.direction='d'
    screen.fill("#3f2fce")
    b.update()
    b.display(screen)
    pygame.display.flip()
    clock.tick(fps)

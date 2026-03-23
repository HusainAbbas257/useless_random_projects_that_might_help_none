import random, pygame
pygame.init()

screen = pygame.display.set_mode((800,600))
clock = pygame.time.Clock()

class Aircraft:
    def __init__(self,type_='fighter'):
        self.type_=type_
        self.health={'fighter':100,'civilian':50,'bomber':200}[type_]
        self.x,self.y=0,10
        self.vx = {'fighter':12,'civilian':5,'bomber':8}[type_]
        self.vy = random.uniform(0,2)
        self.rect=pygame.Rect(self.x,self.y,20,20)
        self.image=pygame.Surface((20,20))
        self.image.fill({'fighter':(255,0,0),'civilian':(100,100,100),'bomber':(200,200,255)}[type_])

    def update(self,group):
        if self.x>800: group.remove(self)
        self.x+=self.vx; self.y+=self.vy
        self.rect.center=(self.x,self.y)

    def draw(self): screen.blit(self.image,self.rect)

class Ammunition:
    def __init__(self,x,y,type_):
        if type_ in ['missile','AAA','proximity shell']:
            self.damage={'missile':500,'AAA':30,'proximity shell':150}[type_]
            self.type_=type_
        self.x,self.y=x,y
        self.vy=-10
        self.rect=pygame.Rect(x,y,5,10)
        self.image=pygame.Surface((5,10))
        
        self.image.fill({'missile':(255,255,0),'AAA':(0,255,0),'proximity shell':(255,0,255)}[type_])
        self.detonation_radius={'missile':40,'AAA':0,'proximity shell':50}[type_]
    def update(self,group):
        if self.y<0: group.remove(self)
        self.y+=self.vy
        self.rect.center=(self.x,self.y)

    def draw(self): screen.blit(self.image,self.rect)

class ADS:
    def __init__(self):
        self.x,self.y=400,550
        self.vx=10
        self.rect=pygame.Rect(self.x,self.y,30,30)
        self.image=pygame.Surface((30,30))
        self.image.fill((0,255,0))
        self.last_shot=0
        self.shooting=False
        self.start_time=0
        self.ammo_type='AAA'

    def update(self):
        keys=pygame.key.get_pressed()
        if keys[pygame.K_a]: self.x-=self.vx
        if keys[pygame.K_d]: self.x+=self.vx
        if keys[pygame.K_1]: self.ammo_type='missile'
        if keys[pygame.K_2]: self.ammo_type='AAA'
        if keys[pygame.K_3]: self.ammo_type='proximity shell'
        self.x%=800 #best one liner i have ever written
        self.rect.center=(self.x,self.y)
    def draw(self): screen.blit(self.image,self.rect)
    def shoot(self,group):
        now=pygame.time.get_ticks()
        if not self.shooting: return
        if now-self.start_time>1000:
            self.shooting=False; return
        if now-self.last_shot>={'missile':500,'AAA':25,'proximity shell':750}[self.ammo_type]:
            self.last_shot=now
            group.append(Ammunition(self.x,self.y,self.ammo_type))

def collide(ammo_list:list[Ammunition],ac_list:list[Aircraft]):
    for ammo in ammo_list[:]:
        for a in ac_list:
            dist=((ammo.x-a.x)**2+(ammo.y-a.y)**2)**0.5
            if dist<ammo.detonation_radius:
                a.health-=ammo.damage*((ammo.detonation_radius-dist))
                if a.health<=0: ac_list.remove(a)
                ammo_list.remove(ammo)
                break
            if ammo.rect.colliderect(a.rect):
                a.health-=ammo.damage
                if a.health<=0: ac_list.remove(a)
                ammo_list.remove(ammo)
                break

ac=[Aircraft()]
ammo=[]
ads=ADS()
last_spawn=0

running=True
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT: running=False
        if event.type==pygame.KEYDOWN and event.key==pygame.K_w:
            ads.shooting=True
            ads.start_time=pygame.time.get_ticks()
        if event.type==pygame.KEYUP and event.key==pygame.K_w:
            ads.shooting=False

    screen.fill((0,0,0))

    if pygame.time.get_ticks()-last_spawn>2000:
        ac.append(Aircraft(random.choice(['fighter','civilian','bomber'])))
        last_spawn=pygame.time.get_ticks()

    for a in ac[:]:
        a.update(ac)
        a.draw()

    for b in ammo[:]:
        b.update(ammo)
        b.draw()

    collide(ammo,ac)

    ads.update()
    ads.shoot(ammo)
    ads.draw()

    pygame.display.flip()
    clock.tick(60)
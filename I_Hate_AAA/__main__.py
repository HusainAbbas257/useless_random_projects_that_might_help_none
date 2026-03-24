import random, pygame
pygame.init()

screen = pygame.display.set_mode((800,600))
clock = pygame.time.Clock()
global score
score=0
class Aircraft:
    def __init__(self,type_='fighter'):
        self.type_=type_
        self.health={'fighter':80,'civilian':50,'bomber':150}[type_]
        self.x,self.y=-1000,10
        self.vx = {'fighter':10,'civilian':5,'bomber':6}[type_]
        self.vy = random.uniform(0,1)
        self.rect=pygame.Rect(self.x,self.y,20,20)
        self.image=pygame.Surface((20,20))
        self.image.fill({'fighter':(255,0,0),'civilian':(100,100,100),'bomber':(200,200,255)}[type_])
        self.aiming_reticle=None
        
    def update(self,group):
        if self.x>800: group.remove(self)
        self.x+=self.vx; self.y+=self.vy
        self.rect.center=(self.x,self.y)
        if self.aiming_reticle: self.aiming_reticle.update()
        color=self.image.get_at((0,0))
        opacity=int(255*(self.health/{'fighter':80,'civilian':50,'bomber':150}[self.type_]))
        self.image.fill((color.r,color.g,color.b,opacity))

    def draw(self): screen.blit(self.image,self.rect)

class Ammunition:
    def __init__(self,x,y,type_):
        if type_ in ['missile','AAA','proximity shell']:
            self.damage={'missile':150,'AAA':34,'proximity shell':200}[type_]
            self.type_=type_
        self.x,self.y=x,y
        self.vx=random.uniform(-0.5,0.5)
        self.vy={'missile':-8,'AAA':-20,'proximity shell':-9}[type_]   
        self.rect=pygame.Rect(x,y,5,10)
        self.image=pygame.Surface((5,10))
        
        self.image.fill({'missile':(255,255,0),'AAA':(0,255,0),'proximity shell':(255,0,255)}[type_])
        self.detonation_radius={'missile':40,'AAA':0,'proximity shell':75}[type_]
    def update(self,group):
        if self.y<0: group.remove(self)
        self.x+=self.vx
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
        self.ammo_type='missile'
        # for line of sight 
        self.los_length=1000
        self.los_image=pygame.Surface((1,self.los_length))
        self.los_image.fill(( random.randint(0,255),random.randint(0,255),0,200))
        self.los_rect=self.los_image.get_rect()

    def update(self):
        keys=pygame.key.get_pressed()
        if keys[pygame.K_a]: self.x-=self.vx
        if keys[pygame.K_d]: self.x+=self.vx
        if keys[pygame.K_1]: self.ammo_type='missile'
        if keys[pygame.K_2]: self.ammo_type='AAA'
        if keys[pygame.K_3]: self.ammo_type='proximity shell'
        self.x%=800 #best one liner i have ever written
        self.rect.center=(self.x,self.y)
        if self.ammo_type=='missile' or self.ammo_type=='AAA':
            for a in ac:
                if a.aiming_reticle is None:
                    a.aiming_reticle=AimingReticle(Ammunition(self.x,self.y,self.ammo_type),a)
                    break
        else:
            for a in ac:
                a.aiming_reticle=None
    def draw(self):
        screen.blit(self.image,self.rect)
            # draw line of sight
        if self.ammo_type=='missile' or self.ammo_type=='AAA':   
            self.los_rect.midbottom=(self.x,self.y)
            screen.blit(self.los_image,self.los_rect)
    def shoot(self,group):
        now=pygame.time.get_ticks()
        if not self.shooting: return
        if now-self.start_time>1000:
            self.shooting=False; return
        if now-self.last_shot>={'missile':500,'AAA':25,'proximity shell':750}[self.ammo_type]:
            self.last_shot=now
            group.append(Ammunition(self.x,self.y,self.ammo_type))
            
            global score
            score-= {'missile':50,'AAA':1,'proximity shell':25}[self.ammo_type]

class blast:
    def __init__(self,ammo:Ammunition):
        self.ammo=ammo
        self.x,self.y=ammo.x-2.5,ammo.y-10
        self.rect=pygame.Rect(self.x,self.y,ammo.detonation_radius,ammo.detonation_radius)
        self.rect.center=(self.x,self.y)
        self.image=pygame.Surface((ammo.detonation_radius,ammo.detonation_radius), pygame.SRCALPHA)
        self.timeo={'missile':1,'AAA':0,'proximity shell':2}[ammo.type_]
        self.time=self.timeo
        self.image.fill((200,100,100,int(255*(self.time/self.timeo))))
        self.damaged=[]
    def damage(self,a:Aircraft):
        if a in self.damaged: return
        dist=((self.x+5-a.x)**2+(self.y+5-a.y)**2)**0.5
        if dist<self.ammo.detonation_radius:
            a.health-=self.ammo.damage*(self.time/self.timeo)
            self.damaged.append(a)
    def update(self,clock:pygame.time.Clock,group:list):
        self.time-= 1/clock.get_fps()
        if self.time<=0: group.remove(self)
    def display(self):
        if self.time<=0: return
        self.image.fill((200,100,100,int(255*(self.time/self.timeo))))      
        screen.blit(self.image,self.rect)
class AimingReticle:
    def __init__(self, ammo, ac):
        self.ammo = ammo
        self.ac = ac
        self.image = pygame.Surface((20,20), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255,255,0), (10,10), 10, 2)
        self.rect = self.image.get_rect()
        ac.aiming_reticle = self

    def update(self):
        # i  had to restudy physics to write this part, it was fun ngl
        ax, ay = self.ac.x, self.ac.y
        bx, by = self.ammo.x, self.ammo.y
        vax, vay = self.ac.vx, self.ac.vy
        vb = self.ammo.vy

        denom = (vb - vay)
        if denom != 0:
            t = (ay - by) / denom
            if t > 0:
                px = ax + vax * t
                py = ay + vay * t
                self.rect.center = (px, py)
                return

        self.rect.center = (ax, ay)

    def draw(self):
        screen.blit(self.image, self.rect)  
def collide(ammo_list:list[Ammunition],ac_list:list[Aircraft],blasts:list[blast]):
    for a in ac_list:
        for ammo in ammo_list:
            dist=((ammo.x-a.x)**2+(ammo.y-a.y)**2)**0.5
            if dist<(ammo.detonation_radius*0.5):
                blasts.append(blast(ammo))
                if a.health<=0: ac_list.remove(a)
                ammo_list.remove(ammo)
                break
            if ammo.rect.colliderect(a.rect):
                a.health-=ammo.damage
                global score
                
                if a.health<=0:
                    ac_list.remove(a)
                    score+= {'fighter':100,'civilian':-10,'bomber':200}[a.type_]
                ammo_list.remove(ammo)
                break
        for b in blasts:
            if a in b.damaged: continue
            b.damage(a)
            if a.health<=0:
                if a in ac_list:
                    ac_list.remove(a)
                score+= {'fighter':100,'civilian':-10,'bomber':200}[a.type_]
frame_count=0
fps=60
ac=[Aircraft()]
ammo=[]
blasts=[]
ads=ADS()
last_spawn=0
spawn_time=5000
score_font=pygame.font.SysFont(None, 36)
running=True
while running:
    frame_count+=1
    for event in pygame.event.get():
        if event.type==pygame.QUIT: running=False
        if event.type==pygame.KEYDOWN and event.key==pygame.K_w:
            ads.shooting=True
            ads.start_time=pygame.time.get_ticks()
        if event.type==pygame.KEYUP and event.key==pygame.K_w:
            ads.shooting=False

    screen.fill((0,0,0))
    
    if pygame.time.get_ticks()-last_spawn>spawn_time:
        ac.append(Aircraft(random.choice(['fighter','civilian','bomber'])))
        last_spawn=pygame.time.get_ticks()

    for a in ac[:]:
        if a.aiming_reticle:
            a.aiming_reticle.update()
        a.update(ac)
        a.draw()
        a.aiming_reticle.draw() if a.aiming_reticle else None

    for b in ammo[:]:
        b.update(ammo)
        b.draw()
    for b in blasts[:]:
        b.update(clock,blasts)
        b.display()
    collide(ammo,ac,blasts)
    if( frame_count%fps==0):
        spawn_time-=50
    spawn_time=max(spawn_time,1000)
    pygame.display.set_caption(f"I Hate AAA - Score: {score}")
    score_font_surface = score_font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_font_surface, (10, 10))
    ads.update()
    ads.shoot(ammo)
    ads.draw()

    pygame.display.flip()
    clock.tick(fps)
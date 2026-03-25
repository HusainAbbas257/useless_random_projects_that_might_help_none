import random, pygame
from pygame import color
pygame.init()


screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
width,height=screen.get_size()
clock = pygame.time.Clock()
# images
bg=pygame.image.load('I_Hate_AAA/bg.jpg')
bg=pygame.transform.scale(bg,(width,height))
aircraft_images = {}
aircraft_images['fighter'] = pygame.image.load('I_Hate_AAA/f22.png').convert_alpha()
aircraft_images['bomber'] = pygame.image.load('I_Hate_AAA/b2.png').convert_alpha()
aircraft_images['civilian'] = pygame.image.load('I_Hate_AAA/civilian.png').convert_alpha()
ammo_images={}
ammo_images['AAA']=pygame.image.load('I_Hate_AAA/AAA.png').convert_alpha()
ammo_images['missile']=pygame.image.load('I_Hate_AAA/missile.png').convert_alpha()
ammo_images['proximity shell']=pygame.image.load('I_Hate_AAA/proximity.png').convert_alpha()
ads_img=pygame.image.load('I_Hate_AAA/ads.png').convert_alpha()

# fonts
ammo_cost=pygame.font.Font('i_Hate_AAA/font.otf',20)
system_font=pygame.font.SysFont(None, 36)

global score,destroyed
destroyed=0 #stores the time left it dissappears
score=0
class Aircraft:
    def __init__(self,type_='fighter'):
        self.type_=type_
        self.healtho={'fighter':150,'civilian':75,'bomber':200}[type_]
        self.health=self.healtho
        self.x,self.y=-1000,random.randint(50,200)
        self.vx = {'fighter':15,'civilian':8,'bomber':10}[type_]
        self.vy = random.uniform(0,1)
        self.image=aircraft_images[type_]
        # resize the image to be of rect size
        self.image=pygame.transform.scale(self.image,({'fighter':(45,45),'civilian':(70,70),'bomber':(55,55)}[type_]))
        self.rect=self.image.get_rect()
        
        self.aiming_reticle=None
        
    def update(self,group):
        self.vy=(1-(self.health/self.healtho))*3
        self.vy*= -1 if self.vy<0 else 1
        if self.x>width:
            if(self.health<self.healtho*0.9) and self.type_!='civilian':
                self.health*=1.25
                self.health=min(self.health,self.healtho)
                self.y-=5
                self.y=max(self.rect.height+5,self.y)
                self.x%=width
            else:
                group.remove(self)
        self.x+=self.vx; self.y+=self.vy
        self.rect.center=(self.x,self.y)
        if self.aiming_reticle: self.aiming_reticle.update()
        img=aircraft_images[self.type_]
        self.image=pygame.transform.scale(img,({'fighter':(45,45),'civilian':(70,70),'bomber':(55,55)}[self.type_]))
        
        opacity=int(255*(self.health/{'fighter':80,'civilian':50,'bomber':150}[self.type_]))
        # accounting for steath 
        opacity*=0.8 if self.type_=='bomber' else (0.9 if self.type_=='fighter' else 1)
        self.image.set_alpha(opacity)
        if(self.health<0.01*self.healtho) or self.y-self.rect.height>=height:
            group.remove(self)
            
            global score,destroyed
            destroyed=1 if a.type_!='civilian' else 0
            score+= {'fighter':75,'civilian':-10,'bomber':150}[self.type_]

    def draw(self): screen.blit(self.image,self.rect)

class Ammunition:
    def __init__(self,x,y,type_):
        if type_ in ['missile','AAA','proximity shell']:
            self.damage={'missile':150,'AAA':26,'proximity shell':200}[type_]
            self.type_=type_
        self.x,self.y=x,y
        self.vx=random.uniform(-0.5,0.5)
        self.vy={'missile':-8,'AAA':-20,'proximity shell':-9}[type_]   
        self.image=ammo_images[type_]
        self.image=pygame.transform.scale(self.image,({'missile':(5,20),'AAA':(3,10),'proximity shell':(5,20)}[type_]))
        self.rect=self.image.get_rect()
        self.detonation_radius={'missile':90,'AAA':0,'proximity shell':210}[type_]
    def update(self,group):
        if self.y<0: group.remove(self)
        self.x+=self.vx
        self.y+=self.vy
        self.rect.center=(self.x,self.y)

    def draw(self): screen.blit(self.image,self.rect)

class ADS:
    def __init__(self):
        self.x,self.y=width-30,height-30
        self.vx=10
        self.image=pygame.transform.scale(ads_img,(50,50))
        self.rect=self.image.get_rect()
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
        self.x%=width #best one liner i have ever written
        self.rect.center=(self.x,self.y)
        if self.ammo_type=='missile' or self.ammo_type=='proximity shell':
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
    def shoot(self,group,damagefontgroup:list):
        now=pygame.time.get_ticks()
        if not self.shooting: return
        if now-self.start_time>1000:
            self.shooting=False; return
        if now-self.last_shot>={'missile':500,'AAA':25,'proximity shell':750}[self.ammo_type]:
            self.last_shot=now
            group.append(Ammunition(self.x,self.y,self.ammo_type))
            while len(damagefontgroup)>=5:
                damagefontgroup.remove(damagefontgroup[0])
            cost={'missile':50,'AAA':1,'proximity shell':25}[self.ammo_type]
            damagefontgroup.append((ammo_cost.render(f'-{cost}',True ,( (random.randint(150,255),random.randint(0,100),random.randint(0,100)))),(self.x+random.uniform(-10,10),self.y+random.uniform(-10,10))))
            global score
            
            score-= cost

class blast:
    def __init__(self,ammo:Ammunition):
        self.ammo=ammo
        self.x,self.y=ammo.x,ammo.y
        self.rect=pygame.Rect(0,0,ammo.detonation_radius//4,ammo.detonation_radius//4)
        self.rect.center=self.x,self.y
        self.rect.bottomright=(self.x,self.y)
        self.image=pygame.Surface((ammo.detonation_radius,ammo.detonation_radius), pygame.SRCALPHA)
        self.timeo={'missile':1,'AAA':0,'proximity shell':2}[ammo.type_]
        self.time=self.timeo
        self.image.fill((200,100,100,int(255*(self.time/self.timeo))))
        self.damaged=[]
    def damage(self,a:Aircraft):
        if a in self.damaged: return
        dist=((self.x+5-a.x)**2+(self.y+5-a.y)**2)**0.5
        if dist<self.ammo.detonation_radius-a.rect.width-self.ammo.rect.height:
            a.health-=self.ammo.damage*(self.time/self.timeo)*0.75
            self.damaged.append(a)
    def update(self,clock:pygame.time.Clock,group:list):
        self.time-= 1/clock.get_fps()
        if self.time<=0: group.remove(self)
    def display(self):
        if self.time<=0: return
        self.image.fill((200,100,100,int(255*(self.time/self.timeo))))      
        screen.blit(self.image,self.rect)
class AimingReticle:
    def __init__(self, ammo:Ammunition, ac):
        self.ammo = ammo
        self.ac = ac
        self.image = pygame.Surface((20,20), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255,255,0), (10,10), ammo.detonation_radius**0.5, 2)
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
    global score,destroyed
    for a in ac_list:
        for ammo in ammo_list:
            dist=((ammo.x-a.x)**2+(ammo.y-a.y)**2)**0.5
            if dist<(ammo.detonation_radius)-a.rect.width-ammo.rect.height:
                blasts.append(blast(ammo))
                if a.health<=0:
                    ac_list.remove(a)
                    destroyed=1 if a.type_!='civilian' else 0
                    score+= {'fighter':100,'civilian':-10,'bomber':200}[a.type_]
                
                ammo_list.remove(ammo)
                break
            if ammo.rect.colliderect(a.rect):
                a.health-=ammo.damage
                if a.health<=0:
                    destroyed=1 if a.type_!='civilian' else 0
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
                destroyed=1 if a.type_!='civilian' else 0
                
                score+= {'fighter':100,'civilian':-10,'bomber':200}[a.type_]
frame_count=0
fps=60
ac=[Aircraft()]
ammo=[]
blasts=[]
ads=ADS()
last_spawn=0
spawn_time=5000
# stores the font surfae and its cordinates to avoid jitter while having some randomness
damage_texts:list[tuple[pygame.Surface,tuple[int,int]]]=[] # i myself got confused so wrote this huge description
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

    screen.blit(bg,(0,0))
    
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
        destroyed=False
        spawn_time-=50
        if damage_texts:
            damage_texts.pop()
    ads.update()
    ads.shoot(ammo,damage_texts)
    ads.draw()
    spawn_time=max(spawn_time,1000)
    pygame.display.set_caption(f"I Hate AAA - Score: {score}")
    system_font_surface = system_font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(system_font_surface, (10, 10))
    for f in damage_texts:
        screen.blit(f[0],f[1])
    destroyed-=1/fps
    if destroyed>0:
        screen.blit(system_font.render("aircraft destroyed", True, (255, 200, 200)),(width//2,50))
    pygame.display.flip()
    clock.tick(fps)
import pygame, random
pygame.init()

screen = pygame.display.set_mode((800,600))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)

bg = pygame.image.load("NitroRacing/track.jpg")
bg = pygame.transform.scale(bg,(800,600))
bgm=pygame.mixer.Sound("NitroRacing/bgm.mp3")
bgm.play(-1)
nitro_effect = pygame.Surface((800,600), pygame.SRCALPHA)
nitro_effect.fill((0,255,0,30))  # semi transparent
# sounds
swoosh_sound = pygame.mixer.Sound("NitroRacing/car-swoosh.wav")
collision_sound = pygame.mixer.Sound("NitroRacing/collision.wav")
horn_sound = pygame.mixer.Sound("NitroRacing/horn.wav")
turbo_sound = pygame.mixer.Sound("NitroRacing/turbo.mp3")
lanes = [150, 250, 350, 450,550]

# player
player_img = pygame.image.load("NitroRacing/player.png").convert_alpha()
player_img = pygame.transform.scale(player_img, (50,30))
lane_index = 1
player_rect = player_img.get_rect(midleft=(100, lanes[lane_index]))

# obstacles
obstacle_img = pygame.image.load("NitroRacing/obstacle.png").convert_alpha()
obstacle_img = pygame.transform.scale(obstacle_img, (50,30))
obstacles = []
lane_f={}
for i in lanes:
    lane_f[i]=0
def get_lane():
    least_3 = sorted(lane_f.items(), key=lambda x: x[1])[:3]
    lane = random.choice(least_3)[0]
    return lane
# nitro
nitro_img=pygame.image.load("NitroRacing/nitro.png").convert_alpha()
nitro_img=pygame.transform.scale(nitro_img,(50,50))
nitro = 100
nitro_active = False
nitro_already_playing = False
READY_THRESHOLD = 80

score = 0
speed_i = 5

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                lane_index = max(0, lane_index-1)
            if event.key == pygame.K_s:
                lane_index = min(len(lanes)-1, lane_index+1)
            if event.key == pygame.K_h:
                horn_sound.play()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE or nitro<5:
                nitro_already_playing = False
    keys = pygame.key.get_pressed()

    # draw
    screen.blit(bg,(0,0))
    screen.blit(player_img, player_rect)
    for o in obstacles:
        screen.blit(obstacle_img, o)
    screen.blit(font.render(f"Score: {int(score)}", True, (255,255,255)), (10,10))
    pygame.draw.rect(screen,((255,0,0) if nitro < READY_THRESHOLD else (255*(100-nitro)/100,255*(nitro/100),100*(nitro/100))), (10,40,abs(nitro)*2,10))  # nitro bar
    screen.blit(nitro_img, (10,30))  # nitro icon
    score_t=font.render(f'SCORE:{int(score)}',True,(int(score%10)*25,int(score%50)*5,int(score%25)*10))
    score_rec=score_t.get_rect(center=(700,50))
    screen.blit(score_t,score_rec)

    # recharge only when not using
    if not nitro_active:
        nitro = min(100, nitro + 0.3)

    # activation condition
    if keys[pygame.K_SPACE] and nitro >= READY_THRESHOLD:
        if not nitro_active :
            turbo_sound.play()
            turbo_sound.fadeout(1500)
        nitro_already_playing = True
        nitro_active = True
    else:
        nitro_active = nitro_already_playing and keys[pygame.K_SPACE]  # keep active if space is still held

    speed = speed_i * (2 if nitro_active else 1)
    # drain only while active
    if nitro_active:
        nitro -= 1
        if nitro <= 0:
            nitro = 0
            nitro_active = False

    player_rect.midleft = (100, lanes[lane_index])

    # spawn obstacles
    if pygame.time.get_ticks() % 750 < 20:  # every 750ms
        lane = get_lane()
        lane_f[lane]+=1
        rect = obstacle_img.get_rect(midleft=(800, lane))
        obstacles.append(rect)

    # move obstacles
    

    # collision
    for o in obstacles:
        o.x-=speed
        if((((o.x-100)**2 + (o.y-player_rect.y)**2)**0.5 < 100) and (not swoosh_sound.get_num_channels())):
            swoosh_sound.play()
        if(o.x < -50):
            try:
                lane_f[o.y]-=1
            except KeyError:
                print("Error: Lane not found for obstacle at y =", o.y)
            obstacles.remove(o)
        
        if player_rect.colliderect(o):
            bgm.stop()
            # draw the exsident scene first:
            screen.blit(bg,(0,0))
            for o in obstacles:
                screen.blit(obstacle_img, o)
            screen.blit(player_img, player_rect)
            screen.blit(font.render(f"Score: {int(score)}", True, (0,int(score%256),0)), (300,300))
            pygame.display.flip()
            collision_sound.play()
            print("Game Over! Score:", score)
            # pause for a moment to let the sound play
            pygame.time.delay(2000)
            running = False

    obstacles = [o for o in obstacles if o.x > -50]

    score += speed * 0.05* (2 if nitro_active else 1)
    if(score%200==0):
        speed_i+= 1
    if nitro_active:
        screen.blit(nitro_effect,(0,0))
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
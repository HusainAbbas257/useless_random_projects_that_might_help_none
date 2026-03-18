import pygame, random
pygame.init()

screen = pygame.display.set_mode((800,600))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)

bg = pygame.image.load("NitroRacing/track.jpg")
bg = pygame.transform.scale(bg,(800,600))

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
    available_lanes = [l for l in lanes if lane_f[l] < 2]
    return random.choice(available_lanes) if available_lanes else random.choice(lanes)
# nitro
nitro_img=pygame.image.load("NitroRacing/nitro.png").convert_alpha()
nitro_img=pygame.transform.scale(nitro_img,(50,50))
nitro = 100
nitro_active = False

score = 0
speed = 5

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

    keys = pygame.key.get_pressed()

    #nitro 
    if keys[pygame.K_SPACE] and nitro > 0:
        nitro_active = True
        nitro -= 1
    else:
        nitro_active = False
        nitro = min(100, nitro + 0.1)

    speed = 10 if nitro_active else 5

    player_rect.midleft = (100, lanes[lane_index])

    # spawn obstacles
    if pygame.time.get_ticks() % 1000 < 20:  # every second
        lane = get_lane()
        lane_f[lane]+=1
        rect = obstacle_img.get_rect(midleft=(800, lane))
        obstacles.append(rect)

    # move obstacles
    for o in obstacles:
        o.x -= speed

    # collision
    for o in obstacles:
        if(o.x < -50):
            try:
                lane_f[o.y]-=1
            except KeyError:
                print("Error: Lane not found for obstacle at y =", o.y)
            obstacles.remove(o)
        
        if player_rect.colliderect(o):
            print("Game Over! Score:", score)
            running = False

    obstacles = [o for o in obstacles if o.x > -50]

    score += speed * 0.1

    # draw
    screen.blit(bg,(0,0))
    screen.blit(player_img, player_rect)

    for o in obstacles:
        screen.blit(obstacle_img, o)

    # UI
    screen.blit(font.render(f"Score: {int(score)}", True, (255,255,255)), (10,10))
    pygame.draw.rect(screen,(0,255,255),(10,40,nitro*2,10))  # nitro bar
    screen.blit(nitro_img, (10,30))  # nitro icon
    score_t=font.render(f'SCORE:{score}',True,(0,0,0))
    score_rec=score_t.get_rect(center=(700,50))
    screen.blit(score_t,score_rec)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
import pygame
import random
pygame.init()

screen = pygame.display.set_mode((800,600))
clock = pygame.time.Clock()
font = pygame.font.Font('creeper_run/Minecraft.ttf', 36)
fps=60
frame_count = 0
# player
player_img = pygame.image.load("creeper_run/player.png")
player_img = pygame.transform.scale(player_img, (30, 30))

x,y = 400,300
vx,vy = 0,0
speed = 0.25
player = player_img.get_rect()
player.topleft = x, y
# creeper
creeper_img = pygame.image.load("creeper_run/creeper.png")
creeper_img = pygame.transform.scale(creeper_img, (30, 30))
cx,cy = 200,200
cvx,cvy = 0,0
creeper_speed = speed*0.85
creeper=creeper_img.get_rect()
creeper.topleft = cx, cy
# coins
coins=[]
for i in range(5):
    coin_img=pygame.image.load("creeper_run/coin.png")
    coin_img=pygame.transform.scale(coin_img,(30,30))
    coin = pygame.Rect(random.randint(0,770), random.randint(0,570), 20, 20)
    coins.append(coin)
    
score = 0
running = True
while running:
    frame_count += 1
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]: vy -= speed
    if keys[pygame.K_s]: vy += speed
    if keys[pygame.K_a]: vx -= speed
    if keys[pygame.K_d]: vx += speed
    if keys[pygame.K_SPACE]: vx*=0.9; vy*=0.9
    x += vx
    y += vy
    if x <= 0: x = 0; vx = -vx * 0.5
    if y <= 0: y = 0; vy = -vy * 0.5
    if x >= 770: x = 770; vx = -vx * 0.5
    if y >= 570: y = 570; vy = -vy * 0.5
    # creeper AI
    if cx < x: cvx += creeper_speed
    if cx > x: cvx -= creeper_speed
    if cy < y: cvy += creeper_speed
    if cy > y: cvy -= creeper_speed
    # slowing this man down else he gonna just wonder all over the world
    cvx *= 0.95
    cvy *= 0.95
    cx += cvx
    cy += cvy
    # not adding boundary for this to make it harder
    
    if(player.colliderect(creeper)):
        print("Game Over!")
        print("Your Score:", score)
        running = False
    player.topleft=x,y
    creeper.topleft=cx,cy
    screen.fill((0,0,0))
    for coin in coins[:]:
        screen.blit(coin_img, coin)
        if player.colliderect(coin):
            coins.remove(coin)
            score += 10
            coins.append(pygame.Rect(random.randint(0,770), random.randint(0,570), 20, 20))
    screen.blit(player_img, player)
    screen.blit(creeper_img, creeper)
    screen.blit(font.render("Score: "+str(score), True, (255,255,255)), (10,10))
    pygame.display.flip()
    if (frame_count % (5*fps) == 0 or (score%100 == 0 and score > 100)):  
        creeper_speed *= 1.1  
        score += 5  
    if frame_count % (10*fps) == 0:  
        score += 10 
    clock.tick(fps)

pygame.quit()
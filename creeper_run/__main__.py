import pygame
pygame.init()

screen = pygame.display.set_mode((800,600))
clock = pygame.time.Clock()

# player
x,y = 400,300
vx,vy = 0,0
speed = 0.25
player=pygame.Rect(x,y,30,30)
# creeper
cx,cy = 200,200
cvx,cvy = 0,0
creeper_speed = speed*0.85
creeper=pygame.Rect(cx,cy,30,30)

running = True
while running:
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
        print("Your Score:", (pygame.time.get_ticks()/1000), "seconds")
        running = False
    player.topleft=x,y
    creeper.topleft=cx,cy
    screen.fill((0,0,0))
    pygame.draw.rect(screen,(0,255,0),player)
    pygame.draw.rect(screen,(255,0,0),creeper)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
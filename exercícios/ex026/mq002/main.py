import pygame
import sys
pygame.init()

display = pygame.display.set_mode((560,340),pygame.RESIZABLE)
pygame.display.set_caption("minitale")

scale = 0
zoom = 1.05

player = pygame.Rect(0,0,32,32)
speed = 0.05
playerx=0.0
playery=0.0 

while 1:
    scale = display.get_height()/340*zoom
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    display.fill((0,0,0))
    
    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]:
        playery -= speed*scale
    elif keys[pygame.K_DOWN]:
        playery += speed*scale
    elif keys[pygame.K_LEFT]:
        playerx -= speed*scale
    elif keys[pygame.K_RIGHT]:
        playerx += speed*scale
    player.topleft = (playerx, playery)

    
    print(scale)
    player.size = (16*scale,16*scale)

    pygame.draw.rect(display,(255,255,255), player, border_radius=int(8*scale))

    pygame.display.flip()
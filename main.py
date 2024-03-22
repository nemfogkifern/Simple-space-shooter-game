import pygame

pygame.init()

width = 640
height = 360

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Space invader')

#Background
bg_surf = pygame.image.load('images/bg.png')



game_active = True

clock = pygame.time.Clock()

while game_active:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    
    screen.blit(bg_surf,(0,0))




    pygame.display.update()
    clock.tick(60)
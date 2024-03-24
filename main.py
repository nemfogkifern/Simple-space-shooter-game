import random

import pygame
pygame.init()

#Screen specs
width = 640
height = 360
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Space invader')

#Background
bg_surf = pygame.image.load('temp/images/bg.png')

font = pygame.font.Font(None, 36)

class Player_Spaceship:
    VEL = 3
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def draw(self, screen):
        spaceship_surf = pygame.image.load('temp/images/spaceship.png').convert_alpha()
        spaceship_rect = spaceship_surf.get_rect(center = (self.x ,self.y))
        screen.blit(spaceship_surf, spaceship_rect)

    def move_y(self, up):
        if up == True:
            self.y -= self.VEL
        else:
            self.y += self.VEL
    def move_x(self, right):
        if right == True:
            self.x += self.VEL
        else:
            self.x -= self.VEL

class Enemy_Spaceship:
    VEL = 1
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def draw(self, screen):
        spaceship_surf = pygame.image.load('temp/images/tie.png').convert_alpha()
        spaceship_rect = spaceship_surf.get_rect(center = (self.x ,self.y))
        screen.blit(spaceship_surf, spaceship_rect)

    def move_y(self, up):
        if up == True:
            self.y -= self.VEL
        else:
            self.y += self.VEL
    def move_x(self, right):
        if right == True:
            self.x += self.VEL
        else:
            self.x -= self.VEL
        
        

class Laser:
    VEL = 5
    COLOR = 'Red'

    def __init__(self, x, y, width, height) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, screen):
        pygame.draw.rect(screen, self.COLOR, (self.x, self.y, self.width, self.height))
    
    def move(self, up):
        if up == True:
            self.y -= self.VEL
        else: 
            self.y += self.VEL

        if self.y <= 0 or self.y >= height:
            pass

def main():
    game_active = True


    clock = pygame.time.Clock()
    FPS = 60
    

    laser_list = []
    enemy_list = []
    last_time = 0
    laser_cooldown = 500

    spawn_timer = 0
    spawn_frequency = 1500

    score = 0

    player_ship = Player_Spaceship(width/2, height/2)


    
    while True:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        #User input
        pressed_keys = pygame.key.get_pressed()

        if game_active:
            #Screen

            screen.blit(bg_surf,(0,0))
            player_ship.draw(screen)
            point_surf = font.render(str(score), False, 'Yellow')
            point_rect = point_surf.get_rect(center=(10, 10))
            screen.blit(point_surf, point_rect)


            current_time = pygame.time.get_ticks()


            #PLayer ship movement


            if pressed_keys[pygame.K_UP] and player_ship.y >= 0:
                player_ship.move_y(True)
            if pressed_keys[pygame.K_DOWN] and player_ship.y <= height:
                player_ship.move_y(False)
            if pressed_keys[pygame.K_LEFT] and player_ship.x >= 0:
                player_ship.move_x(False)
            if pressed_keys[pygame.K_RIGHT] and player_ship.x <= width:
                player_ship.move_x(True)

            #Laser firing
            laser_cooldown_time = current_time - last_time

            if pressed_keys[pygame.K_SPACE] and laser_cooldown_time > laser_cooldown:
                player_laser = Laser(player_ship.x, player_ship.y - 10, 4, 18)
                laser_list.append(player_laser)
                last_time = pygame.time.get_ticks()

            for laser in laser_list:
               laser.draw(screen)
               laser.move(True)

               if laser.y <= 0 or laser.y >= height:
                   laser_list.remove(laser)

            #Enemy ships

            spawn_timer += clock.get_rawtime()

            if  (spawn_timer  > spawn_frequency):
                for i in range(random.randint(1,6)):
                    if i == 0: continue
                    enemy_ship = Enemy_Spaceship(width / 6 + i * 80 , 0)
                    enemy_list.append(enemy_ship)
                    spawn_timer = 0

            for enemy in enemy_list:
                    enemy.draw(screen)
                    enemy.move_y(False)

                    if enemy.y <= 0 or enemy.y >= height:
                        enemy_list.remove(enemy)

            player_rect = pygame.Rect(player_ship.x - 25.5, player_ship.y - 24.5, 51, 49)  
            for enemy_ship in enemy_list:
                enemy_rect = pygame.Rect(enemy_ship.x - 22.5, enemy_ship.y - 22, 45, 44)
                if player_rect.colliderect(enemy_rect):
                    game_active = False
            for laser in laser_list:
                laser_rect = pygame.Rect(laser.x, laser.y, 4, 18)
                for enemy_ship in enemy_list:
                    enemy_rect = pygame.Rect(enemy_ship.x - 22.5, enemy_ship.y - 22, 45, 44)
                    if laser_rect.colliderect(enemy_rect):
                        enemy_list.remove(enemy_ship)
                        laser_list.remove(laser)
                        score += 1

            
        else:
            screen.fill('Black')

            game_start_text_surf = font.render(f"Press Space to start", False, 'Yellow')
            game_start_text_rect = game_start_text_surf.get_rect(center=(width/2, height/2))
            
            score_text_surf = font.render(f" Your score: {str(score)}", False, 'Yellow')
            score_text_rect = score_text_surf.get_rect(center=(width/2, height/2 + 30))

            ship_deco_surf = pygame.image.load('temp/images/spaceship.png').convert_alpha()
            ship_deco_rect = ship_deco_surf.get_rect(center=(width/2, height/2 - 60))

            screen.blit(game_start_text_surf, game_start_text_rect)
            screen.blit(score_text_surf, score_text_rect)
            screen.blit(ship_deco_surf, ship_deco_rect)





            if pressed_keys[pygame.K_SPACE]:
                score = 0
                enemy_list = []
                laser_list = []

                player_ship.x = width/2
                player_ship.y = height/2

                game_active = True
        
        
        pygame.display.update()
        clock.tick(FPS)

if __name__ == '__main__':
    main()



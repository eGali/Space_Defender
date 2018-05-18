import pygame
import sys
import random
import time
from pygame.locals import *
from game import *
from time import process_time

# constants
SHIPSPACE = 80
BOARD_LENGTH = 800
BOARD_WIDTH = 800
BLACK = pygame.Color(0,0,0)
WHITE = pygame.Color(255, 255, 255)
NEON = pygame.Color(57, 255, 20)
SKY = pygame.Color(0,51,102)
ENEMY_DROP_AMOUNT = 60
START = True

def main():
    pygame.init()
    FPS = 30
    LEVEL = 1
    nextLevel = True
    ENEMY_SHIP_SPEED = 1
    SHIP_HEALTH = 100
    changeLevel = False
    fps_clock = pygame.time.Clock()
    
#     creates all sprite groups to be used
    stars = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_shots = pygame.sprite.Group()
    all_enemies = pygame.sprite.Group()
    all_walls = pygame.sprite.Group()
    all_asteroids = pygame.sprite.Group()
    all_enemy_shots = pygame.sprite.Group()
    
#     create board
    window_size = (BOARD_LENGTH, BOARD_WIDTH)
    screen = pygame.display.set_mode(window_size)
    
#     create stars
    for x in range(0, 400):
        star1 = Star(random.randrange(0, 800), random.randrange(0, 800), 'images/star.png')
        stars.add(star1)
    
#     display and sounds used
    pygame.display.set_caption('Space Defender')
    laserSound = pygame.mixer.Sound('sounds/laser.ogg')
    enemyDead = pygame.mixer.Sound('sounds/enemyExplosion.ogg')
    asteroidDestroy = pygame.mixer.Sound('sounds/asteroidExplosion.ogg')
    backMusic = pygame.mixer.Sound('sounds/allOfUs.ogg')
    shipExplode = pygame.mixer.Sound('sounds/shipExplode.ogg')
    shiHit = pygame.mixer.Sound('sounds/shipHit.ogg')
    bulletHit = pygame.mixer.Sound('sounds/hit.ogg')
    
#     create walls
    wall1 = Wall(-10,0,10,BOARD_LENGTH)
    all_walls.add(wall1)
    all_sprites.add(wall1)
    wall2 = Wall(BOARD_WIDTH, 0, 10, BOARD_LENGTH)
    all_walls.add(wall2)
    all_sprites.add(wall2)
    wall3 = Wall(0, BOARD_LENGTH, BOARD_LENGTH, 10)
    all_walls.add(wall3)
    all_sprites.add(wall3)
    wall4 = Wall(0, -10, BOARD_LENGTH, 10)
    all_walls.add(wall4)
    all_sprites.add(wall4)
    
#     fill screen and create ship
    screen.fill(SKY)
    ship = Ship(200, 700, 'images/ship.png')
    all_sprites.add(ship)
    
#     bool values for keys used
    keyA = False
    keyD = False
    
#     start of main game loop
    while True:
        if  not pygame.mixer.get_busy():
            backMusic.play()
        if START:
            start(screen)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
    
            if event.type == KEYDOWN:
                if event.key == K_p:
                    pause(screen)
                if event.key == K_a:
                    keyA = True
                if event.key == K_d:
                    keyD = True
                if event.key == K_EQUALS:
                    SHIP_HEALTH += 10
                if event.key == K_SPACE:
                    s = shoot(ship, True)
                    all_shots.add(s)
                    all_sprites.add(s)
                    laserSound.play()
                    
            if event.type == KEYUP:
                if event.key == K_a:
                    keyA = False
                if event.key == K_d:
                    keyD = False          
        
        if keyA:
            x = ship.getX() + -10
            ship.setX(x)
            
        if keyD:
            x = ship.getX() + 10
            ship.setX(x)
            
#         collision between ship and walls
        wallhit = pygame.sprite.spritecollide(ship, all_walls, False)
        for s in wallhit:
            if s != ship:
                if keyA:
                    ship.rect.left = s.rect.right
                if keyD:
                    ship.rect.right = s.rect.left
                    
#         test to see which level to create
        if LEVEL == 1 and nextLevel == True:
            nextLevel = False
            level1(all_sprites, all_enemies, ENEMY_SHIP_SPEED, 50)
        if LEVEL == 2 and nextLevel == True:
            nextLevel = False
            level1(all_sprites, all_enemies, ENEMY_SHIP_SPEED, 110)
            level2(all_sprites, all_enemies, ENEMY_SHIP_SPEED, 170)
        if LEVEL == 3 and nextLevel == True:
            nextLevel = False
            level1(all_sprites, all_enemies, ENEMY_SHIP_SPEED, 170)
            level2(all_sprites, all_enemies, ENEMY_SHIP_SPEED, 230)
            level3(all_sprites, all_enemies, ENEMY_SHIP_SPEED, 290)
        if LEVEL == 4 and nextLevel == True:
            nextLevel = False
            SHIP_HEALTH = 100
            level1(all_sprites, all_enemies, ENEMY_SHIP_SPEED, 230)
            level2(all_sprites, all_enemies, ENEMY_SHIP_SPEED, 290)
            level3(all_sprites, all_enemies, ENEMY_SHIP_SPEED, 350)
            level4(all_sprites, all_enemies, ENEMY_SHIP_SPEED, 410)
        if LEVEL == 5 and nextLevel == True:
            nextLevel = False
            SHIP_HEALTH = 100
            level1(all_sprites, all_enemies, ENEMY_SHIP_SPEED, 290)
            level2(all_sprites, all_enemies, ENEMY_SHIP_SPEED, 350)
            level3(all_sprites, all_enemies, ENEMY_SHIP_SPEED, 410)
            level4(all_sprites, all_enemies, ENEMY_SHIP_SPEED, 470)
            level5(all_sprites, all_enemies, ENEMY_SHIP_SPEED, 530)
            
        screen.fill(SKY)
        stars.update()
        stars.draw(screen)
         
#         create new asteroid
        if LEVEL != 5:
            if random.randrange(0,25) == 11 :
                s = asteroid(random.randrange(0, 3))
                all_asteroids.add(s)
                all_sprites.add(s)
        if LEVEL == 5:
            if random.randrange(0,13) == 11 :
                s = asteroid(random.randrange(0, 3))
                all_asteroids.add(s)
                all_sprites.add(s)
             
        if len(all_sprites) > 0:
            all_sprites.update()
        
#         test ship collision with all sprites
        ship_hit = pygame.sprite.spritecollide(ship, all_sprites, False)
        for hit in ship_hit:
            if not all_shots.has(hit) and hit != ship and not all_walls.has(hit) and not all_enemy_shots.has(hit) and not all_enemies.has(hit):
                kind = hit.getKind()
                if kind == 1:
                    damage = 10
                elif kind == 2:
                    damage = 30
                elif kind == 3:
                    damage = 5
                SHIP_HEALTH  -= damage
                shiHit.play()
                all_sprites.remove(hit)
                all_asteroids.remove(hit)
                all_enemies.remove(hit)
                
#         enemy collision with walls
        for wall in all_walls:
            wallCollide = pygame.sprite.spritecollide(wall, all_enemies, False)
            for hit in wallCollide:
                if all_enemies.has(hit):
                    hit.setVX()
                
#         erase enemy shots when hit
        for shot in all_shots:
            shotCollide = pygame.sprite.spritecollide(shot, all_enemy_shots, False)
            for hit in shotCollide:
                    all_sprites.remove(hit)
                    all_enemy_shots.remove(hit)
                    all_shots.remove(hit)
                    bulletHit.play()
            
#         erase enemies shot 
        for pew in all_shots:
            enemy_hit = pygame.sprite.spritecollide(pew, all_enemies, False)
             
            for hit in enemy_hit:
                all_shots.remove(pew)
                all_sprites.remove(pew)
                all_enemies.remove(hit)
                all_sprites.remove(hit)
                enemyDead.play()
             
            if pew.rect.y < -10:
                all_shots.remove(pew)
                all_sprites.remove(pew)
                 
#         test asteroids shot
        for pew in all_shots:
            asteroidHit = pygame.sprite.spritecollide(pew, all_asteroids, False)
            for hit in asteroidHit:
                all_shots.remove(pew)
                all_sprites.remove(pew)
                if all_asteroids.has(hit):
                    kind = hit.getKind()
                    x = hit.getX()
                    y = hit.getY()
                    if kind == 1:
                        splitAsteroid(all_asteroids, all_sprites, hit, 2)
                        removeAsteroid(all_asteroids, all_sprites, hit)
                    if kind == 2:
                        splitAsteroid(all_asteroids, all_sprites, hit, 0)
                        removeAsteroid(all_asteroids, all_sprites, hit)
                    if kind == 3:
                        removeAsteroid(all_asteroids, all_sprites, hit)
                asteroidDestroy.play()
                 
        for rock in all_asteroids:
            if rock.rect.y > 820:
                all_asteroids.remove(rock)
                all_sprites.remove(rock)
                 
#         sets enemy shooting rate         
        for enemy in all_enemies:
            to = 100
            if LEVEL == 2:
                to = 150
            if LEVEL == 3:
                to = 200
            if LEVEL == 4:
                to = 250
            if LEVEL == 5:
                to = 225
            s = random.randrange(0, to)   
            if s == 6:
                eShot = shoot(enemy, False)
                all_enemy_shots.add(eShot)
                all_sprites.add(eShot)
                
        shipEnemyHit = pygame.sprite.spritecollide(ship, all_enemies, False)
        for hit in shipEnemyHit:
            SHIP_HEALTH = 0
            gameOver(screen, False)
                       
#         test if enemies crash each other
        for enemy in all_enemies:
            ship_hit = pygame.sprite.spritecollide(enemy, all_enemies, False)
            for crash in ship_hit:
                if crash != enemy:
                    enemy.setVX()
                    
#         test if ship has been shot
        enemyHit = pygame.sprite.spritecollide(ship, all_enemy_shots, False)
        for hit in enemyHit:
            if hit != ship:
                all_enemy_shots.remove(hit)
                all_sprites.remove(hit)
                SHIP_HEALTH -= 20
                shiHit.play()
        
#         timer to move ships to next show
        elapsedTime = pygame.time.get_ticks()
        if elapsedTime % 1000 == 0:
            changeLevel = True
        if changeLevel:
            for enemy in all_enemies:
                enemy.setY(ENEMY_DROP_AMOUNT)
            changeLevel = False
        
#         game update
        all_sprites.draw(screen)
        topGameDisplay(screen, SHIP_HEALTH, len(all_enemies))
        pygame.display.update()
        fps_clock.tick(FPS)
        
        if len(all_enemies) == 0:
            LEVEL += 1
            nextLevel = True
            
        if LEVEL > 5:
            gameOver(screen, True)
        if SHIP_HEALTH <= 0:
            shipExplode.play()
            gameOver(screen, False)
            


def start(screen):
    """
    Main start screen
    :param screen: screen to draw on
    """
    global START
    font = pygame.font.SysFont('Consolas', 115, False, False)
    font2 = pygame.font.SysFont('Consolas', 80, False, False)
    text_to_draw = font.render('Space Defender' , True, NEON)
    start = font2.render('Press enter to start' , True, NEON)
    center = (((BOARD_WIDTH/2)- 300),(BOARD_LENGTH/2) - 200)
    bottom = (((BOARD_WIDTH/2)- 250),(BOARD_LENGTH/2))
    screen.blit(text_to_draw, center)
    screen.fill(BLACK)
    screen.blit(text_to_draw, center)
    screen.blit(start, bottom)
    pause = True

    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    START = False
                    return
                    
        pygame.display.update()


def gameOver(screen, win):
    """
    Screen that pops up when game is over
    :param screen: screen to draw on
    """
    font = pygame.font.SysFont('Consolas', 115, False, False)
    restart = font.render('Play Again?' , True, NEON)
    yesNo = font.render('y/n' , True, NEON)
    ifWon = font.render('You Win!' , True, NEON)
    ifLost = font.render('Loser!' , True, NEON)
    center = (((BOARD_WIDTH/2) - 150),(BOARD_LENGTH/2) - 70)
    top = (((BOARD_WIDTH/2) - 230),(BOARD_LENGTH/2) - 100)
    bottom = (((BOARD_WIDTH/2) - 80),((BOARD_LENGTH/2)))
    if win:
        screen.fill(BLACK)
        screen.blit(ifWon, center)
        pygame.display.update()
        pygame.time.delay(2000)
    if not win:
        screen.fill(BLACK)
        screen.blit(ifLost, center)
        pygame.display.update()
        pygame.time.delay(2000)
    screen.fill(BLACK)
    screen.blit(restart, top)
    screen.blit(yesNo, bottom)

    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == KEYDOWN:
                if event.key == K_y:
                    main()
                if event.key == K_n:
                    done()
                    
        pygame.display.update()

def splitAsteroid(all_asteroids, all_sprites, hit, newType):
    """
    Splits an asteroid into smaller pieces
    :param all_asteroids: sprite group of all asteroids
    :param all_sprites: sprite group of all sprites
    :param hit: sprite to get position from
    :param newType: type of asteroid to create
    """
    x = hit.getX()
    y = hit.getY()
    a1 = asteroid(newType)
    a1.setY(y)
    a1.setX(x, False)
    all_asteroids.add(a1)
    all_sprites.add(a1)
    a2 = asteroid(newType)
    a2.setY(y)
    a2.setX(x, True)
    all_asteroids.add(a2)
    all_sprites.add(a2)
    
def removeAsteroid(all_asteroids, all_sprites, hit):
    """
    Removes an asteroid
    :param all_asteroids: sprite group of all asteroids
    :param all_sprites: sprite group of all sprites
    :param hit: sprite to be removed
    """
    all_asteroids.remove(hit)
    all_sprites.remove(hit)
    
def done():
    """
    Function to exit the game
    """
    sys.exit()
            
def topGameDisplay(screen, health, enemies):
    """
    Top game display for health and enemies remaining
    :param screen: main screen to draw on
    :param health: ship health
    :param enemies: enemies remaining
    """
    
    pygame.draw.line(screen, WHITE, (0, 0), (800, 0), 50)
    if health <= 0:
        health = 0
    font = pygame.font.SysFont('Consolas', 30, False, False)
    playerHealth = font.render('Health: {0}'.format(health) , True, BLACK)
    enemiesLeft = font.render('Enemies: {0}'.format(enemies) , True, BLACK)
    
    screen.blit(playerHealth, (25, 5))
    screen.blit(enemiesLeft, (650, 5))
            
def asteroid(x):
    """
    Function to create  a new asteroid
    :param x: integer to determine which asteroid to make
    :return:
    """
    image = None
    if (x == 0):
        image = 'images/asteroid1.png'
        kind = 1
    elif x == 1:
        y = random.randrange(0, 3)
        if y == 2:
            image = 'images/asteroid2.png'
            kind = 2
        else:
            kind = 3
            image = 'images/asteroid3.png'

    elif x == 2:
        image = 'images/asteroid3.png'
        kind = 3
    
    return Asteroid(random.randrange(0, 700), 0, random.randrange(-5, 5), random.randrange(1, 5), image, kind)

def level1(all_sprites, all_enemies, ENEMY_SPEED, startPos):
    """
    Creates level 1
    :param all_sprites: sprite group of all sprites
    :param all_enemies: sprite group of all enemies
    :param ENEMY_SPEED: speed of new enemy
    :param startPos: level at which the enemy spawns
    """
    count = 50
    while count < 750:
        e = Enemy(count, startPos, ENEMY_SPEED, 'images/enemy1.png', 1)
        all_sprites.add(e)
        all_enemies.add(e)
        count += SHIPSPACE
        
def pause(screen):
    """
    Function to pause the game
    :param screen: The main game screen
    """
    
    font = pygame.font.SysFont('Consolas', 115, False, False)
    text_to_draw = font.render('Paused' , True, NEON)
    center = (((BOARD_WIDTH/2) - 150),(BOARD_LENGTH/2) - 70)
    screen.blit(text_to_draw, center)
    pause = True

    while pause:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == KEYDOWN:
                if event.key == K_p:
                    pause = False

        pygame.display.update()
        
def level2(all_sprites, all_enemies, ENEMY_SPEED, startPos):
    """
    Creates level 2
    :param all_sprites: sprite group of all sprites
    :param all_enemies: sprite group of all enemies
    :param ENEMY_SPEED: speed of new enemy
    :param startPos: level at which the enemy spawns
    """
    count = 50
    while count < 750:
        e = Enemy(count, startPos, ENEMY_SPEED * -1, 'images/enemy2.png', 2)
        all_enemies.add(e)
        all_sprites.add(e)
        count += SHIPSPACE
        
def level3(all_sprites, all_enemies, ENEMY_SPEED, startPos):
    """
    Creates level 3
    :param all_sprites: sprite group of all sprites
    :param all_enemies: sprite group of all enemies
    :param ENEMY_SPEED: speed of new enemy
    :param startPos: level at which the enemy spawns
    """
    count = 50
    while count < 750:
        e = Enemy(count, startPos, ENEMY_SPEED, 'images/enemy3.png', 3)
        all_enemies.add(e)
        all_sprites.add(e)
        count += SHIPSPACE
        
def level4(all_sprites, all_enemies, ENEMY_SPEED, startPos):
    """
    Creates level 4
    :param all_sprites: sprite group of all sprites
    :param all_enemies: sprite group of all enemies
    :param ENEMY_SPEED: speed of new enemy
    :param startPos: level at which the enemy spawns
    """
    count = 50
    while count < 750:
        e = Enemy(count, startPos, ENEMY_SPEED * -1, 'images/enemy4.png', 4)
        all_enemies.add(e)
        all_sprites.add(e)
        count +=SHIPSPACE
        
def level5(all_sprites, all_enemies, ENEMY_SPEED, startPos):
    """
    Creates level 5
    :param all_sprites: sprite group of all sprites
    :param all_enemies: sprite group of all enemies
    :param ENEMY_SPEED: speed of new enemy
    :param startPos: level at which the enemy spawns
    """
    count = 50
    while count < 750:
        e = Enemy(count, startPos, ENEMY_SPEED, 'images/enemy5.png', 5)
        all_enemies.add(e)
        all_sprites.add(e)
        count += SHIPSPACE
    
def shoot(ship, friendly):
    """
    Creates a new shot object
    :param ship: sprite ship that shot is coming from
    :param friendly: bool to see if ship is friendly
    :return: new ship object
    """
    x = ship.getX()
    y = ship.getY()
    if friendly:
        sh = Shoot(x, y, 'images/shot.png')
    else:
        sh = enemyShoot(x, y, 'images/enemy_shot.png')
    return sh
    
if __name__ == "__main__":
    main()
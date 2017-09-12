import pygame
import random
from pygame.locals import *

class Star(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        """
        Creates a new star object
        :param x: This is the x position of the star
        :param y: This is the y position of the star
        :param image: The image that is going to be used for the star
        """
        super().__init__()
        self.image = pygame.image.load('star.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    def update(self):
        """
        Updates the position of the star
        """
        self.rect.y += 2
        if self.rect.y > 800:
            self.rect.y = -10

class Ship(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        """
        Creates a ship
        :param x: This is the ships x position
        :param y: This is the ships y position
        :param image: The image that is going to be used for the ship
        """
        super().__init__()
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.change_x = 0
        self.change_y = 0
    
    def update(self):
        """
        This updates the image of the ship that should be displayed
        based on the position of the ship
        """
        if(pygame.key.get_pressed()[pygame.K_a] != 0):
            self.image = pygame.image.load('ship_left.png').convert_alpha()
        elif(pygame.key.get_pressed()[pygame.K_d] != 0):
            self.image = pygame.image.load('ship_right.png').convert_alpha()
        elif(pygame.key.get_pressed()[pygame.K_s] != 0):
            self.image = pygame.image.load('ship.png').convert_alpha()
        else:
            self.image = pygame.image.load('ship.png').convert_alpha()
    
    def getX(self):
        """
        gets x position
        :return: Returns the x position of the ship
        """
        return self.rect.x
    def getY(self):
        """
        gets y position
        :return: Returns the y position of the ship
        """
        return self.rect.y
    def setY(self, y):
        """
        sets y position
        :param y: The new y position to be assigned to the ship
        """
        self.rect.y = y
    def setX(self, x):
        """
        sets x position
        :param x: The new x position to be assigned to the ship
        """
        self.rect.x = x
    def setImage(self, image):
        """
        sets image
        :param image: Sets a new image for the ship
        """
        self.image = pygame.image.load(image).convert_alpha()
        
        
class Shoot(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        """
        Creates a new shot obeject from the ship
        :param x: This is the shots x position
        :param y: This is the shots y position
        :param image: The image that is going to be used for the shot
        """
        super().__init__()
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = (x + 15)
        self.rect.y = (y)
    def update(self):
        """
        Updates the y position of the shot so it moves
        """
        self.rect.y -= 30
    def setx(self, x):
        """
        sets x position
        :param x: Sets the new x position of the shot
        """
        self.rect.x = x
    def sety(self, y):
        """
        sets y position
        :param y: Sets the new y position of the shot
        """
        self.rect.y = y
    def getY(self):
        """
        gets y position
        :return: Returns the y position of the ship
        """
        return self.rect.y
        
class enemyShoot(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        """
        Creates a new shot object from an enemy ship
        :param x: This is the shots x position
        :param y: This is the shots y position
        :param image: The image that is going to be used for the shot
        """
        super().__init__()
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = (x + 15)
        self.rect.y = (y)
    def update(self):
        """
        Updates the y position of the shot to move it
        """
        self.rect.y += 10
    def setx(self, x):
        """
        sets x position
        :param x: Sets the x position of the shot
        """
        self.rect.x = x
    def sety(self, y):
        """
        sets y position
        :param y: Sets the y position of the shot
        """
        self.rect.y = y
    def getY(self):
        """
        gets y position
        :return: Returns the y position of the shot
        """
        return self.rect.y
    
    
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, vx, image, row):
        """
        Creates a new enemy ship
        :param x: Sets the y position of the enemy ship
        :param y: Sets the y position of the enemy ship
        :param vx: Sets the ship movement speed
        :param image: Sets the image to be used for the ship
        :param row: Sets which row the ship is gonna be on
        """
        super().__init__()
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vx = vx
        self.row = row
        
    def getX(self):
        """
        gets x position
        :return: Returns the x position of the ship
        """
        return self.rect.x
    def getY(self):
        """
        gets y position
        :return: Returns the y position of the ship
        """
        return self.rect.y
    def setX(self, x):
        """
        sets new y position
        :param x: new x positon
        """
        self.vx *= -1
        if reflect:
            self.rect.x = x
            self.rect.x += self.vx
        else:
            self.rect.x = x
    def setY(self, y):
        """
        Sets new x position
        :param y: Sets the y position
        """
        self.rect.y += y
        
    def setVX(self):
        """
        Sets the movement direction of the ship
        """
        self.vx *= -1
        
    def update(self):
        """
        Updates the ships position
        """
        self.rect.x += self.vx
        
class Asteroid(pygame.sprite.Sprite):
    def __init__(self, x, y, vx, vy, image, kind):
        """
        Creates a new asteroid object
        :param x: Sets the x position
        :param y:Sets the y position
        :param vx: sets the x direction movement speed
        :param vy: sets the y direction movement speed
        :param image: Sets the asteroids image
        :param kind: Sets which type of asteroid it is
        """
        super().__init__()
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vx = vx
        self.vy = vy
        self.kind = kind
        
    def getKind(self):
        """
        Gets the type of asteroid
        :return: The asteroids image
        """
        return self.kind
    def getX(self):
        """
        Returns x position
        :return: x position
        """
        return self.rect.x
    def getY(self):
        """
        Returns y position
        :return: y position
        """
        return self.rect.y
    def setX(self, x, reflect):
        """
        Sets new x position and to reflect or not
        :param x: new x position
        :param reflect: bool value to reflect or not
        """
        self.vx *= -1
        if reflect:
            self.rect.x = x
            self.rect.x += self.vx
        else:
            self.rect.x = x
    def setY(self, y):
        """
        sets y position
        :param y: new y position
        """
        self.rect.y = y  
        
    def update(self):
        """
        Updates the asteroids positon
        """
        l_collide = self.rect.x + self.image.get_width() + self.vx > 860
        r_collide = self.rect.x + self.vx < -60
        if l_collide or r_collide:
            self.vx *= -1

        self.rect.x += self.vx
        self.rect.y += self.vy
        
        
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        """
        Creates a new wall object
        :param x: x position
        :param y: y position
        :param width: width of wall
        :param height: height of wall
        """
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(pygame.Color(255, 0, 255))
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x    
        
        
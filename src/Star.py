import pygame
from pygame.locals import *

'''
Created on May 28, 2015

@author: hulk
'''
class Star(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = pygame.image.load('star.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
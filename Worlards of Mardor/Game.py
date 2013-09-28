__author__ = 'Devin & Stan'
import pygame
import Inventory
import sys
from Constants import *


##
#Game
#Description: runs the main operational code
#
#Variables:
#   inventory - the player's inventory
#
#
#

class Game(object):

    ##
    #__init__
    #
    #
    def __init__(self):
        pygame.init()
        self.inventory = Inventory.Inventory()
        size = (500, 500) #(width, height)
        self.screen = pygame.display.set_mode(size)


a = Game()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    vial = pygame.image.load("bloodvial.png")
    vialrect = vial.get_rect()

    a.screen.fill((0, 0, 0))

    a.screen.blit(vial, vialrect)

    pygame.display.flip()

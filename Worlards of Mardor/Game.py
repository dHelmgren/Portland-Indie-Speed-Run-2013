__author__ = 'Devin & Stan'
import pygame
import Inventory

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
        self.inventory = Inventory.Inventory()           ######WE GOTTA FIX IT
        size = (500, 500) #(width, height)
        self.screen = pygame.display.set_mode(size)


a = Game()
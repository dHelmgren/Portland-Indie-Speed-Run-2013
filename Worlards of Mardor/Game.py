__author__ = 'Devin & Stan'
import pygame
import Inventory
import sys
from Farmable import *
from Worker import *
from Livestock import *
from Crop import *
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

    ##
    #updateState
    #Description: Updates the state of the game and the inventory between turns. Is responsible for
    #   all changes to the game state!
    #
    ##
    def updateState(self):
        #first, update all the farmable's clocks
        for farmable in self.inventory.unitList:
            Farmable.updateClock(farmable)
            #if the clock has hit zero, the object either gains stacks, or is harvestable
            if farmable.clock == 0:
                if isinstance(farmable, Worker) or isinstance(farmable, Livestock):
                    farmable.clock = farmable.time
                    Farmable.updateStacks(farmable)
            else:
                #not totally sure how we want to implement this. should we move it to another list
                #to be managed by the player?
                whatShouldWeDo = "I don't know yet"


a = Game()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    vial = pygame.image.load("bloodvial.png")
    vialrect = vial.get_rect()

    a.screen.fill((0, 0, 0))

    a.screen.blit(vial, vialrect)

    pygame.display.flip()

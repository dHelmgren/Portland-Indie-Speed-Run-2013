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
#   screen - The screen as it is shown to the player
#   state - The state that the game is currently in
#

class Game(object):

    ##
    #__init__
    #
    #
    def __init__(self):
        pygame.init()
        self.inventory = Inventory.Inventory()
        size = (800, 640) #(width, height)
        self.screen = pygame.display.set_mode(size)
        self.state = DWELLINGS

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

    ##
    #drawScreen
    #Description: Draws the side bar for the game including the blood vial, and relevant invs
    #
    #
    def drawScreen(self, screen):
        if self.state is DWELLINGS:
            #draw our dwellings screen
            do = "stuff"
        elif self.state is CROPS:
            #draw our crops screen
            do = "stuff"
        else:
            #draw our shop screen
            do = "stuff"

    ##
    #drawSideBar
    #Description: Draws the side bar for the game including the blood vial, and relevant invs
    #
    #
    def drawSideBar(self, screen):
        vial = pygame.image.load("bloodvial.png")
        vialrect = vial.get_rect()
        vialrect = vialrect.move([710, 0])

        screen.blit(vial, vialrect)

a = Game()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    a.screen.fill((0, 0, 0))
    a.drawScreen(a.screen)
    a.drawSideBar(a.screen)
    pygame.display.flip()

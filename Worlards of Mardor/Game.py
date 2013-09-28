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

        for farmable in self.inventory.unitList:
            if farmable is not None:
                #first, update all the farmable's clock
                Farmable.updateClock(farmable)
                #if the clock has hit zero, the object either gains stacks, or is harvestable
                if farmable.clock == 0:
                    if isinstance(farmable, Worker) or isinstance(farmable, Livestock):
                        farmable.clock = farmable.time
                        Farmable.updateStacks(farmable)
                    #If it's a crop it's ready!
                    elif isinstance(farmable, Crop):
                        Crop.readyForHarvest(farmable)
                elif farmable.clock < 0:
                    Crop.makeRuined(farmable)
                #next, make things eat food, using consume function and the unit's food cost
                self.inventory.consume(farmable.consumption)

    def unitTest(self):
        self.inventory.addUnitPlot(1, Crop(BLOODROOT))
        self.inventory.addUnitPlot(2, Crop(SCREAMING_FUNGUS))
        self.inventory.addUnitPlot(3, Crop(ORCWORT))
        self.inventory.addUnitPlot(4, Livestock(PLAGUE_TOAD))
        self.inventory.addUnitPlot(5, Livestock(DIRE_RAT))

        for num in [0,1,2,3,4,5,6,7,8,9,10,11]:
            print("Turn Number:")
            print(num)
            for unit in self.inventory.unitList:
                if unit is not None:
                    Farmable.printStats(unit)
            print(self.inventory.foodstuffs)
            self.updateState()




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
        rect = vial.get_rect()
        rect = rect.move([710, 0])  #move the vial to the right side of the screen
        screen.blit(vial, rect)

        blood = pygame.image.load("bloodicon.png")
        rect = blood.get_rect()
        rect = rect.move([715, 400])  #move the blood drop to the right side of the screen
        screen.blit(blood, rect)

        food = pygame.image.load("foodicon.png")
        rect = food.get_rect()
        rect = rect.move([715, 500])  #move the blood drop to the right side of the screen
        screen.blit(food, rect)



a = Game()
a.unitTest()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    musicPlaying = pygame.mixer.get_busy()
    if not musicPlaying:
        song = pygame.mixer.Sound("MoonlightHall.mp3")
        song.play()

    a.screen.fill((0, 0, 0))
    a.drawScreen(a.screen)
    a.drawSideBar(a.screen)
    pygame.display.flip()



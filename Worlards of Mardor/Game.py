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
#   click - A way to store where the mouse is pressed down
#   endRect - The space that defines the end button
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
        pygame.display.set_caption('Worlards of Mardor')
        self.reqTithe = 500
        self.state = PLOTS
        self.click = None
        self.endRect = None
        self.plotList = []
        self.titheFrac = str(self.inventory.tithe) + "/" + str(self.reqTithe)
        self.bankNum = str(self.inventory.blood)
        self.foodNum = str(self.inventory.foodstuffs)

    def updateTithe(self):
        self.titheFrac = str(self.inventory.tithe) + "/" + str(self.reqTithe)

    def updateBlood(self):
        self.bankNum = str(self.inventory.blood)

    def updateFood(self):
        self.foodNum = str(self.inventory.foodstuffs)
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
                if self.inventory.foodstuffs >= farmable.consumption:
                    self.inventory.consume(farmable.consumption)
                #if the farmable is consuming more than user has, it takes damage to its hardiness
                else:
                    farmable.hardiness -= 1
        deadNums = (index for index,dead in enumerate(self.inventory.unitList) if dead is not None and dead.hardiness < 0)

        for deceased in deadNums:
            self.inventory.removeUnitPlot(deceased)



    def unitTest(self):
        self.inventory.addUnitPlot(1, Crop(BLOODROOT))
        self.inventory.addUnitPlot(2, Crop(SCREAMING_FUNGUS))
        self.inventory.addUnitPlot(3, Crop(ORCWORT))
        self.inventory.addUnitPlot(4, Livestock(PLAGUE_TOAD))
        self.inventory.addUnitPlot(5, Livestock(DIRE_RAT))

        # print(self.inventory.blood)
        # print(self.inventory.tithe)
        # print(self.inventory.foodstuffs)
        # self.sacrificePlot(0)
        # self.sellPlot(0)
        # self.harvestPlot(0)
        # print(self.inventory.blood)
        # print(self.inventory.tithe)
        # print(self.inventory.foodstuffs)

        # self.endTurn()
        # print(self.inventory.foodstuffs)
        # for unit in self.inventory.unitList:
        #     if unit is not None:
        #         Farmable.printStats(unit)
        # self.harvestPlot(1)
        # self.endTurn()
        # for unit in self.inventory.unitList:
        #     if unit is not None:
        #         Farmable.printStats(unit)
        # print(self.inventory.foodstuffs)
        # self.harvestPlot(1)
        # for unit in self.inventory.unitList:
        #     if unit is not None:
        #         Farmable.printStats(unit)
        # print(self.inventory.foodstuffs)

        # for num in [0,1,2,3,4,5,6,7,8,9,10,11]:
        #     print("Turn Number:")
        #     print(num)
        #     for unit in self.inventory.unitList:
        #         if unit is not None:
        #             Farmable.printStats(unit)
        #     print(self.inventory.foodstuffs)
        #     self.updateState()




    ##
    #drawScreen
    #Description: Draws the side bar for the game including the blood vial, and relevant invs
    #
    ##

    def drawScreen(self, screen):
        if self.state is DWELLINGS:
            #TODO: draw our dwellings screen
            do = "stuff"

        elif self.state is PLOTS:
            xAdjust = 0
            yAdjust = 0
            for unit in self.inventory.unitList:
                plot = None
                if isinstance(unit, Crop):
                    if unit.stacks == 0:
                        plot = pygame.image.load("sprout2.png")
                    elif unit.stacks == 1:
                        plot = pygame.image.load("readyplant.png")
                    elif unit.stacks == -1:
                        plot = pygame.image.load("deadplant.png")

                else:
                    plot = pygame.image.load("dirt.png")
                rect = plot.get_rect()
                rect = rect.move([32 + xAdjust*160, 16 + yAdjust*160])  #move the vial to the right side of the screen
                screen.blit(plot, rect)
                xAdjust += 1
                if xAdjust > 3:
                    yAdjust += 1
                    xAdjust = 0

        else:
            #TODO: draw our shop screen
            do = "stuff"

    ##
    #drawSideBar
    #Description: Draws the side bar for the game including the blood vial, and relevant invs
    #
    #
    def drawSideBar(self, screen):
        asset = pygame.image.load("sidebar.png")
        rect = asset.get_rect()
        rect = rect.move([672, 0])  #move the vial to the right side of the screen
        screen.blit(asset, rect)

        asset = pygame.image.load("bloodvial.png")
        rect = asset.get_rect()
        rect = rect.move([700, 10])  #move the vial to the right side of the screen
        screen.blit(asset, rect)

        asset = pygame.image.load("bloodicon.png")
        rect = asset.get_rect()
        rect = rect.move([685, 340])  #move the blood drop to the right side of the screen
        screen.blit(asset, rect)

        asset = pygame.image.load("foodicon.png")
        rect = asset.get_rect()
        rect = rect.move([685, 450])  #move the food icon to the right side of the screen
        screen.blit(asset, rect)

        asset = pygame.image.load("endbutton.png")
        rect = asset.get_rect()
        rect = rect.move([704, 560])  #move the end button to the right side of the screen
        self.endRect = rect
        screen.blit(asset, rect)

        numFont = pygame.font.SysFont("Lucidia Console", 50)

        self.updateTithe()
        titheLab = numFont.render(self.titheFrac, 1, (255, 0, 0))
        screen.blit(titheLab, (695, 275))

        self.updateBlood()
        bankLab = numFont.render(self.bankNum, 1, (255, 0, 0))
        screen.blit(bankLab, (690, 380))

        self.updateFood()
        foodLab = numFont.render(self.foodNum, 1, (255, 0, 0))
        screen.blit(foodLab, (690, 490))

    ##
    #checkClick
    #Description: Checks to see if the release of a button click is the same place as where it
    #       went down
    #
    #
    def checkClick(self, pos):
        if self.endRect.collidepoint(self.click) and self.endRect.collidepoint(pos):
            return True
        else:
            return False

    ##
    #EVENT OUTCOME FUNCTIONS
    ##

    ##
    #harvestPlot
    #Description: when given a unitPlot, harvests a stack of that unit. If the last stack is harvested, the unit is
    #   removed from the inventory, and foodstuffs are added to the inventory.
    #
    #Parameters:
    #   unitID - the plot number which has been clicked
    ##

    def harvestPlot(self, unitID):
        #if the target is valid...
        if self.inventory.unitList[unitID] is not None:
            #get the object and remove a stack
            unitData = self.inventory.unitList[unitID]
            if unitData.stacks > 0:
                Farmable.removeAStack(unitData)
                #based on the item's turnout, increase the number of foodstuffs
                self.inventory.foodstuffs += unitData.turnout
                #if there are no more stacks, that unit is depleted, remove it
                if unitData.stacks == 0:
                    self.inventory.removeUnitPlot(unitID)
            elif unitData.stacks <= 0:
                print("Not ready to harvest.")

    ##
    #sellPlot
    #Description: sells a in order to add to our currency
    #
    #Parameter:
    #   unitID - the plot number which has been clicked
    ##

    def sellPlot(self, unitID):
        #if the target is valid...
        if self.inventory.unitList[unitID] is not None:
            #get the object and remove a stack
            unitData = self.inventory.unitList[unitID]
            if unitData.stacks > 0:
                Farmable.removeAStack(unitData)
                #based on the item's turnout, increase the blood in our funds
                self.inventory.blood += unitData.sellPrice
                #if there are no more stacks, that unit is depleted, remove it
                if unitData.stacks == 0:
                    self.inventory.removeUnitPlot(unitID)
            elif unitData.stacks <= 0:
                print("Not ready to sell.")

    ##
    #sacrificePlot
    #Description: sacrifices a plot order to add to our tithe
    #
    #Parameter:
    #   unitID - the plot number which has been clicked
    ##

    def sacrificePlot(self, unitID):
        #if the target is valid...
        if self.inventory.unitList[unitID] is not None:
            #get the object and remove a stack
            unitData = self.inventory.unitList[unitID]
            if unitData.stacks > 0:
                Farmable.removeAStack(unitData)
                #based on the item's turnout, increase the blood in our funds
                if isinstance(unitData, Worker):
                    self.inventory.tithe += unitData.sellPrice * 2
                else:
                    self.inventory.tithe += unitData.sellPrice
                #if there are no more stacks, that unit is depleted, remove it
                if unitData.stacks == 0:
                    self.inventory.removeUnitPlot(unitID)
            elif unitData.stacks <= 0:
                print("Not ready to sacrifice.")


    ##
    #endTurn
    #Description: Do all of our cool end-turn thingies
    ##
    def endTurn(self):
        print "End turn button pressed!"
        self.updateState()

    def popUp(self, offset, screen):
        asset = pygame.image.load("window.png")
        rect = asset.get_rect()
        rect = rect.move([offset[0], offset[1]])
        screen.blit(asset, rect)

        asset = pygame.image.load("winbutt1.png")
        rect = asset.get_rect()
        rect = rect.move([offset[0], offset[1]])
        rect = rect.move([13, 210])
        screen.blit(asset, rect)


a = Game()
a.unitTest()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN: a.click = pygame.mouse.get_pos()
        elif event.type == pygame.MOUSEBUTTONUP:
            if a.checkClick(pygame.mouse.get_pos()):
                a.endTurn()

    musicPlaying = pygame.mixer.get_busy()
    if not musicPlaying:
        song = pygame.mixer.Sound("MoonlightHall.wav")
        #song.play()

    a.screen.fill((0, 0, 0))
    a.drawScreen(a.screen)
    a.popUp((500, 500), a.screen)
    a.drawSideBar(a.screen)
    pygame.display.flip()



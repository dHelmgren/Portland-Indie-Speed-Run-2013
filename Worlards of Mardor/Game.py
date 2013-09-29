__author__ = 'Devin & Stan'
import pygame
import Inventory
import sys
import random
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
        pygame.display.set_caption('Exsanguia')
        self.reqTithe = 50
        self.state = PLOTS
        self.click = None
        self.endRect = None
        self.plotList = []
        self.titheFrac = str(self.inventory.tithe) + "/" + str(self.reqTithe)
        self.bankNum = str(self.inventory.blood)
        self.foodNum = str(self.inventory.foodstuffs)
        self.plotPaths = []
        self.plagueT = []
        self.rats = []
        self.currentEntities = []
        self.popUpActive = False
        self.selectedPlot = None


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
        plotCounter = 0
        for farmable in self.inventory.unitList:
            if plotCounter > self.inventory.unitList[16].stacks:
                #remove the current unit if we don't have enough Goblins
                self.inventory.removeUnitPlot(plotCounter - 1)
            elif farmable is not None:
                plotCounter += 1
                #first, update all the farmable's clock
                Farmable.updateClock(farmable)

                #TODO We're not getting to our harvestable graphic- DO SOMETHING!!

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

        if self.inventory.unitList[16].hardiness < 0 or self.inventory.unitList[16].stacks < 0:
            print("Your goblins cannibalize each other and destroy your farm. Your day at the alter is tentatively scheduled for next week.")
            sys.exit(0)

        #enumerates over all of the units, finds those defined as dead (hardiness < 0) and returns a list of their
        #indicies
        deadNums = (index for index,dead in enumerate(self.inventory.unitList) if dead is not None and dead.hardiness < 0)

        for deceasedIndex in deadNums:
            self.inventory.removeUnitPlot(deceasedIndex)


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
        self.currentEntities = []
        if self.state is DWELLINGS:
            #TODO: draw our dwellings screen
            do = "stuff"

        elif self.state is PLOTS:
            #initialize some values used later
            xAdjust = 0
            yAdjust = 0
            unitID = 0
            frogCount = 0
            ratCount = 0

            for path in self.plotPaths:
                screen.blit(path[0], path[1])

            for unit in self.inventory.unitList:
                #remove the previous picture
                plot = None
                #don't do this for our GOBLINs
                if isinstance(unit, Worker):
                    break
                #draw the appropriate image for the crop
                elif isinstance(unit, Crop):
                    if unit.type == ORCWORT:
                        if unit.stacks == 0:
                            plot = pygame.image.load("orcwort1.png")
                        elif unit.stacks == 1:
                            plot = pygame.image.load("orcwort2.png")
                        elif unit.stacks == 2:
                            plot = pygame.image.load("orcwort3.png")
                        elif unit.stacks == -1:
                            plot = pygame.image.load("orcwort4.png")
                    elif unit.type == SCREAMING_FUNGUS:
                        if unit.stacks == 0:
                            plot = pygame.image.load("shrieker1.png")
                        elif unit.stacks == 1:
                            plot = pygame.image.load("shrieker2.png")
                        elif unit.stacks == 2:
                            plot = pygame.image.load("shrieker3.png")
                        elif unit.stacks == -1:
                            plot = pygame.image.load("shrieker4.png")
                    elif unit.type == BLOODROOT:
                        if unit.stacks == 0:
                            plot = pygame.image.load("bloodroot1.png")
                        elif unit.stacks == 1:
                            plot = pygame.image.load("bloodroot2.png")
                        elif unit.stacks == 2:
                            plot = pygame.image.load("bloodroot3.png")
                        elif unit.stacks == -1:
                            plot = pygame.image.load("bloodroot4.png")

                #draw the appropriate image for the Livestock
                elif isinstance(unit, Livestock):
                    if unit.type == PLAGUE_TOAD:
                        plot = self.plagueT[frogCount]
                        frogCount += 1
                    elif unit.type == DIRE_RAT:
                        plot = self.rats[ratCount]
                        ratCount += 1
                    else:
                        plot = pygame.image.load("pen.png")
                #if it isn't either, just draw dirt
                else:
                    plot = pygame.image.load("dirt.png")
                #get the rect of our button image, move it to the right location
                rect = plot.get_rect()
                rect = rect.move([32 + xAdjust*160, 16 + yAdjust*160])
                #create an entry for currentEntities that includes the button's rect, unit object, and the number of the
                #plot
                if not self.popUpActive:
                    self.currentEntities.append((rect, unit, unitID))
                else:
                    self.popUp([200, 200], self.screen)
                #draw it
                screen.blit(plot, rect)
                #adjust where the next draw will happen
                xAdjust += 1
                if xAdjust > 3:
                    yAdjust += 1
                    xAdjust = 0
                #increment the unitID
                unitID += 1
        #state is STORE
        else:
            bar = pygame.image.load("tempstorebar.png")
            rect = bar.get_rect()
            rect = rect.move([0, 448])
            self.screen.blit(bar, rect)

            xAdjust = 0
            yAdjust = 0
            for item in [BLOODROOT, SCREAMING_FUNGUS, ORCWORT, PLAGUE_TOAD, DIRE_RAT, GOBLIN]:
                if item is BLOODROOT:
                    icon = pygame.image.load("shopBloodroot.png")
                elif item is SCREAMING_FUNGUS:
                    icon = pygame.image.load("shopShreiker.png")
                elif item is ORCWORT:
                    icon = pygame.image.load("shopOrcwort.png")
                elif item is PLAGUE_TOAD:
                    icon = pygame.image.load("shopToad.png")
                elif item is DIRE_RAT:
                    icon = pygame.image.load("shopRat.png")
                elif item is GOBLIN:
                    icon = pygame.image.load("shopGoblin.png")
                rect = icon.get_rect()
                rect = rect.move([16 + 192 * xAdjust, 470 + 96 * yAdjust])
                self.screen.blit(icon, rect)
                if not self.popUpActive:
                    self.currentEntities.append((rect, item, None))
                #draw the popup
                else:
                    self.popUp([200, 200], self.screen)
                xAdjust += 1
                if xAdjust > 2:
                    yAdjust += 1
                    xAdjust = 0


        self.currentEntities.append((self.endRect, ENDBUTTON, None))

    ##
    #drawSideBar
    #Description: Draws the side bar for the game including the blood vial, and relevant invs
    #
    #
    def drawSideBar(self, screen):
        asset = pygame.image.load("sidebar.png")
        rect = asset.get_rect()
        rect = rect.move([672, 0])
        screen.blit(asset, rect)

        asset = pygame.image.load("bloodvial.png")
        rect = asset.get_rect()
        rect = rect.move([700, 10])
        screen.blit(asset, rect)

        asset = pygame.image.load("bloodicon.png")
        rect = asset.get_rect()
        rect = rect.move([685, 340])
        screen.blit(asset, rect)

        asset = pygame.image.load("foodicon.png")
        rect = asset.get_rect()
        rect = rect.move([685, 450])
        screen.blit(asset, rect)

        asset = pygame.image.load("endbutton.png")
        rect = asset.get_rect()
        rect = rect.move([704, 560])
        self.endRect = rect
        screen.blit(asset, rect)

        numFont = pygame.font.SysFont("Lucidia Console", 30)

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

    def checkClick(self, pos, rect):
        if rect is None:
            return False

        if rect.collidepoint(self.click) and rect.collidepoint(pos):
            return True
        else:
            return False

    ##
    #EVENT OUTCOME FUNCTIONS
    ##

    ##
    #buyItem
    #Description: from the shop menu pop up, adds the proper thing to your inventory
    ##
    def buyItem(self):
        #if the thing you selected to buy is a GOBLIN, it will be added as a stack
        if self.inventory.blood < UNIT_STATS[self.selectedPlot][COST]:
            return False
        if self.selectedPlot == GOBLIN:
            self.inventory.unitList[16].stacks += 1
            self.inventory.spendBlood(UNIT_STATS[self.selectedPlot][COST])
            return True
        elif self.inventory.plotsWorked + 1 <= self.inventory.unitList[16].stacks:
            counter = 0
            for slot in self.inventory.unitList:
                if slot is None:
                    if self.selectedPlot <= ORCWORT:
                        self.inventory.addUnitPlot(counter, Crop(self.selectedPlot))
                        self.inventory.spendBlood(UNIT_STATS[self.selectedPlot][COST])
                        return True
                    else:
                        self.inventory.addUnitPlot(counter, Livestock(self.selectedPlot))
                        self.inventory.spendBlood(UNIT_STATS[self.selectedPlot][COST])
                        return True
                counter += 1
        return False



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

    ##
    #popUp
    #Description: Draws our game's popup window
    #
    def popUp(self, offset, screen):
        if self.state == PLOTS:
            self.currentEntities = []
            asset = pygame.image.load("window.png")
            rect = asset.get_rect()
            rect = rect.move([offset[0], offset[1]])
            screen.blit(asset, rect)

            asset = pygame.image.load("winbutt1.png")
            rect = asset.get_rect()
            rect = rect.move([offset[0], offset[1]])
            rect = rect.move([13, 210])
            screen.blit(asset, rect)
            self.currentEntities.append((rect, BUTTON1, None))

            asset = pygame.image.load("winbutt2.png")
            rect = asset.get_rect()
            rect = rect.move([offset[0], offset[1]])
            rect = rect.move([113, 210])
            screen.blit(asset, rect)
            self.currentEntities.append((rect, BUTTON2, None))

            asset = pygame.image.load("winbutt3.png")
            rect = asset.get_rect()
            rect = rect.move([offset[0], offset[1]])
            rect = rect.move([213, 210])
            screen.blit(asset, rect)
            self.currentEntities.append((rect, BUTTON3, None))

        elif self.state == SHOP:
            self.currentEntities = []
            asset = pygame.image.load("shopdisplay.png")
            rect = asset.get_rect()
            rect = rect.move([330, 0])
            screen.blit(asset, rect)

            asset = pygame.image.load("winbutt1.png")
            rect = asset.get_rect()
            rect = rect.move([offset[0], offset[1]])
            rect = rect.move([13, 210])
            screen.blit(asset, rect)
            self.currentEntities.append((rect, BUTTON1, None))

            asset = pygame.image.load("winbutt3.png")
            rect = asset.get_rect()
            rect = rect.move([offset[0], offset[1]])
            rect = rect.move([213, 210])
            screen.blit(asset, rect)
            self.currentEntities.append((rect, BUTTON3, None))

    ##
    #changeState
    #Description: Changes the state
    def changeState(self, direction):
        self.popUpActive = False
        self.state += direction
        if self.state > -1:
            self.state = SHOP
        elif self.state < -3:
            self.state = DWELLINGS

        if self.state == PLOTS:
            self.plotPaths = []
            paths = []
            paths.append(pygame.image.load("path1.png"))
            paths.append(pygame.image.load("path2.png"))
            paths.append(pygame.image.load("path3.png"))
            paths.append(pygame.image.load("pathcross.png"))

            for y in range(0, 25):
                for x in range(0, 25):
                    asset = random.choice(paths)
                    rect = asset.get_rect()
                    rect = rect.move([x*32, y*32 - 16])
                    self.plotPaths.append((asset, rect))
            self.plagueT = []
            toads = []
            toads.append(pygame.image.load("toads1.png"))
            toads.append(pygame.image.load("toads2.png"))
            toads.append(pygame.image.load("toads3.png"))
            toads.append(pygame.image.load("toads4.png"))
            for x in range(0, 12):
                self.plagueT.append(random.choice(toads))
            self.rats = []
            dires = []
            dires.append(pygame.image.load("rats1.png"))
            dires.append(pygame.image.load("rats2.png"))
            dires.append(pygame.image.load("rats3.png"))
            for x in range(0, 12):
                self.rats.append(random.choice(dires))

    ##
    #clickCallback
    #Description: The method called when something on our screen has been clicked
    #
    # culprit - A tuple containing ([the rect of our culprit], [and their metadata], [and their plot ID where relevant])
    def clickCallback(self, culprit):
        print "CLICK CALLBACK!"
        print culprit[2]
        if self.state == PLOTS:
            if culprit[2] >= 0 and culprit[1] is not None:
                self.popUpActive = True
                self.selectedPlot = culprit[2]
            elif culprit[1] == BUTTON1:
                self.harvestPlot(self.selectedPlot)
                self.popUpActive = False
                self.selectedPlot = None
            elif culprit[1] == BUTTON2:
                self.sellPlot(self.selectedPlot)
                self.popUpActive = False
                self.selectedPlot = None
            elif culprit[1] == BUTTON3:
                self.sacrificePlot(self.selectedPlot)
                self.popUpActive = False
                self.selectedPlot = None
        elif self.state == SHOP:
            #if the pressed button is not a part of pop up
            if culprit[1] >= 0:
                self.popUpActive = True
                self.selectedPlot = culprit[1]
            #if the button IS a part of pop up
            elif culprit[1] == BUTTON1:  #This will buy the thing!
                if not self.buyItem():
                    print("there is no room")
                self.popUpActive = False
                self.selectedPlot = None
            elif culprit[1] == BUTTON2:
                self.popUpActive = False
                self.selectedPlot = None
            elif culprit[1] == BUTTON3:
                self.popUpActive = False
                self.selectedPlot = None

        if culprit[1] == ENDBUTTON:
            self.endTurn()


a = Game()
a.changeState(0)
#a.unitTest()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN: a.click = pygame.mouse.get_pos()
        elif event.type == pygame.MOUSEBUTTONUP:

            for thing in a.currentEntities:
                if a.checkClick(pygame.mouse.get_pos(), thing[0]):
                    a.clickCallback(thing)

        elif event.type == pygame.KEYDOWN:
            a.changeState(1)


    musicPlaying = pygame.mixer.get_busy()
    if not musicPlaying:
        song = pygame.mixer.Sound("MoonlightHall.wav")
        #song.play()

    a.screen.fill((0, 0, 0))
    a.drawScreen(a.screen)
    a.drawSideBar(a.screen)
    pygame.display.flip()



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
        self.reqTithe = 10
        self.state = SHOP
        self.click = None
        self.endRect = None
        self.plotList = []
        self.titheFrac = str(self.inventory.tithe) + "/" + str(self.reqTithe)
        self.bankNum = str(self.inventory.blood)
        self.foodNum = str(self.inventory.foodstuffs)
        self.gobNum = str(3)
        self.calendar = 12
        self.year = 0
        self.plotPaths = []
        self.plagueT = []
        self.rats = []
        self.currentEntities = []
        self.popUpActive = False
        self.selectedPlot = None
        self.clerkDlg = False
        self.clerkSpch = None
        self.favor = 0.05
        self.eventTime = True
        self.intro = [True, 0]#30]
        self.shopNoob = True
        self.plotNoob = True
        self.slaveNoob = True
        self.randEventText = ["", ""]
        self.gameOver = False


    def updateTithe(self):
        self.titheFrac = str(self.inventory.tithe) + "/" + str(self.reqTithe)

    def updateBlood(self):
        self.bankNum = str(self.inventory.blood)

    def updateFood(self):
        self.foodNum = str(self.inventory.foodstuffs)

    def updateGobs(self):
        self.gobNum = str(self.inventory.unitList[16].stacks)
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
            self.gameOver = True
            self.eventTime = True

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
    #VIEW FUNCTIONS
    ##

    ##
    #drawScreen
    #Description: Draws the side bar for the game including the blood vial, and relevant invs
    #
    ##

    def drawScreen(self, screen):
        if not self.eventTime:
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
                            if unit.clock == unit.time:
                                plot = pygame.image.load("orcwort1.png")
                            elif unit.clock > 0:
                                plot = pygame.image.load("orcwort2.png")
                            elif unit.clock == 0:
                                plot = pygame.image.load("orcwort3.png")
                            elif unit.stacks == -1:
                                plot = pygame.image.load("orcwort4.png")
                        elif unit.type == SCREAMING_FUNGUS:
                            if unit.clock == unit.time:
                                plot = pygame.image.load("shrieker1.png")
                            elif unit.clock > 0:
                                plot = pygame.image.load("shrieker2.png")
                            elif unit.clock == 0:
                                plot = pygame.image.load("shrieker3.png")
                            elif unit.stacks == -1:
                                plot = pygame.image.load("shrieker4.png")
                        elif unit.type == BLOODROOT:
                            if unit.clock == unit.time:
                                plot = pygame.image.load("bloodroot1.png")
                            elif unit.clock > 0:
                                plot = pygame.image.load("bloodroot2.png")
                            elif unit.clock == 0:
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
                asset = pygame.image.load("shopfront.png")
                rect = asset.get_rect()
                self.screen.blit(asset, rect)

                asset = pygame.image.load("storebar.png")
                rect = asset.get_rect()
                rect = rect.move([0, 448])
                self.screen.blit(asset, rect)

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
                    rect = rect.move([60 + 250 * xAdjust, 465 + 96 * yAdjust])
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
                if self.clerkDlg:
                    asset = pygame.image.load("shopDlg.png")
                    rect = asset.get_rect()
                    rect = rect.move([290, 315])
                    self.screen.blit(asset, rect)
                    if self.clerkSpch is None:
                        options = []
                        if self.inventory.blood <= 30:
                            speech1 = []
                            speech1.append("What do you want, worm? I do not have")
                            speech1.append("time for your weakness.")
                            options.append(speech1)
                            speech2 = []
                            speech2.append("Ah. You. You'd better not incinerate")
                            speech2.append("my shelver again.")
                            options.append(speech2)
                        elif self.inventory.blood <= 80:
                            speech1 = []
                            speech1.append("I see you haven't been killed yet.")
                            speech1.append("How surprising.")
                            options.append(speech1)
                            speech2 = []
                            speech2.append("It's amazing that you don't nauseate")
                            speech2.append("me to look at anymore.")
                            options.append(speech2)
                        else:
                            speech1 = []
                            speech1.append("Once again you seek my services. And")
                            speech1.append("what might you need, hm?")
                            options.append(speech1)
                            speech2 = []
                            speech2.append("Welcome, Great One. Please, how my I")
                            speech2.append("serve you...?")
                            options.append(speech2)
                        self.clerkSpch = random.choice(options)

                    numFont = pygame.font.SysFont("Courier", 15)
                    x = 0

                    for ch in self.clerkSpch:
                        flavor = numFont.render(ch, 1, (0, 0, 0))
                        screen.blit(flavor, (320, 340 +x*20))
                        x += 1

            asset = pygame.image.load("arrowL.png")
            rect = asset.get_rect()
            rect = rect.move([0, 320])
            self.screen.blit(asset, rect)
            self.currentEntities.append((rect, LEFT, None))

            asset = pygame.image.load("arrowR.png")
            rect = asset.get_rect()
            rect = rect.move([640, 320])
            self.screen.blit(asset, rect)
            self.currentEntities.append((rect, RIGHT, None))

            self.currentEntities.append((self.endRect, ENDBUTTON, None))
        else:#THIS IS AN EVENT
            if not self.intro[0]:
                if not self.gameOver:
                    asset = pygame.image.load("eventScreen.png")
                    rect = asset.get_rect()
                    self.screen.blit(asset, rect)
                    self.currentEntities.append((rect, EVENT, None))
                    numFont = pygame.font.SysFont("Courier", 15)
                    x = 0
                    for ch in self.randEventText:
                        flavor = numFont.render(ch, 1, (0, 0, 0))
                        screen.blit(flavor, (220, 220 +x*20))
                        x += 1
                else:
                    asset = pygame.image.load("gameOver.png")
                    rect = asset.get_rect()
                    rect = rect.move([50, 96])
                    self.screen.blit(asset, rect)
                    self.currentEntities.append((rect, EVENT, None))
            else:
                self.intro[1] -= 1
                asset = pygame.image.load("Exsanguia.png")
                rect = asset.get_rect()
                rect = rect.move([-50, 0])
                self.screen.blit(asset, rect)
                self.currentEntities.append((rect, EVENT, None))
                if self.intro[1] <= 0:
                    asset = pygame.image.load("window.png")
                    rect = asset.get_rect()
                    rect = rect.move([200, 380])
                    self.screen.blit(asset, rect)
                    numFont = pygame.font.SysFont("Courier", 15)
                    intro = ["Welcome, devout follower of Exsanguia.",
                             "It is time to show your zeal. Collect",
                             "tithe for our Goddess, and she shall",
                             "favor you. You have been given the",
                             "tools necessary to succeed, and as",
                             "your influence grows, so too shall",
                             "your wealth. Do not fail.", "", ""
                             "[CLICK TO CONTIUE]"]
                    x = 0
                    for ch in intro:
                        flavor = numFont.render(ch, 1, (0, 0, 0))
                        screen.blit(flavor, (220, 410 +x*20))
                        x += 1

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

        progress = (self.inventory.tithe/self.reqTithe)
        if self.inventory.tithe > self.reqTithe:
            asset = pygame.image.load("vial7.png")
        elif progress <= (1/6):
            asset = pygame.image.load("vial1.png")
        elif progress <= (2/6):
            asset = pygame.image.load("vial2.png")
        elif progress <= (3/6):
            asset = pygame.image.load("vial3.png")
        elif progress <= (4/6):
            asset = pygame.image.load("vial4.png")
        elif progress <= (5/6):
            asset = pygame.image.load("vial5.png")
        elif progress <= 1:
            asset = pygame.image.load("vial6.png")


        rect = asset.get_rect()
        rect = rect.move([700, 10])
        screen.blit(asset, rect)

        asset = pygame.image.load("bloodicon.png")
        rect = asset.get_rect()
        rect = rect.move([685, 308])
        screen.blit(asset, rect)

        asset = pygame.image.load("foodicon.png")
        rect = asset.get_rect()
        rect = rect.move([685, 370])
        screen.blit(asset, rect)

        asset = pygame.image.load("endbutton.png")
        rect = asset.get_rect()
        rect = rect.move([704, 560])
        self.endRect = rect
        screen.blit(asset, rect)

        asset = pygame.image.load("goblinicon.png")
        rect = asset.get_rect()
        rect = rect.move([684, 428])
        screen.blit(asset, rect)

        numFont = pygame.font.SysFont("Lucidia Console", 30)

        self.updateTithe()
        titheLab = numFont.render(self.titheFrac, 1, (255, 0, 0))
        screen.blit(titheLab, (695, 275))

        self.updateBlood()
        bankLab = numFont.render(self.bankNum, 1, (255, 0, 0))
        screen.blit(bankLab, (690, 348))

        self.updateFood()
        foodLab = numFont.render(self.foodNum, 1, (255, 0, 0))
        screen.blit(foodLab, (690, 408))

        self.updateGobs()
        gobLab = numFont.render(self.gobNum, 1, (255, 0, 0))
        screen.blit(gobLab, (690, 408 + 50))

        calenLab = numFont.render(str(self.calendar), 1, (255, 0, 0))
        screen.blit(calenLab, (690, 500))

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
                self.inventory.blood += 5
                #if there are no more stacks, that unit is depleted, remove it
                if unitData.stacks == 0:
                    self.inventory.removeUnitPlot(unitID)
            elif unitData.stacks == 0:
                print("Not ready to harvest.")
            else:
                self.inventory.removeUnitPlot(unitID)

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
                    self.inventory.tithe += unitData.sellPrice * 5
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
        self.intro = [False, 0]
        self.eventEngine()
        self.updateState()
        self.calendar -= 1
        if self.calendar == 0:
            self.judgement()

    ##
    #judgement
    #Description: at the end of the year, decides whether the player has lost, and calculates the new tithe
    #
    ##

    def judgement(self):
        if self.inventory.tithe < self.reqTithe:
            self.gameOver = True
            self.eventTime = True
        self.year += 1
        self.reqTithe = (10 + self.reqTithe) * (self.inventory.tithe/self.reqTithe)
        self.calendar = 12
        self.inventory.tithe = 0


    ##
    #eventEngine
    #Description: generates an event, and runs the consequences
    ##

    def eventEngine(self):
        #if your luck is worse than your favor gen event
        luck = random.random()
        if luck < self.favor:
            luck = random.random()
            self.favor = 0.05
            self.eventTime = True
            #Blood Event
            if luck < .25:
                luck = random.random()
                if luck < .3:
                    self.randEventText = VAMPIRES
                elif luck < .6:
                    self.ranEventText = INJURY
                else:
                    self.randEventText = LOCAL_TAXES
                self.inventory.blood -= 20
                if self.inventory.blood < 0:
                    self.inventory.blood = 0
            #Food Event
            elif .25 <= luck and luck < .5:
                luck = random.random()
                if luck < .3:
                    self.randEventText = WITHER
                elif luck < .6:
                    self.ranEventText = GEL_CUBE
                else:
                    self.randEventText = SMALL
                self.inventory.foodstuffs -= 2
                if self.inventory.foodstuffs < 0:
                    self.inventory.foodstuffs = 0

            #Livestock Event
            elif .5 <= luck and luck < .75:
                luck = random.random()
                if luck < .3:
                    self.randEventText = BARBARIANS
                elif luck < .6:
                    self.ranEventText = RAT_ESCAPE
                else:
                    self.randEventText = FIRE_WRYM
                haveLivestock = False
                unluckyLivestock = None
                for unit in self.inventory.unitList:
                    if isinstance(unit, Livestock):
                        haveLivestock = True
                        unluckyLivestock = unit
                        break
                if haveLivestock:
                    unluckyLivestock.stacks -= 1
                else:
                    self.eventTime = False

            #Goblin Event
            else:
                luck = random.random()
                if luck < .3:
                    self.randEventText = EMPTY_LANDS
                elif luck < .6:
                    self.ranEventText = DO_GOODERS
                else:
                    self.randEventText = FEED_FRENZY
                self.inventory.unitList[16].stacks -= 1

        else:
            self.favor += 0.05
            print("the month passes quietly")


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
            rect = rect.move([45, 210])
            screen.blit(asset, rect)
            self.currentEntities.append((rect, BUTTON1, None))

            asset = pygame.image.load("winbutt2.png")
            rect = asset.get_rect()
            rect = rect.move([offset[0], offset[1]])
            rect = rect.move([145, 210])
            screen.blit(asset, rect)
            self.currentEntities.append((rect, BUTTON2, None))

            asset = pygame.image.load("winbutt3.png")
            rect = asset.get_rect()
            rect = rect.move([offset[0], offset[1]])
            rect = rect.move([245, 210])
            screen.blit(asset, rect)
            self.currentEntities.append((rect, BUTTON3, None))

        elif self.state == SHOP:
            self.clerkDlg = False
            self.clerkSpch = None
            self.currentEntities = []
            asset = pygame.image.load("shopdisplay.png")
            rect = asset.get_rect()
            rect = rect.move([330, 0])
            screen.blit(asset, rect)

            things = [BLOODROOT, SCREAMING_FUNGUS, ORCWORT, PLAGUE_TOAD, DIRE_RAT, GOBLIN]

            description = []
            if things[self.selectedPlot] is BLOODROOT:
                asset = pygame.image.load("shopBloodroot.png")
                flavor = pygame.image.load("bldrtFlv.png")
                name = "BLOODROOT"
                cost = "10"
                description.append("Known for killing off nearby plants,")
                description.append("birds and some small mammals.")
                description.append("Important peasants should use")
                description.append("protective gear.")
            elif things[self.selectedPlot] is SCREAMING_FUNGUS:
                asset = pygame.image.load("shopShreiker.png")
                flavor = pygame.image.load("shrkFlv.png")
                name = "SCREAMING FUNGUS"
                cost = "20"
                description.append("Possibly the best food and cash crop")
                description.append("any Warlord could ask for. If it")
                description.append("wasn't for all the screaming....")
            elif things[self.selectedPlot] is ORCWORT:
                asset = pygame.image.load("shopOrcwort.png")
                flavor = pygame.image.load("orcwrtFlv.png")
                name = "ORCWORT"
                cost = "40"
                description.append("A simple white flower whose seeds")
                description.append("cause hemophilia. And they said")
                description.append("blood doesn't grow on trees!")
            elif things[self.selectedPlot] is PLAGUE_TOAD:
                asset = pygame.image.load("shopToad.png")
                flavor = pygame.image.load("bldrtFlv.png")
                name = "PLAGUE TOAD"
                cost = "30"
                description.append("If the peasants complain, sacrifice")
                description.append("them. The Plague Toads are more")
                description.append("valuable, anyway.")
            elif things[self.selectedPlot] is DIRE_RAT:
                asset = pygame.image.load("shopRat.png")
                flavor = pygame.image.load("bldrtFlv.png")
                name = "DIRE RAT"
                cost = "80"
                description.append("Dire-Rat smells of decay and")
                description.append("tastes of vomit. What nostalgia")
                description.append("it must arouse in you.")
            elif things[self.selectedPlot] is GOBLIN:
                asset = pygame.image.load("shopGoblin.png")
                flavor = pygame.image.load("bldrtFlv.png")
                name = "GOBLIN"
                cost = "100"
                description.append("Nearly useless sacks of skin and")
                description.append("organs, goblins are nevertheless")
                description.append("perfect slaves. Easily dominated,")
                description.append("easily fed... easily slain.")

            rect = asset.get_rect()
            rect = rect.move([340, 10])
            screen.blit(asset, rect)

            rect = flavor.get_rect()
            rect = rect.move([360, 190])
            screen.blit(flavor, rect)

            asset = pygame.image.load("shopframe.png")
            screen.blit(asset, rect)

            asset = pygame.image.load("bloodicon.png")
            rect = asset.get_rect()
            rect = rect.move([430, 45])
            screen.blit(asset, rect)

            numFont = pygame.font.SysFont("Courier", 20)
            price = numFont.render(cost, 1, (0, 0, 0))
            screen.blit(price, (465, 50))

            numFont = pygame.font.SysFont("Courier", 25)
            title = numFont.render(name, 1, (0, 0, 0))
            screen.blit(title, (420, 10))

            numFont = pygame.font.SysFont("Courier", 15)
            x = 0
            for des in description:
                flavor = numFont.render(des, 1, (0, 0, 0))
                screen.blit(flavor, (345, 90 +x*20))
                x += 1

            asset = pygame.image.load("winbutt5.png")
            rect = asset.get_rect()
            rect = rect.move([offset[0], offset[1]])
            rect = rect.move([200, 210])
            screen.blit(asset, rect)
            self.currentEntities.append((rect, BUTTON1, None))

            asset = pygame.image.load("winbutt4.png")
            rect = asset.get_rect()
            rect = rect.move([offset[0], offset[1]])
            rect = rect.move([320, 210])
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

        elif self.state == SHOP:
            self.clerkDlg = True

    ##
    #clickCallback
    #Description: The method called when something on our screen has been clicked
    #
    # culprit - A tuple containing ([the rect of our culprit], [and their metadata], [and their plot ID where relevant])
    def clickCallback(self, culprit):
        if culprit[1] == EVENT:
            self.eventTime = False
        if culprit[1] is RIGHT:
            self.changeState(1)
        elif culprit[1] is LEFT:
            self.changeState(-1)
        elif self.state == PLOTS:
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
                self.clerkDlg = True
                if not self.buyItem():
                    print("there is no room")
                self.popUpActive = False
                self.selectedPlot = None
            elif culprit[1] == BUTTON2:
                self.clerkDlg = True
                self.popUpActive = False
                self.selectedPlot = None
            elif culprit[1] == BUTTON3:
                self.clerkDlg = True
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


    musicPlaying = pygame.mixer.get_busy()
    if not musicPlaying:
        song = pygame.mixer.Sound("MoonlightHall.wav")
        song.play()

    a.screen.fill((0, 0, 0))
    a.drawScreen(a.screen)
    if not a.eventTime: a.drawSideBar(a.screen)
    pygame.display.flip()



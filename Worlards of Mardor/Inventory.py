__author__ = 'Devin & Stan'

from Worker import *
from Crop import *
from Livestock import *
from Constants import *
##
#Inventory
#Description: This file holds all the relevant information about a player's inventory
#
#Variables:
#   blood - the amount of currency currently held by the
#   tithe - the amount of blood given to the tithe so far
#   favor - the amount of favor the player holds with their deity
#   unitList[] - the units owned by the player
#   foodstuffs - the amount of food that the player can give to their livestock and workers
#   maxUnits - the number of plots that the user has right now
#   maxPlots - the maximum number of plots available to the player
##

class Inventory(object):

    ##
    #__init__
    #Description: initialized the player's inventory
    #
    ##
    def __init__(self):
        self.blood = 300
        self.tithe = 0
        self.favor = 0.5
        self.foodstuffs = 10
        self.unitList = [None]*17
        self.unitList[16] = Worker(GOBLIN)
        self.maxUnits = 6
        self.maxPlots = 10
        #sets the number of useable workers to three for the beginning of the game
        self.unitList[0].modifyWorkerNumber()

    ##
    #removeUnitPlot
    #Description: removes the unit from the unitList, which will be reflected when the GUI updates
    #
    #Parameter:
    #   plotID - the number associated with the player selected plot. It is between 0 and 9
    def removeUnitPlot(self, plotID):
        self.unitList[plotID] = None


    ##
    #addUnitPlot
    #Description: adds a unit to one of the available plots
    #
    #Parameters:
    #   plotID - the id number associated with the selected plot
    #   unit - the initialized unit object that will be stored in that plot
    #
    #Implications:
    #   The unit will have to be initialized before it is given to the Inventory. Checking to see if the number of plots
    #   is full must be done ELSEWHERE
    #
    def addUnitPlot(self, plotID, unit):
        self.unitList[plotID] = unit

    ##
    #consume
    #Description: modifies the food total using the consumption cost of a unit
    #
    #Parameter:
    #   amtToEat - the consumption cost of a unit
    #
    #TODO: negative food total?
    def consume(self, amtToEat):
        self.foodstuffs -= amtToEat


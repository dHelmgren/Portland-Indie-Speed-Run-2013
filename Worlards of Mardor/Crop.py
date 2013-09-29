__author__ = 'Devin'

from Farmable import *

##
#Crop
#Description: Contains methods and variables that define the operation of a crop
#
#Variable:
#   harvestable - a boolean to indicate if a crop can be harvested
##

class Crop(Farmable):

    def __init__(self, unitType):
        super(Crop, self).__init__(unitType)
        self.harvestable = False

    def readyForHarvest(self):
        self.harvestable = True
        #a plant starts with 0 stacks, gains a stack when ready for harvest
        self.stacks = 1

    def makeRuined(self):
        self.harvestable = False
        #a plant starts with 0 stack, if ruined, it has -1
        self.stacks = -1

    def removeAStack(self):
        self.stacks = 0
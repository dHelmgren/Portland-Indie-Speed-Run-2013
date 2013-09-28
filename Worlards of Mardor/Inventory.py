__author__ = 'Devin & Stan'

import Worker
import Livestock
import Crop
from Constants import *
##
#Inventory
#Description: This file holds all the relevant information about a player's inventory
#
#Variables:
#   blood - the amount of currency currently held by the
#   favor - the amount of favor the player holds with their deity
#   unitList[] - the units owned by the player
#   foodstuffs - the amount of food that the player can give to their livestock and workers
#   maxUnits - the number of plots that the user has right now
#

class Inventory(object):

    ##
    #__init__
    #Description: initialized the player's inventory
    #
    ##
    def __init__(self):
        self.blood = 300
        self.favor = 0.5
        self.foodstuffs = 10
        self.unitList = []
        self.unitList.append(Worker(GOBLIN))
        self.maxUnits = 6

    #this will need getter and setter methods for each variable



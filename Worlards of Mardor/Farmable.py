__author__ = 'Devin'

from Constants import *
import math


#unit stat lookup
#stats ordered as follows (turnout, time, cost, sellPrice, hardiness, consumption, stacks, maxStacks, output)
UNIT_STATS = []
UNIT_STATS.append((8, 2, 10, 15, 0, 0, 0, None, None))  #BLOODROOT
UNIT_STATS.append((6, 3, 20, 45, 0, 0, 0, None, None))  #SCREAMING_FUNGUS
UNIT_STATS.append((1, 6, 40, 90, 0, 0, 0, None, None))  #ORCWORT
UNIT_STATS.append((1, 2, 30, 5, 1, 1, 2, 80, None))  #PLAGUE_TOAD
UNIT_STATS.append((10, 5, 80, 70, 2, 4, 2, 8, None))  #DIRE_RAT
UNIT_STATS.append((4, 7, 100, 20, 2, 2, 0, 16, 0))  #GOBLIN

##
#Farmable
#Description: This file describes the basic functionality of a farmable object
#
#Variables:
#   turnout - the amount of foodstuffs added when this farmable is harvested
#   time - the number of turns required to have a mature farmable
#   cost - the cost to purchase this item from the store
#   sellPrice - the value of each foodstuff when sold
#   hardiness - the amount of attention needed to secure the farmable between turns
#   consumption - how much foodstuffs this unit needs per turn
#   stacks - represents the number of sub units
#   maxStacks - the maximum number of stacks allowed for this unit
#   output - the amount of work the unit provides each turn
#   clock - the number of turns left before the Farmable is harvestable/produces a new generation
##

class Farmable(object):

    ##
    #__init__
    #Description: initializes any object that is farmable
    ##
    def __init__(self, unitType):
        stats = UNIT_STATS[unitType]
        self.turnout = stats[0]
        self.time = stats[1]
        self.cost = stats[2]
        self.sellPrice = stats[3]
        self.hardiness = stats[4]
        self.consumption = stats[5]
        self.stacks = stats[6]
        self.maxStacks = stats[7]
        self.output = stats[8]
        self.clock = self.time
        self.type = unitType

    ##
    #updateStacks
    #Description: Grows the population of a stackable farm object
    #
    ##
    def updateStacks(self):
        #Update the size of the population
        self.stacks += 1
        #don't let it exceed the capacity
        if self.stacks > self.maxStacks:
            self.stacks = self.maxStacks

    ##
    #updateClock
    #Description: Updates the clock for the
    ##
    def updateClock(self):
        #decrease the number of turns until the object is "done"
        self.clock -= 1

    def removeAStack(self):
        self.stacks -= 1

    ##
    #printStats
    #Description: prints information about the farmable
    def printStats(self):
        print((self.clock, self.stacks, self.type))

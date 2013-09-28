__author__ = 'Devin'

from Constants import *


#unit stat lookup
#stats ordered as follows (turnout, time, cost, sellPrice, hardiness, consumption, stacks, maxStacks, output)
UNIT_STATS = []
UNIT_STATS.append((0, 0, 100, 0, 0, None, None, None, None))  #BLOODROOT
UNIT_STATS.append((0, 0, 200, 0, 0, None, None, None, None))  #SCREAMING_FUNGUS
UNIT_STATS.append((0, 0, 400, 0, 0, None, None, None, None))  #ORCWORT
UNIT_STATS.append((0, 0, 300, 0, 0, 0, 0, 0, None))  #PLAGUE_TOAD
UNIT_STATS.append((0, 0, 500, 0, 0, 0, 0, 0, None))  #DIRE_RAT
UNIT_STATS.append((0, 0, 600, 0, 0, 0, 0, 0, None))  #GOBLIN

##
#Farmable
#Description: This file describes the basic functionality of a farmable object
#
#Variables:
#   turnout - the amount of foodstuffs added when this crop is harvested
#   time - the number of turns required to have a mature crop
#   cost - the cost to purchase this item from the store
#   sellPrice - the value of each foodstuff when sold
#   hardiness - the amount of attention needed to secure the crop between turns
#   consumption - how much foodstuffs this unit needs per turn
#   stacks - represents the number of sub units
#   maxStacks - the maximum number of stacks allowed for this unit
#   output - the amount of work the unit provides each turn
#

class Farmable(object):

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

__author__ = 'Devin'

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
#

class Farmable(object):

    def __init__(self, tur, tim, cos, sel, har):
        self. turnout = tur
        self.time = tim
        self.cost = cos
        self.sellPrice = sel
        self.hardiness = har


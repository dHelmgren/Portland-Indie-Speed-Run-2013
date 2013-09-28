__author__ = 'Devin'

from Farmable import *

##
#Livestock
#Description: This file contains information and methods to define functionality of a Livestock object
#
#Variables:
#   consumption - how much foodstuffs this unit needs per turn
#   stacks - represents the number of sub units
#   maxStacks - the maximum number of stacks allowed for this unit

class Livestock(Farmable):

    def __init__(self, livestockKey):

        #retrieve livestock info for the livestockKey
        livestockKey = (0,0,0,0,0,0,0,0)
        #pull out the first five pieces for the basic key
        basicKey = (0,0,0,0,0)
        counter = 0
        for num in livestockKey:
            if counter < 5:
                basicKey[counter] = livestockKey[counter]
            counter += 1
        super(Livestock, self).__init__(livestockKey)
        self.consumption = livestockKey[5]
        self.stacks = livestockKey[6]
        self.maxStacks = livestockKey[7]


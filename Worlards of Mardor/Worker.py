__author__ = 'Devin'

from Farmable import *


##
#Worker
#Description: This file contains information and methods to define functionality of a Worker object
##

class Worker(Farmable):

    def __init__(self, unitType):
        #retrieve livestock info for the livestockKey

        super(Worker, self).__init__(unitType)

    ##
    #modifyWorkerNumber
    #Description: adjusts the number of workers at the beginning of the game
    #
    def modifyWorkerNumber(self):
        self.stacks = 3

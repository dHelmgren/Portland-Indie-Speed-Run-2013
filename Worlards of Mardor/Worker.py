__author__ = 'Devin'

import Farmable


##
#Worker
#Description: This file contains information and methods to define functionality of a Livestock object
#
#
#
#Variables:

#
#

class Worker(Farmable):

    def __init__(self, unitType):
        #retrieve livestock info for the livestockKey
        super(Worker, self).__init__(unitType)

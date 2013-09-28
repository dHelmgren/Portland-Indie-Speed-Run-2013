__author__ = 'Devin'

import Livestock


##
#Worker
#Description: This file contains information and methods to define functionality of a Livestock object
#
#
#
#Variables:
#   output - the amount of work that the unit can do on other crops
#
#

class Worker(Livestock):

    def __init__(self):
        #retrieve livestock info for the livestockKey
        workerKey = (0,0,0,0,0,0,0,0,0)
        #pull out the first five pieces for the basic key
        basicKey = (0,0,0,0,0,0,0,0)
        counter = 0
        for num in workerKey:
            if counter < 5:
                basicKey[counter] = workerKey[counter]
            counter += 1
        super(Worker, self).__init__(workerKey)
        self.output = workerKey[8]
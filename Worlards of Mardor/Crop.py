__author__ = 'Devin'

from Farmable import *

##
#Crop
#Description: Contains methods and variables that define the operation of a crop
#
##

class Crop(Farmable):

    def __init__(self, unitType):
        super(Crop, self).__init__(unitType)
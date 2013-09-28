__author__ = 'Devin'

from Farmable import *

##
#Crop
#Description: Contains methods and variables that define the operation of a crop
#
#Variables:
#

class Crop(Farmable):

    def __init__(self, cropKey):
        #use the dictionary to fetch the tuple which represents the stats of that crop
        cropKey = (0,0,0,0,0)

        super(Crop, self).__init__(cropKey)
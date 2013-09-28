__author__ = 'Devin'

from Farmable import *

##
#Livestock
#Description: This file contains information and methods to define functionality of a Livestock object
#
##

class Livestock(Farmable):

    def __init__(self, unitType):

        super(Livestock, self).__init__(unitType)
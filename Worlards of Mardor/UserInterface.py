__author__ = 'Devin'

import pygame, os, sys, time
from pygame.locals import *

##
#UserInterface
#Description: class that handles all drawing and key presses, and translates everything to something
# that can more easily be understood by a programmer.
#
#Variables:
#   inputSize - An (x,y) tuple expressing the size of the aNTiCS window in pixels.((int,int))
##

class UserInterface(object):
    ##
    #__init__
    #Description: Creates a new UserInterface
    #
    #Parameters:
    #   inputSize - the size of the window to be created, in pixels.(int)
    ##
    def __init__(self, inputSize):
        self.screen = pygame.display.set_mode(inputSize)
        pygame.display.set_caption("Demo")
__author__ = 'Devin'

##
#Constants
#Description: a list for all of the constants that are used in the game
##

#Event Screen
EVENT = -10

#Arrows
LEFT = -9
RIGHT = -8

# Button Constants
ENDBUTTON = -7
BUTTON1 = -6
BUTTON2 = -5
BUTTON3 = -4

#Screen States
SHOP = -3
PLOTS = -2
DWELLINGS = -1

#Crop Types
BLOODROOT = 0
SCREAMING_FUNGUS = 1
ORCWORT = 2

#Livestock Types
PLAGUE_TOAD = 3
DIRE_RAT = 4

#Worker Types
GOBLIN = 5

#Unit Stat Constants

TURNOUT = 0
TIME = 1
COST = 2
SELL_PRICE = 3

#LOSS OF FOOD
WITHER = ["Your crop is left too long and withers in the fields.",
          " Your pathetic attempts at saving the last of it",
          "yields barely enough to feed you, ",
          "let alone the peasants."]

GEL_CUBE = ["A gelatinous cube has been found in the Bloodroot Silo!",
           "Thankfully, the creature gorged itself before eating",
           "all your stores, so it was simple enough to",
           " melt him into lantern oil."]

SMALL = ["A strange, small creature seems to have found its way into",
         " your food storage."]

#LOSS OF LIVESTOCK
BARBARIANS = ["Marauding barbarians come through and break your",
              "Toad pen! After your slaves come out of hiding,",
              "they count a handful missing. What a shame."]

RAT_ESCAPE = ["The Dire-Rats have escaped their cages! ",
              "However, they did not flee but gorged ",
              "themselves on Plague Toads. You do not ",
              "lose any Rats, but your Toad population drops."]

FIRE_WRYM = ["A young Fire Wyrm burns down part of your keep ",
             "and demands tithe in the form of food. ",
             "Rather than pay for the repairs, you offer him ",
             "a small tithe of your rats and he leaves."]

#LOSS OF SLAVES
EMPTY_LANDS = ["The empty fields of the past few months ",
               "were simply too much. Some of your slaves die."]

DO_GOODERS = ["A band of marauding do-gooders has freed some ",
              "of your slaves! This cannot be tolerated. ",
              "It is time to raise taxes again."]

FEED_FRENZY = ["One of your goblins injured himself in ",
               "the fields and started a feeding frenzy! ",
               "Several slaves were killed in the fray."]

#LOSS OF BLOOD
VAMPIRES = ["Vampires have raided the Blood Bank! ",
            "The wretched creatures swallowed enough ",
            "blood to burst a score of plague toads, ",
            "but it slowed them down. The Dire-Rats ",
            "will eat well tonight."]

INJURY = ["You are injured during a conquest against ",
          "the local church and must be given a ",
          "transfusion from your Blood Bank."]

LOCAL_TAXES = ["The King's Tax Collector arrived. ",
               "You resist your overwhelming desire to ",
               "kill him as he siphons from your bank. ",
               "You conduct a horrid ritual that night to ",
               "ensure his... safe... return home."]


import random

class Player:
    def __init__(self, name):
        self.id = name
        self.balance = 0    #Current balance
        self.position = 0   #Current position
        self.jail = false   #Jailed status
        self.property = []  #Property owned
        self.cards = []     #Cards owned
        self.bankrupt = false   #Bankruptcy status
        self.ai = "something will go here"

    def move(self, position):
        previous = self.position
        a = random.randint(1, 6)
        b = random.randint(1, 6)
        #Maybe some conditionals based on doubles and such
        roll = a + b
        self.position += roll
        print(self.id + "rolled " + roll + " moving from " + previous + " to " + self.position + "\n")

import random


class Player:
    def __init__(self, name):
        self.id = name
        self.money = 0    # Current amount of money
        self.position = 0   # Current position
        self.jail = false   # Jailed status
        self.property = []  # Property owned
        self.cards = []     # Cards owned
        self.bankrupt = false   # Bankruptcy status
        self.spendingAI = 0.5    # This can determine how they spend their money [0 - 1]
        self.ai = "something will go here"

    def move(self, position):
        previous = position
        a = random.randint(1, 6)
        b = random.randint(1, 6)
        # Maybe some conditionals based on doubles and such
        if self.jail:    # If player is in jail, attempt to get out
            self.get_out_of_jail()
        else:
            roll = a + b
            self.position += roll
            print(self.id + "rolled " + roll + " moving from " + previous + " to " + self.position + "\n")
            return roll

    def spend_money(self, amount):
        spent = False
        if self.money < amount:
            print("Not enough money!")
        else:
            self.money = self.money - amount
            spent = True
        return spent

    def go_to_jail(self):
        self.position = 10
        self.jail = True

    def get_out_of_jail(self):
        # If player AI is is passive/is try to accumulate money, more likely
        # to try to roll doubles. If more aggro, more likely to pay bail
        # If player has the money for bail, will roll rng for paying bail
        # If player does not have the money, always try to roll doubles
        if self.money >= 50:
            if self.spendingAI < 0.3:   # Between 0.0 and 0.2 inclusive
                spend_rng = random.randint(0, 60)   # Not likely to pay bail
            elif self.spendingAI > 0.2 & self.spendingAI < 0.6:     # Between 0.3 and 0.5 inclusive
                spend_rng = random.randint(10, 70)
            elif self.spendingAI > 0.5 & self.spendingAI < 0.9:     # Between 0.6 and 0.8 inclusive
                spend_rng = random.randint(30, 80)
            else:   # Between 0.9 and 1.0 inclusive
                spend_rng = random.randint(45, 100)     # Nearly guaranteed to pay bail
            if spend_rng >= 50:
                if self.spend_money(50):    # If money successfully spent
                    self.jail = False
                    a = random.randint(1, 6)
                    b = random.randint(1, 6)
                    roll = a + b
                    self.position += roll
                    print(self.id + "rolled " + roll + " moving from " + previous + " to " + self.position + "\n")
            else:
                a = random.randint(1, 6)
                b = random.randint(1, 6)
                if a == b:
                    print("Rolled doubles! Get out of jail!")
                    roll = a + b
                    self.position += roll
                    print(self.id + "rolled " + roll + " moving from " + previous + " to " + self.position + "\n")
                else:
                    print("Failed to roll doubles, too bad!")
        else:
            a = random.randint(1, 6)
            b = random.randint(1, 6)
            if a == b:
                print("Rolled doubles! Get out of jail!")
                roll = a + b
                self.position += roll
                print(self.id + "rolled " + roll + " moving from " + previous + " to " + self.position + "\n")
            else:
                print("Failed to roll doubles, too bad!")
        return

    def position_action(self, board):
        # Based on the position the player has landed on, take certain actions
        position = board[self.position]
        # Not complete
        return
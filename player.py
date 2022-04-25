import random
import board as board


class Player:
    def __init__(self, name, spendingAI):
        self.id = name     # Identifier
        self.money = 0    # Current amount of money
        self.position = 0   # Current position
        self.jail = False   # Jailed status
        self.property = []  # Property owned
        self.cards = []     # Cards the player currently has
        self.railroads = 0     # Railroads owned
        self.bankrupt = False   # Bankruptcy status
        self.spendingAI = spendingAI    # This can determine how they spend their money [ranging from 0.0 to 1.0]
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
            self.position = self.position % 40
            print(self.id, "rolled ", roll, " moving from ", previous, " to ", self.position, "\n")
            return roll

    def spend_money(self, amount):
        spent = False
        if self.money < amount:
            # Add options to allow the player to not get bankrupt
            print("Not enough money!")
        else:
            self.money = self.money - amount
            spent = True
        return spent

    def add_money(self, amount):
        self.money = self.money + amount
        return self.money

    def go_to_jail(self):
        print("Go to jail!")
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
            elif self.spendingAI > 0.2 and self.spendingAI < 0.6:     # Between 0.3 and 0.5 inclusive
                spend_rng = random.randint(10, 70)
            elif self.spendingAI > 0.5 and self.spendingAI < 0.9:     # Between 0.6 and 0.8 inclusive
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
                    print(self.id, "rolled ", roll, " to ", self.position, "\n")
            else:
                a = random.randint(1, 6)
                b = random.randint(1, 6)
                if a == b:
                    print("Rolled doubles! Get out of jail!")
                    self.jail = False
                    roll = a + b
                    self.position += roll
                    print(self.id, "rolled ", roll, " to ", self.position, "\n")
                else:
                    print("Failed to roll doubles, too bad!")
        else:
            a = random.randint(1, 6)
            b = random.randint(1, 6)
            if a == b:
                print("Rolled doubles! Get out of jail!")
                self.jail = False
                roll = a + b
                self.position += roll
                print(self.id, "rolled ", roll, " to ", self.position, "\n")
            else:
                print("Failed to roll doubles, too bad!")
        return

    def position_action(self, board):
        # Based on the position the player has landed on, take certain actions
        position = board[self.position]
        if position.name == "Go to Jail":
            self.go_to_jail()
        elif position.name == "Income Tax":
            # Add option to spend 10% of net worth if we want
            self.spend_money(200)
        elif position.name == "Luxury Tax":
            self.spend_money(75)
            print("Taxed $75!")
        # Include options to buy property and actions to take if landing on owned property
        # Not complete
        return

    def bankrupt_action(self):
        # Include last ditch effort to allow player to not get bankrupt,
        # Like selling property back to the bank/other players
        # Game over for the player, take them out of the game
        # Take back all cards owned by that player and give it to the bank
        self.bankrupt = True

    def rent(self, property):
        # Do not call this function if the current owner is the bank
        # Determine how much money the player needs to pay when landing
        # on another person's property
        # Possibly add options if a player owns all of the color group?
        if property.type == "Railroad":
            railroads_owned = property.cur_owner.railroads
            amount_owed = 25 * railroads_owned
        else:
            i = property.total_houses
            amount_owed = property.rent_prices[i]
        self.spend_money(amount_owed)
        property.cur_owner.add_money(amount_owed)
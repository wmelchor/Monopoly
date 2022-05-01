from asyncio.windows_events import NULL
import random
from time import sleep
from unicodedata import name
import board as board
import playstyle as playstyle


class Player:
    def __init__(self, name, spendingAI):
        self.name = name     # Identifier
        self.money = 1500   # Current amount of money
        self.position = 0   # Current position
        self.jail = False   # Jailed status
        self.property = []  # Property owned
        self.cards = []     # Cards the player currently has
        self.railroads = 0     # Railroads owned
        self.bankrupt = False   # Bankruptcy status
        self.spendingAI = spendingAI    # This can determine how they spend their money [ranging from 0.0 to 1.0]
        self.playstyle = playstyle.Playstyle(spendingAI)
        self.ai = "something will go here"

    def move(self, position, board):
        if self.bankrupt:
            return

        previous = position
        a = random.randint(1, 6)
        b = random.randint(1, 6)
        # Maybe some conditionals based on doubles and such
        if self.jail:    # If player is in jail, attempt to get out
            self.get_out_of_jail(board)
        else:
            roll = a + b
            self.position += roll
            self.position = self.position % 40
            print(self.name, "(" ,self.money , ")", "rolled ", roll, " moving from ", board[previous].name, " to ", board[self.position].name)
            # if passed go collect 200
            if previous > self.position:
                self.add_money(200)
                print("Passed Go Collect $200!")
            return roll

    def spend_money(self, amount):
        spent = False
        if self.money < amount:
            # Add options to allow the player to not get bankrupt
            print("Not enough money!")
            self.bankrupt_action()
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

    def get_out_of_jail(self, board):
        # add get out of jail card implementation ##########################
        # If player AI is is passive/is try to accumulate money, more likely
        # to try to roll doubles. If more aggro, more likely to pay bail
        # If player has the money for bail, will roll rng for paying bail
        # If player does not have the money, always try to roll doubles
        previous = self.position
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
                    print(self.name, "rolled ", roll, " to ", self.position, "\n")
            else:
                a = random.randint(1, 6)
                b = random.randint(1, 6)
                if a == b:
                    print("Rolled doubles! Get out of jail!")
                    self.jail = False
                    roll = a + b
                    self.position += roll
                    print(self.name, "rolled ", roll, " moving from ", board[previous].name, " to ", board[self.position].name)
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
                print(self.name, "rolled ", roll, " to ", self.position, "\n")
            else:
                print("Failed to roll doubles, too bad!")
        return

    def bankrupt_action(self):
        # Include last ditch effort to allow player to not get bankrupt,
        # Like selling property back to the bank/other players
        # Game over for the player, take them out of the game
        # Take back all cards owned by that player and give it to the bank
        print(self.name + " went bankrupt!!!!!!!!!!!!!")
        self.bankrupt = True

    def rent(self, property, board, players):
        # Do not call this function if the current owner is the bank
        # Determine how much money the player needs to pay when landing
        # on another person's property
        # Possibly add options if a player owns all of the color group?
        if property.type == "Utility":
            # make amount_owed a function of dice roll
            amount_owed = 100
        
        elif property.type == "Railroad":
            railroads_owned = 0
            for x in board:
                if x.type == "Railroad" and x.cur_owner == property.cur_owner:
                    railroads_owned = railroads_owned + 1

            amount_owed = 25 * railroads_owned
        else:
            i = property.total_houses
            if property.rent_prices[i] == NULL:
                return
            amount_owed = property.rent_prices[i]
        if not self.spend_money(50 * amount_owed):
            return
      
        for player in players:
            if player.name == property.cur_owner:
                player.add_money(amount_owed)
                print(self.name , " payed ", player.name, amount_owed)


    def defaultDecision(self, board):
        # Uses spendingAI and current board info to decide on a purchase
        # spendingAI < 0.5 passive
        # spendingAI > 0.5 aggressive
        # spendingAI = 0.5 neutral

        # (spendingAI - 0.5)/10 + ownedbyme/(totalcolor - ownedbyothers)
        

        cardsofcolor = []
        ownedByMe = 0
        ownedByOther = 0 
        
        for x in board:
            if (x.type == board[self.position].type):
                cardsofcolor.append(x)
                if (x.cur_owner == self.name):
                    ownedByMe +=1
                elif(x.cur_owner != "Bank"):
                    ownedByOther += 1
        return random.random() > ((4 * (self.spendingAI - 0.5) / 10)) + (ownedByMe/(len(cardsofcolor) - ownedByOther))

    def buy_position(self, position, board):
        # Buy position and adjust player values
        self.spend_money(board[position].price)
        self.property.append(board[position].name)
        # print(self.property , "property array")
        # sleep(5)
        board[position].cur_owner = self.name

    def position_action(self, board, players):
        # Based on the position the player has landed on, take certain actions
        if self.bankrupt:
            return

        position = self.position

        
        #test bankrupt

        if self.money <= 0:
            self.bankrupt_action()

        #    
        elif board[position].name == "Go":
            print("Back at Go")
        elif board[position].name == "Free Parking":
            print("Free Parking")
        elif board[position].name == "Go to Jail":
            self.go_to_jail()
        elif board[position].name == "Income Tax":
            # Add option to spend 10% of net worth if we want
            self.spend_money(200)
            print("Taxed $200!")
        elif board[position].name == "Luxury Tax":
            self.spend_money(75)
            print("Taxed $75!")
        elif board[position].name == "Chance":
            # incomplete
            print("Chance??")
            i = 0
            random.shuffle(globals()["board"].chance_cards)
            self.chance_action(i, board, players)
        elif board[position].name == "Community Chest":
             # incomplete
            print("Community Chest")
        elif board[position].name == "Jail":
            if self.jail:
                print("Still in Jail")
            else:
                print("Visiting Jail")    
        else:
            if board[position].cur_owner != "Bank" and board[position].cur_owner != self.name:
                self.rent(board[position], board, players)
            elif board[position].cur_owner == "Bank":
                if self.defaultDecision(board):
                    self.buy_position(position, board)
        return

    def chance_action(self, index, positions, players):     # index for card deck, board, players
        if board.chance_cards[index] == "Advance to Boardwalk":
            print("Drew chance card! Advance to Boardwalk")
            self.position = 39
        elif board.chance_cards[index] == "Advance to Go (Collect $200)":
            print("Drew chance card! Advance to Go (Collect $200)")
            self.position = 0
            self.add_money(200)
        elif board.chance_cards[index] == "Advance to Illinois Avenue":
            print("Drew chance card! Advance to Illinois Avenue")
            if self.position > 24:
                self.add_money(200)
            self.position = 24
        elif board.chance_cards[index] == "Advance to St. Charles Place":
            print("Drew chance card! Advance to St. Charles Place")
            if self.position > 11:
                self.add_money(200)
            self.position = 11
        elif board.chance_cards[index] == "Advance to the nearest Railroad":
            print("Drew chance card! Advance to the nearest Railroad")
            if self.position < 5:
                self.position = 5
            elif 15 > self.position > 5:
                self.position = 15
            elif 25 > self.position > 15:
                self.position = 25
            elif 35 > self.position > 25:
                self.position = 35
            else:
                self.position = 5
        elif board.chance_cards[index] == "Make general repairs on all your property":
            print("Drew chance card! Make general repairs on all your property")
            count = 0
            for positions in positions:
                if positions.cur_owner == self.name:
                    count = count + positions.total_houses
            total_pay = count * 25
            self.spend_money(total_pay)
        elif board.chance_cards[index] == "Advance token to nearest Utility":
            print("Drew chance card! Advance token to nearest Utility")
            if self.position < 12 or self.position > 28:
                self.position = 12
            else:
                self.position = 28
        elif board.chance_cards[index] == "Bank pays you dividend of $50":
            print("Drew chance card! Bank pays you dividend of $50")
            self.add_money(50)
        elif board.chance_cards[index] == "Get Out of Jail Free":
            print("Drew chance card! Get Out of Jail Free")
            self.cards.append("Get Out of Jail Free")
        elif board.chance_cards[index] == "Go Back 3 Spaces":
            print("Drew chance card! Go Back 3 Spaces")
            if self.position == 2:
                self.position = 40
            elif self.position == 1:
                self.position = 39
            elif self.position == 0:
                self.position = 38
            else:
                self.position = self.position - 3
        elif board.chance_cards[index] == "Go to Jail":
            print("Drew chance card! Go to Jail")
            self.go_to_jail()
        elif board.chance_cards[index] == "Speeding fine":
            print("Drew chance card! Speeding fine")
            self.spend_money(15)
        elif board.chance_cards[index] == "Take a trip to Reading Railroad":
            print("Drew chance card! Take a trip to Reading Railroad")
            if self.position > 5:
                self.add_money(200)
            self.position = 5
        elif board.chance_cards[index] == "You have been elected Chairman of the Board":
            print("Drew chance card! You have been elected Chairman of the Board. Pay each player $50")
            total = 50 * 4
            self.spend_money(total)
            for player in players:
                player.add_money(50)
        elif board.chance_cards[index] == "Your building loan matures. Collect $150":
            print("Drew chance card! Your building loan matures. Collect $150")
            self.add_money(150)
        else:
            print("e")

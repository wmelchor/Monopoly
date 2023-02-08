
import random
from time import sleep
from unicodedata import name
import board as board
import playstyle as playstyle
NULL = 0

class Player:
    def __init__(self, name, spendingAI):
        self.name = name     # Identifier
        self.money = 1500   # Current amount of money
        self.position = 0   # Current position
        self.jail = False   # Jailed status
        self.property = []  # Property owned
        self.cards = []     # Cards the player currently has
        self.chance_times = 0   # Times player drew a chance
        self.community_times = 0  # Times player drew a comm card
        self.railroads = 0     # Railroads owned
        self.bankrupt = False   # Bankruptcy status
        self.spendingAI = spendingAI    # This can determine how they spend their money [ranging from 0.0 to 1.0]
        self.playstyle = playstyle.Playstyle(spendingAI)
        self.ai = "something will go here"
        self.placement = 1  # finishing placement

    def move(self, position, board, globalvals):
        if self.bankrupt:
            return

        previous = position
        a = random.randint(1, 6)
        b = random.randint(1, 6)
        # Maybe some conditionals based on doubles and such
        if self.jail:    # If player is in jail, attempt to get out
            self.get_out_of_jail(board, globalvals)
        else:
            roll = a + b
            self.position += roll
            self.position = self.position % 40
            #print(self.name, "(" ,self.money , ")", "rolled ", roll, " moving from ", board[previous].name, " to ", board[self.position].name)
            # if passed go collect 200
            if previous > self.position:
                self.add_money(200, globalvals)
                #print("Passed Go Collect $200!")
            return roll

    def spend_money(self, amount, globalvals):
        spent = False
        if globalvals[3]:
            if self.money < amount:
                # Add options to allow the player to not get bankrupt
            # print("Not enough money!")
                self.bankrupt_action(globalvals)
            else:
                self.money = self.money - amount
                spent = True
        else:

            if self.money < amount:
                # Add options to allow the player to not get bankrupt
            # print("Not enough money!")
                self.bankrupt_action(globalvals)
            else:
                globalvals[2] += amount
                self.money = self.money - amount
                spent = True
        return spent

    def add_money(self, amount, globalvals):
        # 20580
        if globalvals[3]:
             self.money = self.money + amount
        else:
            if globalvals[2] - amount <= 0:
                return 
            else:
                self.money = self.money + amount
                globalvals[2] -= amount
        return self.money

    def go_to_jail(self):
       # print("Go to jail!")
        self.position = 10
        self.jail = True

    def get_out_of_jail(self, board, globalvals):
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
                if self.spend_money(50, globalvals):    # If money successfully spent
                    self.jail = False
                    a = random.randint(1, 6)
                    b = random.randint(1, 6)
                    roll = a + b
                    self.position += roll
                    #print(self.name, "rolled ", roll, " to ", self.position, "\n")
            else:
                a = random.randint(1, 6)
                b = random.randint(1, 6)
                if a == b:
                    #print("Rolled doubles! Get out of jail!")
                    self.jail = False
                    roll = a + b
                    self.position += roll
                    #print(self.name, "rolled ", roll, " moving from ", board[previous].name, " to ", board[self.position].name)
                else:
                    #print("Failed to roll doubles, too bad!")
                    pass
        else:
            a = random.randint(1, 6)
            b = random.randint(1, 6)
            if a == b:
                #print("Rolled doubles! Get out of jail!")
                self.jail = False
                roll = a + b
                self.position += roll
                #print(self.name, "rolled ", roll, " to ", self.position, "\n")
            else:
                #print("Failed to roll doubles, too bad!")
                pass
        return

    def bankrupt_action(self, globalvals):
        # Include last ditch effort to allow player to not get bankrupt,
        # Like selling property back to the bank/other players
        # Game over for the player, take them out of the game
        # Take back all cards owned by that player and give it to the bank
        

        if self.bankrupt:
            return

        self.placement = globalvals[4]
        globalvals[4] -= 1

        
        #print(self.name + " went bankrupt!!!!!!!!!!!!!")
        #print(self.name + " placed" , self.placement)

        self.bankrupt = True
        globalvals[2] += self.money
        for card in self.property:
            card.cur_owner = "Bank"
            if card.total_houses == 5:
                globalvals[0] += 4
                globalvals[1] += 1
            else:    
                globalvals[0] += card.total_houses 
            card.total_houses = 0
        return 

    def rent(self, property, board, players, globalvals):
        # Do not call this function if the current owner is the bank
        # Determine how much money the player needs to pay when landing
        # on another person's property
        # Possibly add options if a player owns all of the color group?
        globalvals[3] = True
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
                globalvals[3] = False
                return
            amount_owed = property.rent_prices[i]
        if not self.spend_money(amount_owed, globalvals):
            globalvals[3] = False
            return
      
        for player in players:
            if player.name == property.cur_owner:
                player.add_money(amount_owed, globalvals)
                globalvals[3] = False
                #print(self.name , " payed ", player.name, amount_owed)


    def defaultDecision(self, board):
        # Uses spendingAI and current board info to decide on a purchase
        # spendingAI < 0.5 passive
        # spendingAI > 0.5 aggressive
        # spendingAI = 0.5 neutral

        # (spendingAI - 0.5)/10 + ownedbyme/(totalcolor - ownedbyothers)
        

        cardsofcolor = []
        ownedByMe = 0
        ownedByOther = 0 
        ownedByBank = 0 
        
        for x in board:
            if (x.type == board[self.position].type):
                cardsofcolor.append(x)
                if (x.cur_owner == self.name):
                    ownedByMe +=1
                elif(x.cur_owner != "Bank"):
                    ownedByOther += 1
                else:
                    ownedByBank +=1

        #(self.spendingAI - 0.5) / 10)) +
        probability = ( ((self.spendingAI - 0.5) / 10)) + (ownedByBank/10 + ownedByMe - ownedByOther)/(len(cardsofcolor))
        #print(probability , "<--------- buy probability")
        return random.random() < probability

    def buy_position(self, position, board, globalvals):
        # Buy position and adjust player values
        self.spend_money(board[position].price, globalvals)
        self.property.append(board[position])
        #for props in self.property:
                #print(self.name, "property list: ", props.name, props.type)
        # print(self.property , "property array")
        # sleep(5)
        board[position].cur_owner = self.name

    def buy_houses(self, board, color, globalvals):
        passive = 800
        aggressive = 400
        #globalhouses = globals[0]
        #globalhotels = globals[1]
    
        for card in self.property:
            if card.type == color and card.total_houses < 5:
                if self.spend_money(card.house_price, globalvals):
                    if card.total_houses == 4 and globalvals[1] > 0:
                        globalvals[1] -= 1
                        globalvals[0] += 4
                        card.total_houses += 1
                        #print("--------------------------------------------------------")

                        #print(self.name , "Bought a hotel on", card.name)
                        #print("--------------------------------------------------------")
                    elif(globalvals[0] > 0):
                        card.total_houses += 1
                        globalvals[0] -= 1
                        #print("--------------------------------------------------------")
                        #print(self.name , "Bought a house on", card.name)
                        #print("--------------------------------------------------------")

    def check_colors(self, globalvals):
        DarkBlue = 2
        Green = 3
        Yellow = 3
        Red = 3
        Orange = 3
        Pink = 3
        LightBlue = 3
        Brown = 2

        cardDarkBlue = 0
        cardGreen = 0
        cardYellow = 0
        cardRed = 0
        cardOrange = 0
        cardPink = 0
        cardLightBlue = 0
        cardBrown = 0

        for card in self.property:
            if card.type == "Dark Blue":
                cardDarkBlue += 1
            elif card.type == "Green":
                cardGreen += 1
            elif card.type == "Yellow":
                cardYellow += 1
            elif card.type == "Red":
                cardRed += 1
            elif card.type == "Orange":
                cardOrange += 1
            elif card.type == "Pink":
                cardPink += 1
            elif card.type == "Light Blue":
                cardLightBlue += 1
            elif card.type == "Brown":
                cardBrown += 1
        if cardDarkBlue == DarkBlue:
            self.buy_houses(board, "Dark Blue", globalvals)
        elif cardGreen == Green:
            self.buy_houses(board, "Green", globalvals)
        elif cardYellow == Yellow:
            self.buy_houses(board, "Yellow", globalvals)
        elif cardRed == Red:
            self.buy_houses(board, "Red", globalvals)
        elif cardOrange == Orange:
            self.buy_houses(board, "Orange", globalvals)
        elif cardPink == Pink:
            self.buy_houses(board, "Pink", globalvals)
        elif cardLightBlue == LightBlue:
            self.buy_houses(board, "Light Blue", globalvals)
        elif cardBrown == Brown:
            self.buy_houses(board, "Brown", globalvals)

    def position_action(self, board, players, globalvals):
        # Based on the position the player has landed on, take certain actions
        if self.bankrupt:
            return

        position = self.position
        self.check_colors(globalvals)

        if self.money <= 0:
            self.bankrupt_action(globalvals)

        #    
        elif board[position].name == "Go":
            #print("Back at Go")
            pass
        elif board[position].name == "Free Parking":
            #print("Free Parking")
            pass
        elif board[position].name == "Go to Jail":
            self.go_to_jail()
        elif board[position].name == "Income Tax":
            # Add option to spend 10% of net worth if we want
            self.spend_money(200, globalvals)
            #print("Taxed $200!")
        elif board[position].name == "Luxury Tax":
            self.spend_money(75, globalvals)
            #print("Taxed $75!")
        elif board[position].name == "Chance":
            # incomplete
            #print("Chance??")
            i = 0
            random.shuffle(globals()["board"].chance_cards)
            self.chance_action(i, board, players, globalvals)
            self.chance_times += 1
        elif board[position].name == "Community Chest":
            # incomplete
            #print("Community Chest")
            i = 0
            random.shuffle(globals()["board"].community_cards)
            self.community_action(i, board, players, globalvals)
            self.community_times += 1
        elif board[position].name == "Jail":
            pass    
        else:
            if board[position].cur_owner != "Bank" and board[position].cur_owner != self.name:
                self.rent(board[position], board, players, globalvals)
            elif board[position].cur_owner == "Bank":
                if self.defaultDecision(board):
                    self.buy_position(position, board, globalvals)
        return

    def chance_action(self, index, positions, players, globalvals):     # index for card deck, board, players
        if board.chance_cards[index] == "Advance to Boardwalk":
            #print("Drew chance card! Advance to Boardwalk")
            self.position = 39
        elif board.chance_cards[index] == "Advance to Go (Collect $200)":
            #print("Drew chance card! Advance to Go (Collect $200)")
            self.position = 0
            self.add_money(200, globalvals)
        elif board.chance_cards[index] == "Advance to Illinois Avenue":
            #print("Drew chance card! Advance to Illinois Avenue")
            if self.position > 24:
                self.add_money(200, globalvals)
            self.position = 24
        elif board.chance_cards[index] == "Advance to St. Charles Place":
            #print("Drew chance card! Advance to St. Charles Place")
            if self.position > 11:
                self.add_money(200, globalvals)
            self.position = 11
        elif board.chance_cards[index] == "Advance to the nearest Railroad":
            #print("Drew chance card! Advance to the nearest Railroad")
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
           
            if positions[self.position].cur_owner != "Bank" and positions[self.position].cur_owner != self.name:
                self.rent(positions[self.position], positions, players, globalvals)
            elif positions[self.position].cur_owner == "Bank":
               if self.defaultDecision(positions):
                    self.buy_position(self.position, positions, globalvals)    

        elif board.chance_cards[index] == "Make general repairs on all your property":
            #print("Drew chance card! Make general repairs on all your property")
            count = 0
            for positions in positions:
                if positions.cur_owner == self.name:
                    count = count + positions.total_houses
            total_pay = count * 25
            self.spend_money(total_pay, globalvals)
        elif board.chance_cards[index] == "Advance token to nearest Utility":
            #print("Drew chance card! Advance token to nearest Utility")
            if self.position < 12 or self.position > 28:
                self.position = 12
            else:
                self.position = 28
        elif board.chance_cards[index] == "Bank pays you dividend of $50":
            #print("Drew chance card! Bank pays you dividend of $50")
            self.add_money(50, globalvals)
        elif board.chance_cards[index] == "Get Out of Jail Free":
           # print("Drew chance card! Get Out of Jail Free")
            self.cards.append("Get Out of Jail Free")
        elif board.chance_cards[index] == "Go Back 3 Spaces":
            #print("Drew chance card! Go Back 3 Spaces")
            if self.position == 2:
                self.position = 40
            elif self.position == 1:
                self.position = 39
            elif self.position == 0:
                self.position = 38
            else:
                self.position = self.position - 3
        elif board.chance_cards[index] == "Go to Jail":
            #print("Drew chance card! Go to Jail")
            self.go_to_jail()
        elif board.chance_cards[index] == "Speeding fine":
            #print("Drew chance card! Speeding fine")
            self.spend_money(15, globalvals)
        elif board.chance_cards[index] == "Take a trip to Reading Railroad":
           # print("Drew chance card! Take a trip to Reading Railroad")
            if self.position > 5:
                self.add_money(200, globalvals)
            self.position = 5
        elif board.chance_cards[index] == "You have been elected Chairman of the Board":
           # print("Drew chance card! You have been elected Chairman of the Board. Pay each player $50")
            total = 50 * 4
            self.spend_money(total, globalvals)
            for player in players:
                player.add_money(50, globalvals)
        elif board.chance_cards[index] == "Your building loan matures. Collect $150":
           # print("Drew chance card! Your building loan matures. Collect $150")
            self.add_money(150, globalvals)
        else:
            print("e")

    def community_action(self, index, positions, players, globalvals):     # index for card deck, board, players
        if board.community_cards[index] == "Life Insurance Matures":
           # print("Drew community card! Life Insurance Matures")
            self.add_money(100, globalvals)
        elif board.community_cards[index] == "Advance to Go (Collect $200)":
           # print("Drew community card! Advance to Go (Collect $200)")
            self.position = 0
            self.add_money(200, globalvals)
        elif board.community_cards[index] == "You have won second prize in a beauty contest":
           # print("Drew community card! You have won second prize in a beauty contest")
            self.add_money(10, globalvals)
        elif board.community_cards[index] == "Bank Error In Your Favor":
           # print("Drew community card! Bank Error In Your Favor")
            self.add_money(200, globalvals)
        elif board.community_cards[index] == "From Sale of Stock You Get $45":
           # print("Drew community card! From Sale of Stock You Get $45")
            self.add_money(45, globalvals)
        elif board.community_cards[index] == "Income Tax Refund":
            #print("Drew community card! Income Tax Refund")
            self.add_money(20, globalvals)
        elif board.community_cards[index] == "Receive for Services $25":
           # print("Drew community card! Receive for Services $25")
            self.add_money(25, globalvals)
        elif board.community_cards[index] == "You Inherit $100":
           # print("Drew community card! You Inherit $100")
            self.add_money(100, globalvals)
        elif board.community_cards[index] == "Get Out of Jail Free":
            #print("Drew community card! Get Out of Jail Free")
            self.cards.append("Get Out of Jail Free")
        elif board.community_cards[index] == "Xmas Fund Matures":
           # print("Drew community card! Xmas Fund Matures")
            self.add_money(100, globalvals)
        elif board.community_cards[index] == "Go to Jail":
           # print("Drew community card! Go to Jail")
            self.go_to_jail()
        elif board.community_cards[index] == "Grand Opera Opening":
            #print("Drew community card! Grand Opera Opening")
            total = 50 * 4
            self.add_money(total, globalvals)
            for player in players:
                player.spend_money(50, globalvals)
        elif board.community_cards[index] == "Doctor's Fee":
            #print("Drew community card! Doctor's Fee")
            self.spend_money(50, globalvals)
        elif board.community_cards[index] == "Pay Hospital":
           # print("Drew community card! Pay Hospital $100")
            self.spend_money(100, globalvals)
        elif board.community_cards[index] == "Pay School Tax of $150":
           # print("Drew community card! Pay School Tax of $150")
            self.spend_money(150, globalvals)
        elif board.community_cards[index] == "You are Assessed for Street Repairs":
            count = 0
            for positions in positions:
                if positions.cur_owner == self.name:
                    count = count + positions.total_houses
            total_pay = count * 50
            self.spend_money(total_pay, globalvals)
        else:
            print("e")

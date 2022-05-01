import board as board
import player as player
import playstyle as playstyle

board = board.cards_and_positions()

globalvals = [32, 12]

# Amount of times winner had the most of a color

color_data = [0, 0, 0, 0, 0, 0, 0]
color_names = ["Dark Blue", "Yellow", "Red", "Orange", "Pink", "Light Blue", "Brown"]   # For printing

sim_to_run = 50  # Amount of simulations to run
#P = player.Player("Name", spendingAI)
# spendingAI < 0.5 passive
# spendingAI > 0.5 aggressive
# spendingAI = 0.5 neutral

P1 = player.Player("Comp1", 1)
P2 = player.Player("Comp2", 0.5)
P3 = player.Player("Comp3", 0.3)
P4 = player.Player("Comp4", 0.7)
players = {P1, P2, P3, P4}


def reset_game(players):
    for player in players:
        player.position = 0
        player.money = 1500
        player.jail = False
        player.property = []
        player.cards = []
        player.railroads = 0
        player.bankrupt = False
    for card in board:
        card.cur_owner = "Bank"
        card.total_houses = 0
    global globalvals
    globalvals = [32, 12]


def game_over(players):
    remaining = len(players)
    for player in players:
        if player.bankrupt:
            remaining -= 1
    if remaining == 1:
        return True
    else:
        return False


def get_color_data(players):
    cardDarkBlue = 0
    cardGreen = 0
    cardYellow = 0
    cardRed = 0
    cardOrange = 0
    cardPink = 0
    cardLightBlue = 0
    cardBrown = 0
    for player in players:
        if not player.bankrupt:
            for card in player.property:
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
    if cardDarkBlue == 2:
        color_data[0] += 1
    if cardYellow == 3:
        color_data[1] += 1
    if cardRed == 3:
        color_data[2] += 1
    if cardOrange == 3:
        color_data[3] += 1
    if cardPink == 3:
        color_data[4] += 1
    if cardLightBlue == 3:
        color_data[5] += 1
    if cardBrown == 2:
        color_data[6] += 1



def winner_data(players):
    for player in players:
        if not player.bankrupt:
            # Add more data
            player_data = "Player name:", player.name, "AI Spending level:", player.spendingAI
            print(player_data, "Properties held:", "\n")
            for props in player.property:
                print(props.name, "(", props.type, ")")
                
            break


def main():
    for i in range(sim_to_run):
        while not game_over(players):   # Infinite loop as of now

            #go through player array calling move/position_action
            for person in players:
                person.move(person.position, board)
                person.position_action(board, players, globalvals)
                #print("global houses:", globalvals[0], "global hotels:", globalvals[1])
                if game_over(players):
                    print("---------------------------------------------GAME OVER!!!! SIMULATION ", (i+1), " IS OVER----------------------------------------------------------------")
                    winner_data(players)
                    get_color_data(players)
                    break
        #get_color_data(players)
        #winner_data(players)
        reset_game(players)
    max_value = max(color_data)
    list_of_max = [i for i, j in enumerate(color_data) if j == max_value]
    print("Color most frequently collected: ")
    for i in list_of_max:
        print(color_names[i])
    print(color_data)


if __name__ == "__main__":
    main()

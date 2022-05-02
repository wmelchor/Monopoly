import board as board
import player as player
import playstyle as playstyle
import matplotlib.pyplot as plt



board = board.cards_and_positions()

numwins = [0, 0, 0, 0]
globalvals = [32, 12, 20580, False]

# Amount of times winner had the most of a color
color_data = [0, 0, 0, 0, 0, 0, 0]
color_names = ["Dark Blue", "Yellow", "Red", "Orange", "Pink", "Light Blue", "Brown"]   # For printing

sim_to_run = 1000  # Amount of simulations to run

#P = player.Player("Name", spendingAI)
# spendingAI < 0.5 passive
# spendingAI > 0.5 aggressive
# spendingAI = 0.5 neutral

P1 = player.Player("Comp1", 1)
P2 = player.Player("Comp2", 1)
P3 = player.Player("Comp3", 1)
P4 = player.Player("Comp4", 1)
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
        player.chance_times = 0
        player.community_times = 0
    for card in board:
        card.cur_owner = "Bank"
        card.total_houses = 0
    global globalvals
    globalvals = [32, 12, 20580, False]


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


def luck_data(players):
    for player in players:
        print("Amount of chance cards drawn for ", player.name, ":", player.chance_times)
        print("Amount of community chest cards drawn for ", player.name, ":", player.community_times)



def winner_data(players):
    for player in players:
        if not player.bankrupt:
            # Add more data
            if (player.name == P1.name):
                numwins[0] += 1
            if (player.name == P2.name):
                numwins[1] += 1
            if (player.name == P3.name):
                numwins[2] += 1
            if (player.name == P4.name):
                numwins[3] += 1
                
            player_data = "Player name:", player.name, "AI Spending level:", player.spendingAI
           # print(player_data, "Properties held:", "\n")
            #for props in player.property:
               # print(props.name, "(", props.type, ")")
                
            break


def main():
    print(globalvals)
    total_turncount = 0
    for i in range(sim_to_run):
        turn_count = 0
        while not game_over(players):   # Infinite loop as of now

            #go through player array calling move/position_action
            for person in players:
                person.move(person.position, board, globalvals)
                person.position_action(board, players, globalvals)
                if not person.bankrupt:
                    turn_count += 1
                #print("global houses:", globalvals[0], "global hotels:", globalvals[1])
                if game_over(players):
                    print("---------------------------------------------GAME OVER!!!! SIMULATION ", (i+1), " IS OVER----------------------------------------------------------------")
                    winner_data(players)
                    get_color_data(players)
                    #luck_data(players)
                    #print("Amount of turns in this simulation: ", turn_count)
                    total_turncount += turn_count
                    break
        #get_color_data(players)
        #winner_data(players)
        reset_game(players)
    max_value = max(color_data)
    list_of_max = [i for i, j in enumerate(color_data) if j == max_value]
    print("Color most frequently collected: ")
    for i in list_of_max:
        print(color_names[i])

    for i in range(len(color_data)):
        print("|",color_names[i],":", color_data[i],"|", end = ' ')

    print("\n","Average Number of Turns: ", total_turncount/sim_to_run)
  

    print("\n","Number of Wins for Each Player: ")
    print(P1.name,"(",P1.spendingAI,")", "Wins: ", numwins[0])
    print(P2.name,"(",P2.spendingAI,")", "Wins: ", numwins[1])
    print(P3.name,"(",P3.spendingAI,")", "Wins: ", numwins[2])
    print(P4.name,"(",P4.spendingAI,")", "Wins: ", numwins[3])

    fig = plt.figure()
    ax = fig.add_axes([.1, .1, .9, .8])
    p1string = P1.name,"(",str(P1.spendingAI),")" 
    P2string = P2.name,"(",str(P2.spendingAI),")" 
    p3string = P3.name,"(",str(P3.spendingAI),")" 
    p4string = P4.name,"(",str(P4.spendingAI),")" 
    #x = [p1string, P2string, p3string, p4string]
    x = [P1.name, P2.name, P3.name, P4.name]
    ax.bar(x, numwins)
    plt.xlabel('Players')
    plt.ylabel('Number of Wins')
    plt.title('# of Wins by Player')
    plt.show()
  

if __name__ == "__main__":
    main()

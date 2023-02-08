import board as board
import player as player
import playstyle as playstyle
import matplotlib.pyplot as plt
import random
import numpy


board = board.cards_and_positions()

numwins = [0, 0, 0, 0]
globalvals = [32, 12, 20580, False, 4]
winarr = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
placearr = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
AIgames = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
avgarr = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


# Amount of times winner had the most of a color
color_data = [0, 0, 0, 0, 0, 0, 0, 0, 0]
color_names = ["Dark Blue", "Yellow", "Red", "Orange", "Pink", "Light Blue", "Brown", "Railroads", "Utility"]   # For printing

sim_to_run = 100 # Amount of simulations to run

w, h = 10, sim_to_run
variancearr = [[0 for x in range(w)] for y in range(h)] 
totalvararr = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#P = player.Player("Name", spendingAI)
# spendingAI < 0.5 passive
# spendingAI > 0.5 aggressive
# spendingAI = 0.5 neutral

#P1 = player.Player("Comp1", 1)
#P2 = player.Player("Comp2", .1)
#P3 = player.Player("Comp3", 1)
#P4 = player.Player("Comp4", 1)
#players = {P1, P2, P3, P4}


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
        player.placement = 1
    for card in board:
        card.cur_owner = "Bank"
        card.total_houses = 0
    global globalvals
    globalvals = [32, 12, 20580, False, 4]


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
    cardRoad = 0
    cardUtility = 0
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
                elif card.type == "Railroad":
                    cardRoad += 1
                elif card.type == "Utility":
                    cardUtility += 1
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
    if cardRoad == 4:
        color_data[7] += 1
    if cardUtility == 2:
        color_data[8] += 1


def luck_data(players):
    for player in players:
        print("Amount of chance cards drawn for ", player.name, ":", player.chance_times)
        print("Amount of community chest cards drawn for ", player.name, ":", player.community_times)



def winner_data(players):
    for player in players:
        #print(list(players)[0].spendingAI * 10 - 1)
        #print(list(players)[1].spendingAI * 10 - 1)
        #print(list(players)[2].spendingAI * 10 - 1)
        #print(list(players)[3].spendingAI * 10 - 1)

        if not player.bankrupt:
            # Add more data
            if (player.name == list(players)[0].name):
                numwins[0] += 1
                #print(list(players)[0].spendingAI * 10 - 1)
                winarr[int(list(players)[0].spendingAI * 10 - 1)] += 1
                
            if (player.name == list(players)[1].name):
                numwins[1] += 1
                #print(list(players)[1].spendingAI * 10 - 1)
                winarr[int(list(players)[1].spendingAI * 10 - 1)] += 1
                
            if (player.name == list(players)[2].name):
                numwins[2] += 1
                #print(list(players)[2].spendingAI * 10 - 1)
                winarr[int(list(players)[2].spendingAI * 10 - 1)] += 1
               
            if (player.name == list(players)[3].name):
                numwins[3] += 1
                #print(list(players)[3].spendingAI * 10 - 1)
                winarr[int(list(players)[3].spendingAI * 10 - 1)] += 1
                
                
            player_data = "Player name:", player.name, "AI Spending level:", player.spendingAI
           # print(player_data, "Properties held:", "\n")
            #for props in player.property:
               # print(props.name, "(", props.type, ")")
                
            break

def placement_data(players, i):
    for person in players:
        variancearr[i][int (person.spendingAI * 10 - 1)] += person.placement
        AIgames[int (person.spendingAI * 10 - 1)] += 1  
        placearr[int (person.spendingAI * 10 - 1)] += person.placement       
        #print(person.name , person.spendingAI , " placed" , person.placement)

def get_avg(arr1, arr2):
    for x in range(len(arr1)):
        if(arr1[x] ==0 or arr2[x] == 0):
            avgarr[x] = 0
        else:
            avgarr[x] = arr1[x]/arr2[x]
    return avgarr

def get_var(avgarr, variancearr):
    for i in range(len(avgarr)):
        for x in range(sim_to_run):
           totalvararr[i] += pow(variancearr[x][i] - avgarr[i], 2)
        if(totalvararr[i] == 0 or AIgames[i] == 0):
            totalvararr[i] = 0
        else:  
            totalvararr[i] /= AIgames[i]
    return totalvararr

        
def main():
    print(globalvals)
    total_turncount = 0
    for i in range(sim_to_run):
        turn_count = 0
        # ************comment out if you don't want random, and uncomment the global player variables at the top of the code
        P1 = player.Player("Comp1", random.randint(1,10)/10)
        P2 = player.Player("Comp2", random.randint(1,10)/10)
        P3 = player.Player("Comp3", random.randint(1,10)/10)
        P4 = player.Player("Comp4", random.randint(1,10)/10)
        #print(P1.spendingAI)
        #print(P2.spendingAI)
        #print(P3.spendingAI)
        #print(P4.spendingAI)
        players = {P1, P2, P3, P4}
        # **************
        while not game_over(players):  

            #go through player array calling move/position_action
            for person in players:
                person.move(person.position, board, globalvals)
                person.position_action(board, players, globalvals)
                if not person.bankrupt:
                    turn_count += 1
                #print("global houses:", globalvals[0], "global hotels:", globalvals[1])
                if game_over(players):
                    placement_data(players, i)
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
    print(winarr)
    #print(placearr)
    #print(AIgames, "<---- games")
    #print(variancearr)

    print(get_avg(placearr, AIgames) , "<------averages")
    print(get_var(avgarr, variancearr), "<----- variances")

    fig = plt.figure()
    ax = fig.add_axes([.1, .1, .9, .8])
    #x = [P1.name, P2.name, P3.name, P4.name]
    x = [".1", ".2", ".3", ".4", ".5", ".6", ".7", ".8", ".9", "1"]
    #ax.bar(x, numwins)
    ax.bar(x, winarr)
    plt.xlabel('Player AI Level')
    plt.ylabel('Number of Wins')
    plt.title('Number of Wins by Player AI Level with 10000 Runs')
    plt.show()
  

if __name__ == "__main__":
    main()

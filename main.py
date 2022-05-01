import board as board
import player as player
import playstyle as playstyle

board = board.cards_and_positions()

globalvals = [32, 12]

sim_to_run = 1  # Amount of simulations to run
#P = player.Player("Name", spendingAI)
# spendingAI < 0.5 passive
# spendingAI > 0.5 aggressive
# spendingAI = 0.5 neutral

P1 = player.Player("Comp1", 1)
P2 = player.Player("Comp2", 1)
P3 = player.Player("Comp3", 1)
P4 = player.Player("Comp4", 1)
players = {P1, P2, P3, P4}


def game_over(players):
    remaining = len(players)
    for player in players:
        if player.bankrupt:
            remaining -= 1
    if remaining == 1:
        return True
    else:
        return False


def winner_data(players):
    for player in players:
        if not player.bankrupt:
            # Add more data
            player_data = "Player name:", player.name, "AI Spending level:", player.spendingAI
            print(player_data, "Properties held:", "\n")
            for props in player.property:
                print(props.name)
            break


def main():
    for i in range(sim_to_run):
        while not game_over(players):   # Infinite loop as of now

            #go through player array calling move/position_action
            for person in players:
                person.move(person.position, board)
                person.position_action(board, players, globalvals)
                print("global houses:", globalvals[0], "global hotels:", globalvals[1])
          
                if game_over(players):
                    break

        winner_data(players)    

    

if __name__ == "__main__":
    main()

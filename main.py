import board as board
import player as player
import playstyle as playstyle

board = board.cards_and_positions()

sim_to_run = 1  # Amount of simulations to run
#P = player.Player("Name", spendingAI)
# spendingAI < 0.5 passive
# spendingAI > 0.5 aggressive
# spendingAI = 0.5 neutral
P1 = player.Player("Comp1", 0.5)
P2 = player.Player("Comp2", 1.0)
players = {P1, P2}


def game_over(player_list):
    remaining = len(player_list)
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
            player_data = "Player name:", player.name, "\nAI Spending level:", player.spendingAI, "\n"
            data = player_data, "Properties held:", player.property, "\n"
            return data


def main():
    for i in range(sim_to_run):
        while not game_over(players):   # Infinite loop as of now

            #go through player array calling move/position_action
            # P1.move(P1.position)
            # P1.position_action(board)
            # P2.move(P2.position)
            # P2.position_action(board)
            for person in players:
                person.move(person.position)
                person.position_action(board)
            

if __name__ == "__main__":
    main()

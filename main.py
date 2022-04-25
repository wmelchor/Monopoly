import board as board
import player as player

board = board.cards_and_positions()

P1 = player.Player("Comp1", 0.6)
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
    while not game_over(players): # Infinite loop as of now
        P1.move(P1.position)
        P1.position_action(board)
        P2.move(P2.position)
        P2.position_action(board)


if __name__ == "__main__":
    main()

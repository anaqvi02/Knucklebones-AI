import random
import os
import time
from game import KnucklebonesGame
from mcts_ai import run_mcts_search

os.environ.setdefault('TERM', 'xterm')

AI_DIFFICULTY = 5000

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_board(game, player_roll=None, ai_roll=None):
    clear_screen()
    print("--- Knucklebones: You vs. The AI ---")

    p1_board = game.get_board(1)
    p2_board = game.get_board(2)

    p1_scores = [game._calculate_column_score(col) for col in p1_board]
    p2_scores = [game._calculate_column_score(col) for col in p2_board]
    p1_total = sum(p1_scores)
    p2_total = sum(p2_scores)

    ai_roll_str = f"AI rolled: [{ai_roll}]" if ai_roll else ""
    print(f"{'' :>25} {ai_roll_str}")

    print("          AI's Board")
    print(f"Score: {p2_total}")
    padded_p2_board = [col + [' '] * (3 - len(col)) for col in p2_board]
    for i in range(2, -1, -1):
        print(f"      +---+---+---+")
        print(f"      | {padded_p2_board[0][i]} | {padded_p2_board[1][i]} | {padded_p2_board[2][i]} |")
    print(f"      +---+---+---+")
    print(f"Scores: | {p2_scores[0]:<2}| {p2_scores[1]:<2}| {p2_scores[2]:<2}|")


    print("\n" + "="*30 + "\n")

    print(f"Scores: | {p1_scores[0]:<2}| {p1_scores[1]:<2}| {p1_scores[2]:<2}|")
    padded_p1_board = [col + [' '] * (3 - len(col)) for col in p1_board]
    for i in range(3):
        print(f"      +---+---+---+")
        print(f"      | {padded_p1_board[0][i]} | {padded_p1_board[1][i]} | {padded_p1_board[2][i]} |")
    print(f"      +---+---+---+")
    print("          Your Board")
    print(f"Score: {p1_total}")


    player_roll_str = f"You rolled: [{player_roll}]" if player_roll else ""
    print(f"\n{player_roll_str}")


def get_player_move(game, dice_roll):
    valid_actions = game.get_valid_actions()
    while True:
        try:
            action_str = input(f"Choose a column (0, 1, or 2) to place your [{dice_roll}]: ")
            action = int(action_str)
            if action in valid_actions:
                return action
            else:
                print("Invalid move. That column is full.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def main():
    game = KnucklebonesGame()
    print("Welcome to Knucklebones!")
    print("Ai difficulty is set to:", AI_DIFFICULTY)
    game.current_player = random.choice([1, 2])

    while not game.is_game_over():
        if game.current_player == 1:
            dice_roll = random.randint(1, 6)
            print_board(game, player_roll=dice_roll)
            move = get_player_move(game, dice_roll)
            game.make_move(move, dice_roll)
        else:
            dice_roll = random.randint(1, 6)
            print_board(game, ai_roll=dice_roll)
            print("\nAI is thinking...")
            time.sleep(1)

            ai_state = game.clone()
            move = run_mcts_search(ai_state, dice_roll, game)
            game.make_move(move, dice_roll)

            print_board(game)
            print(f"\nAI placed its [{dice_roll}] in column {move}.")
            time.sleep(1.5)

    print_board(game)
    winner = game.get_winner()
    print("\n" + "---" * 10)
    print("      !!! GAME OVER !!!")
    print("---" * 10)

    if winner == 1:
        print("Congratulations! You won!")
    elif winner == 2:
        print("The AI has defeated you. Better luck next time!")
    else:
        print("It's a draw!")

if __name__ == "__main__":
    main()
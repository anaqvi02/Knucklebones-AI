import random
import concurrent.futures
import os
import argparse
from tqdm import tqdm

from game import KnucklebonesGame
from mcts_ai import run_mcts_search
import config


def play_one_game(ai_iterations):
    game = KnucklebonesGame()

    while not game.is_game_over():
        dice_roll = random.randint(1, 6)

        state_for_ai = game.clone()

        move = run_mcts_search(state_for_ai, dice_roll, ai_iterations)

        game.make_move(move, dice_roll)

    return game.get_winner()


def main():
    parser = argparse.ArgumentParser(description="Knucklebones MCTS Self-Play Simulation")
    parser.add_argument(
        '--ai_iterations', 
        type=int, 
        default=config.AI_DIFFICULTY, 
        help='Number of MCTS iterations per move for the AI (higher = stronger AI, slower simulation)'
    )
    args = parser.parse_args()

    print("--- Knucklebones MCTS Self-Play Simulation ---")

    stats = {'p1_wins': 0, 'p2_wins': 0, 'draws': 0}

    num_workers = max(1, os.cpu_count() - 1)

    while True:
        try:
            num_matches_str = input(
                f"\nHow many matches to simulate? (Current Total: {sum(stats.values())}) [Enter to exit]: ")
            if not num_matches_str:
                print("Exiting.")
                break

            num_matches = int(num_matches_str)
            if num_matches <= 0:
                raise ValueError("you need 1 match at least")

        except ValueError:
            print("Invalid input. Please enter a positive whole number.")
            continue

        print(
            f"\nRunning {num_matches} new matches on {num_workers} CPU cores (AI strength: {args.ai_iterations} iterations/move)...")

        results = []
        with concurrent.futures.ProcessPoolExecutor(max_workers=num_workers) as executor:
            futures = [executor.submit(play_one_game, args.ai_iterations) for _ in range(num_matches)]
            for future in tqdm(concurrent.futures.as_completed(futures), total=num_matches, desc="Simulating Games"):
                results.append(future.result())

        for winner in results:
            if winner == 1:
                stats['p1_wins'] += 1
            elif winner == 2:
                stats['p2_wins'] += 1
            else:
                stats['draws'] += 1

        total_games = sum(stats.values())
        p1_win_rate = (stats['p1_wins'] / total_games) * 100 if total_games > 0 else 0
        p2_win_rate = (stats['p2_wins'] / total_games) * 100 if total_games > 0 else 0

        print("\n--- Cumulative Results ---")
        print(f"Total Matches Played: {total_games}")
        print(f"Player 1 Wins: {stats['p1_wins']} ({p1_win_rate:.2f}%)")
        print(f"Player 2 Wins: {stats['p2_wins']} ({p2_win_rate:.2f}%)")
        print(f"Draws: {stats['draws']}")
        print("--------------------------")


if __name__ == "__main__":
    main()
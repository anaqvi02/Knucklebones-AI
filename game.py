import random
import copy


class KnucklebonesGame:

    def __init__(self):
        self.player1_board = [[], [], []]
        self.player2_board = [[], [], []]
        self.current_player = 1

    def clone(self):
        return copy.deepcopy(self)

    def get_board(self, player):
        return self.player1_board if player == 1 else self.player2_board

    def get_opponent_board(self, player):
        return self.player2_board if player == 1 else self.player1_board

    def get_valid_actions(self):
        board = self.get_board(self.current_player)
        return [c for c in range(3) if len(board[c]) < 3]

    def make_move(self, column, dice_roll):
        player_board = self.get_board(self.current_player)
        opponent_board = self.get_opponent_board(self.current_player)

        opponent_board[column] = [die for die in opponent_board[column] if die != dice_roll]

        player_board[column].append(dice_roll)

        self.current_player = 2 if self.current_player == 1 else 1

    def is_game_over(self):
        p1_full = all(len(col) == 3 for col in self.player1_board)
        p2_full = all(len(col) == 3 for col in self.player2_board)
        return p1_full or p2_full

    def _calculate_column_score(self, column):
        score = 0
        counts = {}
        for die in column:
            counts[die] = counts.get(die, 0) + 1

        for die, count in counts.items():
            score += die * count * count
        return score

    def get_winner(self):
        p1_score = sum(self._calculate_column_score(col) for col in self.player1_board)
        p2_score = sum(self._calculate_column_score(col) for col in self.player2_board)

        if p1_score > p2_score:
            return 1
        elif p2_score > p1_score:
            return 2
        else:
            return 0

    def __eq__(self, other):
        if not isinstance(other, KnucklebonesGame):
            return NotImplemented
        return (self.player1_board == other.player1_board and
                self.player2_board == other.player2_board and
                self.current_player == other.current_player)

    def __hash__(self):
        p1_board_tuple = tuple(tuple(col) for col in self.player1_board)
        p2_board_tuple = tuple(tuple(col) for col in self.player2_board)
        return hash((p1_board_tuple, p2_board_tuple, self.current_player))
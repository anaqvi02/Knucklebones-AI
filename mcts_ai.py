import math
import random
import collections
import config

UCT_C = config.UCT_C
RAVE_EQUIVALENCE = config.RAVE_EQUIVALENCE

def _calculate_heuristic_score(game, column, dice_roll):
    player = game.current_player
    player_board = game.get_board(player)
    opponent_board = game.get_opponent_board(player)

    original_column = player_board[column]
    temp_column = original_column + [dice_roll]
    new_score = game._calculate_column_score(temp_column)
    old_score = game._calculate_column_score(original_column)
    score_gain = new_score - old_score

    opponent_column = opponent_board[column]
    disruption_gain = 0
    if dice_roll in opponent_column:
        opponent_original_score = game._calculate_column_score(opponent_column)
        temp_opponent_column = [d for d in opponent_column if d != dice_roll]
        opponent_new_score = game._calculate_column_score(temp_opponent_column)
        disruption_gain = opponent_original_score - opponent_new_score

    combo_bonus = 0
    counts = collections.defaultdict(int)
    for die in temp_column:
        counts[die] += 1
    
    dice_count = counts[dice_roll]
    if dice_count == 2:
        combo_bonus = dice_roll * config.HEURISTIC_WEIGHT_COMBO_PAIR
    elif dice_count == 3:
        combo_bonus = dice_roll * config.HEURISTIC_WEIGHT_COMBO_TRIPLE

    poison_penalty = 0
    if dice_roll < 3:
        for die_in_col in original_column:
            if die_in_col > 4:
                poison_penalty += (die_in_col - dice_roll) * config.HEURISTIC_WEIGHT_POISON_PENALTY

    return score_gain + (disruption_gain * config.HEURISTIC_WEIGHT_DISRUPTION) + combo_bonus - poison_penalty


class MCTSNode:
    def __init__(self, game_state, parent=None, move=None):
        self.state = game_state
        self.parent = parent
        self.move = move
        self.wins = 0
        self.visits = 0
        self.children = []
        self.untried_moves = self.state.get_valid_actions()
        self.rave_wins = collections.defaultdict(float)
        self.rave_visits = collections.defaultdict(int)

    def select_best_child_rave(self):
        best_score = -1
        best_child = None

        for child in self.children:
            if child.visits == 0:
                return child

            mcts_q = child.wins / child.visits

            rave_q = self.rave_wins[child.move] / (self.rave_visits[child.move] + 1e-6)

            beta = math.sqrt(RAVE_EQUIVALENCE / (3 * self.visits + RAVE_EQUIVALENCE))
            
            combined_q = (1 - beta) * mcts_q + beta * rave_q

            exploration_term = UCT_C * math.sqrt(math.log(self.visits) / child.visits)
            
            uct_score = combined_q + exploration_term

            if uct_score > best_score:
                best_score = uct_score
                best_child = child
        
        return best_child

    def expand(self, child_node):
        self.untried_moves.remove(child_node.move)
        self.children.append(child_node)
        return child_node

    def update(self, winner, sim_moves_p1, sim_moves_p2):
        self.visits += 1
        if self.state.current_player != winner and winner != 0:
            self.wins += 1
        elif winner == 0:
            self.wins += 0.5

        for move in sim_moves_p1:
            self.rave_visits[move] += 1
            if winner == 1: self.rave_wins[move] += 1
            elif winner == 0: self.rave_wins[move] += 0.5
        
        for move in sim_moves_p2:
            self.rave_visits[move] += 1
            if winner == 2: self.rave_wins[move] += 1
            elif winner == 0: self.rave_wins[move] += 0.5


def run_mcts_search(game_state, dice_roll, game_instance):
    total_cells_filled = sum(len(col) for col in game_instance.player1_board) + sum(len(col) for col in game_instance.player2_board)
    
    if total_cells_filled < 6:
        iterations = config.AI_DIFFICULTY // 2
    elif total_cells_filled < 12:
        iterations = config.AI_DIFFICULTY
    else:
        iterations = config.AI_DIFFICULTY * 2

    iterations = max(iterations, 100)

    transposition_table = {}

    root = MCTSNode(game_state=game_state)
    transposition_table[game_state] = root

    if not root.untried_moves:
        return None

    for _ in range(iterations):
        node = root
        
        while not node.untried_moves and node.children:
            node = node.select_best_child_rave()
        
        current_sim_state = node.state.clone()

        if node.untried_moves:
            move = random.choice(node.untried_moves)
            roll_for_expansion = dice_roll if node is root else random.randint(1, 6)
            
            temp_sim_state = node.state.clone()
            temp_sim_state.make_move(move, roll_for_expansion)

            if temp_sim_state in transposition_table:
                child_node = transposition_table[temp_sim_state]
                node = child_node
            else:
                child_node = MCTSNode(game_state=temp_sim_state, parent=node, move=move)
                transposition_table[temp_sim_state] = child_node
                node.untried_moves.remove(move)
                node.children.append(child_node)
                node = child_node

        sim_moves_p1 = []
        sim_moves_p2 = []
        sim_state_for_playout = current_sim_state.clone()

        while not sim_state_for_playout.is_game_over():
            sim_dice_roll = random.randint(1, 6)
            valid_moves = sim_state_for_playout.get_valid_actions()
            if not valid_moves: break
            
            best_move = max(valid_moves, key=lambda m: _calculate_heuristic_score(sim_state_for_playout, m, sim_dice_roll))
            
            if sim_state_for_playout.current_player == 1: sim_moves_p1.append(best_move)
            else: sim_moves_p2.append(best_move)
            
            sim_state_for_playout.make_move(best_move, sim_dice_roll)

        winner = sim_state_for_playout.get_winner()
        while node is not None:
            node.update(winner, sim_moves_p1, sim_moves_p2)
            node = node.parent

    if not root.children:
        return random.choice(game_state.get_valid_actions())
        
    best_move = max(root.children, key=lambda c: c.visits).move
    return best_move
# God of Knucklebones

A Python implementation of Knucklebones, the dice game from *Cult of the Lamb*, with an AI opponent using Monte Carlo Tree Search.

## Rules

Knucklebones is a two-player dice game. Each player has a 3×3 grid.

1. On your turn, roll a die (1-6) and place it in any column with space
2. Matching dice in a column multiply: two of a kind score 2× each, three of a kind score 3× each
3. Placing a die removes all matching dice from your opponent's corresponding column
4. The game ends when either player fills their board. Highest score wins.

## Features

- MCTS-based AI with RAVE (Rapid Action Value Estimation)
- Terminal interface
- Self-play mode for AI analysis
- Configurable search depth

## Installation

```bash
git clone https://github.com/yourusername/god-of-knucklebones.git
cd god-of-knucklebones
pip install -r requirements.txt
```

## Usage

Play against the AI:

```bash
python play.py
```

Run self-play simulations:

```bash
python train.py
python train.py --ai_iterations 10000
```

## Configuration

AI parameters in `config.py`:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `AI_DIFFICULTY` | 5000 | MCTS iterations per move |
| `UCT_C` | 1.414 | UCT exploration constant |
| `RAVE_EQUIVALENCE` | 350 | RAVE blending parameter |

## Structure

```
play.py       # Main game interface
train.py      # Self-play simulation
game.py       # Game logic
mcts_ai.py    # AI implementation
config.py     # Parameters
```

## License

MIT

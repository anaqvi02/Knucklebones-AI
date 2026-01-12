# 🎲 God of Knucklebones

A Python implementation of **Knucklebones**, the dice game from *Cult of the Lamb*, featuring an AI opponent powered by Monte Carlo Tree Search (MCTS).

## Game Rules

Knucklebones is a two-player dice game played on a 3×3 grid per player:

1. **Roll & Place**: On your turn, roll a die (1-6) and place it in any column that isn't full
2. **Scoring**: Each column scores the sum of its dice, with **multipliers for matching values**:
   - Two matching dice = each worth 2× their value
   - Three matching dice = each worth 3× their value
3. **Destruction**: When you place a die, it **removes all matching dice** from your opponent's corresponding column
4. **Game End**: The game ends when either player fills their board. Highest total score wins!

## Features

- 🤖 **Smart AI** using MCTS with RAVE (Rapid Action Value Estimation)
- 🎮 **Terminal-based gameplay** with a clean visual interface
- 📊 **Self-play training mode** for analyzing AI performance
- ⚙️ **Configurable difficulty** via MCTS iterations

## Installation

```bash
git clone https://github.com/yourusername/god-of-knucklebones.git
cd god-of-knucklebones
pip install -r requirements.txt
```

## Usage

### Play Against the AI

```bash
python play.py
```

### Run Self-Play Simulations

Test the AI against itself to analyze balance and performance:

```bash
python train.py
python train.py --ai_iterations 10000  # Stronger AI (slower)
```

## Configuration

Edit `config.py` to tune AI parameters:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `AI_DIFFICULTY` | 5000 | MCTS iterations per move |
| `UCT_C` | 1.414 | Exploration constant (√2) |
| `RAVE_EQUIVALENCE` | 350 | RAVE blending parameter |

## Project Structure

```
├── play.py       # Play against AI (main entry point)
├── train.py      # AI self-play simulation
├── game.py       # Game logic and rules
├── mcts_ai.py    # MCTS AI implementation
└── config.py     # Configuration parameters
```

## License

MIT License - see [LICENSE](LICENSE) for details.

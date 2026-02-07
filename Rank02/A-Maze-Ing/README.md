*This project has been created as part of the 42 curriculum by mramidam and mnassiri.*

# A-Maze-Ing

A maze generator and solver featuring multiple generation and solving algorithms with an interactive terminal visualizer.

## Description

A-Maze-Ing is a command-line maze generator that creates perfect or imperfect mazes with a "42" pattern embedded in the center. The project includes:
- **Maze generation** using Hunt and Kill or Recursive Backtracker algorithms
- **Pathfinding** with BFS (shortest path) or DFS algorithms
- **Interactive visualizer** with animated path solving and customizable colors
- **Configurable parameters** via a config file
- **Reusable Python package** (`mazegen`) for integration in other projects

## Instructions

### Running the CLI

```bash
python3 a_maze_ing.py config.txt
```
Or
```bash
./a_maze_ing.py config.txt
```
### Installing the Package

**Using the wheel (recommended):**
```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

**Using the source distribution (tar.gz):**
```bash
pip install mazegen-1.0.0.tar.gz
```

> **Note:** The wheel (`.whl`) is faster to install since it's pre-built. The source distribution (`.tar.gz`) will be built during installation, which may take slightly longer but works on all platforms.

Or build from source:
```bash
pip install build
python -m build
pip install dist/mazegen-1.0.0-py3-none-any.whl  # or dist/mazegen-1.0.0.tar.gz
```

### Building and Installing in a Virtual Environment

```bash
# 1. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# 2. Install build tools
pip install build

# 3. Build the package (creates dist/ in project folder)
python -m build

# 4. Install the package into the venv
pip install dist/mazegen-1.0.0-py3-none-any.whl

# 5. Test it works
python -c "from mazegen import MazeGenerator; print('Package installed successfully!')"
```

## Config File Format Description

```text
# required
WIDTH=30                                    # Maze width in cells (required)
HEIGHT=30                                   # Maze height in cells (required)
ENTRY=0,0                                   # Entry point x,y (required)
EXIT=0,29                                   # Exit point x,y (required)
OUTPUT_FILE=maze.txt                        # Output file path (required)
PERFECT=yes                                 # yes/no - Perfect maze or add loops (required)

# optional
SEED=42                                     # Random seed for reproducibility (optional)
ALGORITHM=BFS                               # BFS or DFS for pathfinding (optional, default: BFS)
GEN_ALGORITHM=RECURSIVE_BACKTRACKER         # Another algo for maze generation (optional)
```

## Visualizer

After generating a maze, an interactive terminal-based visualizer launches automatically using the `curses` library. Features include:

- **Animated solution path** - Watch the path trace through the maze step by step
- **ASCII title screen** - Displays project name using pyfiglet on startup
- **Interactive menu** - Press number keys to access options:
  - `1` - Re-generate a new maze
  - `2` - Show/Hide the solution path
  - `3` - Cycle through wall colors
  - `4` - Cycle through "42" pattern colors
  - `5` - Cycle through solution path colors
  - Any other key - Exit the visualizer

> **Note:** The visualizer requires a terminal large enough to display the maze. If the terminal is too small, an error message will be shown.

## Algorithms

The project implements **4 algorithms** total: 2 for maze generation and 2 for pathfinding.

### Maze Generation Algorithms

| Algorithm | Description | Config Value |
|-----------|-------------|---------------|
| **Hunt and Kill** (default) | Two-phase algorithm: random walk (kill) then scan for unvisited cells (hunt) | `hunt_and_kill` |
| **Recursive Backtracker** | DFS-based algorithm using a stack for backtracking | `recursive_backtracker` |

We chose **Hunt and Kill** as the default because:
1. Easy to implement with two simple phases
2. Always produces perfect mazes
3. Easy to add imperfections by removing random walls
4. Produces mazes with long, winding passages

### Pathfinding Algorithms

| Algorithm | Description | Config Value |
|-----------|-------------|---------------|
| **BFS** (default) | Breadth-First Search - guarantees shortest path | `BFS` |
| **DFS** | Depth-First Search - finds any valid path, memory efficient | `DFS` |

## Reusable Code: mazegen Package

The `mazegen/` directory is a standalone Python package that can be imported independently:

```python
from mazegen import MazeGenerator, bfs, dfs

# Create and generate maze
gen = MazeGenerator(width=20, height=20, seed=42)
maze = gen.generate()

# Find path
path = bfs(maze, entry=(0, 0), exit_=(19, 19))
print(path)  # "EESSSWW..."
```

### Package Contents

| Module | Description |
|--------|-------------|
| `MazeGenerator` | Generates mazes using Hunt & Kill or Recursive Backtracker |
| `Maze` | Maze data structure with wall operations |
| `bfs()` | Shortest path using Breadth-First Search |
| `dfs()` | Any path using Depth-First Search |

## Resources

### References
- [Hunt and Kill Algorithm - Jamis Buck](https://weblog.jamisbuck.org/2011/1/24/maze-generation-hunt-and-kill-algorithm) - Algorithm explanation and visualization
- [Maze Algorithms - Jamis Buck](https://www.jamisbuck.org/mazes/) - Interactive maze algorithm demos
- [Randomized dept-first search AKA recursive backtracker](https://en.wikipedia.org/wiki/Maze_generation_algorithm#Randomized_depth-first_search) - Algorithm explanation
- [Curses — Terminal handling for character-cell displays](https://docs.python.org/3/library/curses.html) - Terminal visualization display

### AI Usage
AI assistance (Claude/Gemini) was used for:
- **Debugging** - Help identifying issues with maze connectivity and validation
- **Organization** - Structuring the package for pip distribution
- **Documentation** - Structuring the readme for better visual presentation

All algorithm implementation and core logic was written by the team.

## Team & Project Management

### Team Roles

| Member | Responsibilities |
|--------|------------------|
| mramidam | Maze generation, pathfinding (BFS/DFS), package structure |
| mnassiri | Visualization |
| Both | Initial parsing implementation, bonus implementation |

### Planning Evolution
1. **Phase 1**: Config parsing (collaborative)
2. **Phase 2**: Split work - maze generation vs visualization
3. **Phase 3**: Integration and testing (collaborative)
4. **Phase 4**: Adding bonus for the project (collaborative)

### What Worked Well
- Clear separation of concerns between modules
- Using a config file for flexibility
- Creating a reusable package

### What Could Be Improved
- Earlier integration testing between components
- More comprehensive error messages

### Tools Used
- Python 3.10+
- Git for Version Control
- VSCode/Vim as IDE
- Pyfiglet for Title Screen

## Bonus Features

Beyond the mandatory requirements of the subject, we implemented:

| Bonus | Description |
|-------|-------------|
| **Extra Generation Algorithm** | Recursive Backtracker as alternative to Hunt and Kill |
| **Extra Solving Algorithm** | DFS as alternative to BFS |
| **Animated Solution** | Step-by-step visualization of the path being traced |
| **Title Screen** | ASCII art splash screen using pyfiglet on startup |

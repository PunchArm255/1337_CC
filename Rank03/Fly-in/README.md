*This project has been created as part of the 42 curriculum by mnassiri.*

# Fly-in

## Description
Fly-in is a drone routing and simulation system designed to navigate a fleet of autonomous drones through a network of interconnected zones from a start hub to an end hub in the minimum number of simulation turns.

The simulation enforces strict constraints including:
- Turn-based movement costs based on zone types (`normal`, `restricted`, `priority`, `blocked`).
- Zone occupancy capacities (`max_drones`, ignored on start and end hubs).
- Connection capacities (`max_link_capacity`).
- Multi-drone collision avoidance.

---

## Instructions

### Installation
Ensure Python 3.10+ is installed. Install all dependencies using the Makefile:
```bash
make install
```

### Execution
Run the simulation with the default map or specify a custom map:
```bash
make run
# or run with a custom map:
python3 main.py <path_to_map_file>
```

### Interactive Controls
- `[SPACE]`: Advance the simulation by one turn (animated).
- `[R]`: Restart the simulation from turn 0.
- `[ESC]`: Exit the program.

### Linting & Debugging
```bash
# static type checking and flake8 compliance
make lint

# strict type checking
make lint-strict

# debug mode via pdb
make debug MAP=map.txt

# clean cache files
make clean
```

---

## Algorithm Choices & Implementation Strategy

### Time-Expanded Cooperative Dijkstra
The pathfinding engine uses **Time-Expanded Cooperative Dijkstra**:
1. **Space-Time Graph**: A state is represented as `(turn, zone_name)`. This allows tracking spatial occupancy over discrete time steps.
2. **Reservations Table**: When a path is planned for Drone $i$, all occupied zones and transit connections are recorded in reservation tables (`zone_reservations[turn][zone]` and `link_reservations[turn][connection]`).
3. **Collision Avoidance**: Subsequent drones search for paths taking into account existing reservations. At any turn, a drone can either advance to an available neighboring zone or wait in place if capacity is constrained.
4. **Staggered Dispatch**: Drones start in staggered intervals to avoid traffic bottlenecks at the starting hub's neighboring gates.
5. **Inaccessible Zones**: Blocked zones are strictly ignored during neighbor expansion, guaranteeing zero invalid transitions.

---

## Visual Representation

The visualization is built with **Pygame**:
- **Dynamic Layout & Scaling**: Zone coordinates are automatically scaled, centered, and padded within the window, dynamically recalculating on window resize.
- **Smooth Easing**: Movement between turns is smoothly interpolated using a `smoothstep` curve ($3t^2 - 2t^3$) rather than abrupt jumping.
- **Minimalist Interface**: Features a compact turn counter badge and an unintrusive color legend to prioritize visibility of the map graph.
- **Zone & Drone Styling**: Distinct color coding for zone types (`normal`, `restricted`, `priority`, `blocked`, and start/end hubs) and detailed multi-rotor drone sprites with ID tags.

---

## Example Input & Expected Output

### Example Map Input
```text
nb_drones: 2

start_hub: start 0 0
hub: corridor 1 0 [max_drones=1]
end_hub: goal 2 0

connection: start-corridor
connection: corridor-goal
```

### Expected Output
```text
Loaded map: map.txt
  zones: 3
  connections: 2
  drones: 2

Calculating routes with dijkstra...
Pathfinding complete!

--- SIMULATION START (3 turns) ---

Turn   1: D1-corridor
Turn   2: D1-goal D2-corridor
Turn   3: D2-goal

--- SIMULATION COMPLETE ---
    total turns: 3
    drones delivered: 2 / 2
```

---

## Resources & AI Usage

### References
- [Dijkstra's Algorithm](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)
- [Multi-Agent Path Finding (MAPF)](https://en.wikipedia.org/wiki/Multi-agent_pathfinding)
- [Pygame Documentation](https://www.pygame.org/docs/)
- [Smoothstep Interpolation](https://en.wikipedia.org/wiki/Smoothstep)

### AI Usage
AI assistance was utilized during this project for:
- Refining the time-expanded state representation and reservation logic.
- Designing the Pygame rendering pipeline and smoothstep animation math.
- Setting up the project Makefile, type annotations, and linting configurations.
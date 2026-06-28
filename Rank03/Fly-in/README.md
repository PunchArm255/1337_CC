*This project has been created as part of the 42 curriculum by mnassiri.*

# Fly-in

## Description
Fly-in is a Python-based simulation engine and pathfinding algorithm designed to route a fleet of autonomous drones through a network of connected zones. The objective is to navigate all drones from a starting hub to an end hub in the fewest possible turns, while strictly adhering to zone capacities, connection limits, and varying movement costs (e.g., restricted zones). 

The project features a Time-Expanded Cooperative Dijkstra algorithm to prevent drone collisions, alongside a fully interactive, anti-aliased Pygame visualizer that allows step-by-step playback of the simulation.

## Instructions
**Installation:**
Ensure you have Python 3.10+ installed. Install the required dependencies using the Makefile:
`make install`

**Execution:**
To run the simulation with the default map:
`make run`
*(Or manually: `python3 main.py <path_to_map_file>`)*

**Controls:**
- `[SPACE]` : Advance the simulation by one turn.
- `[R]` : Restart the simulation from turn 0.
- `[ESC]` : Exit the program.

## Algorithm Choices & Implementation Strategy
The core pathfinding logic uses a **Time-Expanded Cooperative Dijkstra** algorithm. 
Standard Dijkstra calculates the shortest path through spatial nodes. To accommodate multiple drones without violating capacity constraints, the algorithm was expanded to include a dimension of *Time*. 
1. The engine calculates the optimal path for Drone 1 and logs its position at every turn into a 2D `Reservation Table`.
2. When calculating Drone 2, the algorithm checks this table. If a node is at maximum capacity during a specific turn, Dijkstra naturally evaluates the cost of waiting in place (`cost = 1`) versus taking a spatial detour.
3. Priority Queues (`heapq`) are utilized to ensure $O(E \log V)$ time complexity per drone.

## Visual Representation
The visualizer was built using Pygame and `pygame.gfxdraw` for hardware-accelerated anti-aliasing.
- **Dynamic Scaling:** The map automatically calculates bounding boxes to scale and center itself dynamically, responding to `VIDEORESIZE` events.
- **Smooth Animation:** Drones do not simply snap between zones. Movement is interpolated using a `smoothstep` ($3t^2 - 2t^3$) easing function, providing fluid, natural acceleration and deceleration.
- **Visual Feedback:** Zones are color-coded by type, and dynamic borders indicate start/end goals. A Heads-Up Display (HUD) provides real-time turn tracking.

## Resources
- [Dijkstra's Algorithm (Wikipedia)](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)
- [Cooperative Pathfinding / Multi-agent Pathfinding](https://en.wikipedia.org/wiki/Multi-agent_pathfinding)
- [Smoothstep Easing Functions](https://en.wikipedia.org/wiki/Smoothstep
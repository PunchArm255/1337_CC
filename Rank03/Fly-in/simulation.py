# simulation.py - converts paths into turn-by-turn simulation and output
from typing import Generator
from graph import Graph


class SimulationEngine:
    """Converts pathfinder paths into discrete turn events."""

    def __init__(
        self,
        graph: Graph,
        all_paths: list[list[tuple[int, str]]],
    ) -> None:
        self.graph = graph
        self.paths = all_paths
        # total turns is the latest turn any drone arrives at goal
        self.max_turn: int = max(
            (path[-1][0] for path in all_paths if path), default=0
        )

    def _get_drone_state(
        self,
        path: list[tuple[int, str]],
        turn: int,
    ) -> tuple[str | None, str]:
        """Evaluates a drone's action for a specific turn.

        Args:
            path: Drone route as a list of (turn, zone) tuples.
            turn: Current simulation turn number.

        Returns:
            Tuple of (output_string_or_None, visual_position_string).
        """
        for j in range(len(path) - 1):
            t_prev, z_prev = path[j]
            t_next, z_next = path[j + 1]

            if t_prev < turn <= t_next:
                if z_prev == z_next:
                    # drone is waiting in place, no output
                    return (None, z_prev)
                elif turn == t_next:
                    # drone arrived at destination zone
                    return (z_next, z_next)
                else:
                    # drone is mid-transit on cnx to restricted zone
                    connection_name = f"{z_prev}-{z_next}"
                    return (connection_name, connection_name)

        # if simulation continues past arrival, drone remains at goal
        if path and turn > path[-1][0]:
            return (None, path[-1][1])

        return (None, path[0][1] if path else "")

    def run(self) -> Generator[dict[str, str], None, None]:
        """Runs the simulation turns, printing moves and yielding visual state.

        Yields:
            Dictionary mapping drone ID to current position string.
        """
        print(f"\n--- SIMULATION START ({self.max_turn} turns) ---")
        print()

        for turn in range(1, self.max_turn + 1):
            movements: list[str] = []
            visual_state: dict[str, str] = {}

            for d_idx, path in enumerate(self.paths):
                drone_id = f"D{d_idx + 1}"
                if not path:
                    continue

                output, visual_pos = self._get_drone_state(path, turn)
                visual_state[drone_id] = visual_pos

                # only print drones that moved
                if output is not None:
                    movements.append(f"{drone_id}-{output}")

            if movements:
                print(f"Turn {turn:>3}: {' '.join(movements)}")

            # yield passes the visual state dict to pygame for rendering
            yield visual_state

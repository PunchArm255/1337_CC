# simulation.py - converts paths into turn-by-turn simulation and output
from typing import Generator
from graph import Graph


class SimulationEngine:
    """converts pathfinder paths into discrete turn events."""

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
        """evaluates a drone's action for a turn."""
        for j in range(len(path) - 1):
            t_prev, z_prev = path[j]
            t_next, z_next = path[j + 1]

            if t_prev < turn <= t_next:
                if z_prev == z_next:
                    # drone is waiting in place - omit from output per subject
                    return (None, z_prev)
                elif turn == t_next:
                    # drone arrived at destination zone
                    return (z_next, z_next)
                else:
                    # drone is mid-transit on connection to restricted zone
                    connection_name = f"{z_prev}-{z_next}"
                    return (connection_name, connection_name)

        # if simulation continues past arrival, drone remains at goal
        if path and turn > path[-1][0]:
            return (None, path[-1][1])

        return (None, path[0][1] if path else "")

    def run(self) -> Generator[dict[str, str], None, None]:
        """runs the simulation turns, printing moves and yielding state."""
        print(f"--- SIMULATION START ({self.max_turn} turns) ---")
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

        print()
        print("--- SIMULATION COMPLETE ---")
        print(f"    total turns: {self.max_turn}")
        delivered = len([p for p in self.paths if p])
        total = len(self.paths)
        print(f"    drones delivered: {delivered} / {total}")

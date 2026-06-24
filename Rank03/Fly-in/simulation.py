# simulation.py — translates pathfinder results into turn-by-turn output
#
# === what this file does ===
# the pathfinder gives us a list of paths — one per drone — where each
# path is a sequence of (turn, zone) pairs. for example:
#   drone 1's path: [(0, "start"), (1, "gate"), (2, "goal")]
#
# the simulation's job is to go through each turn (1, 2, 3, ...) and
# figure out what every drone is doing during that turn. three possibilities:
#   1. the drone MOVED to a new zone this turn -> print it
#   2. the drone is IN TRANSIT on a connection (restricted zone) -> print it
#   3. the drone is WAITING and didn't move -> skip it (subject says so)
#
# this produces two things:
#   - terminal output in the exact format the subject requires
#   - a visual state dict that gets yielded to pygame for animation
#
# === why does it use yield? ===
# yield is like "pause and hand off data". each turn, the simulation
# yields a dict of {drone_id: position} to the pygame loop. pygame
# draws the frame, waits for SPACE to be pressed, then calls next()
# to resume the simulation and get the next turn's state.
#
# this is a generator pattern — the simulation runs lazily, one turn
# at a time, driven by the pygame event loop.
#
# ref: https://realpython.com/introduction-to-python-generators/
# ref: https://docs.python.org/3/reference/expressions.html#yield-expressions

from typing import Generator
from graph import Graph


class SimulationEngine:
    """converts pathfinder results into turn-by-turn drone movements.

    this is the bridge between the algorithm (pathfinder) and the
    presentation layer (terminal output + pygame visualization).
    """

    def __init__(
        self,
        graph: Graph,
        all_paths: list[list[tuple[int, str]]]
    ) -> None:
        self.graph = graph
        self.paths = all_paths
        # find the last turn any drone arrives at the goal.
        # this tells us how many turns the simulation needs to run.
        # if a drone has no path (empty list), we skip it with the if guard.
        self.max_turn: int = max(
            (path[-1][0] for path in all_paths if path), default=0
        )

    def _get_drone_state(
        self,
        path: list[tuple[int, str]],
        turn: int
    ) -> tuple[str | None, str]:
        """figures out what a single drone is doing during a specific turn.

        returns a tuple of (output_string, visual_position):
          - output_string: the text to print (like "D1-roof1"), or None if waiting
          - visual_position: where to draw the drone in pygame

        how it works:
        we walk through the drone's path segments and find which segment
        covers the current turn. a segment is two consecutive path entries:
          path[j] = (t_prev, z_prev)  ->  path[j+1] = (t_next, z_next)

        if turn falls between t_prev and t_next, this is the active segment.
        """
        for j in range(len(path) - 1):
            t_prev, z_prev = path[j]
            t_next, z_next = path[j + 1]

            # is this turn within this segment's time range?
            if t_prev < turn <= t_next:
                if z_prev == z_next:
                    # drone is waiting in the same zone — don't print it
                    # (subject: "drones that do not move are omitted")
                    return (None, z_prev)

                elif turn == t_next:
                    # drone arrived at its destination this turn
                    return (z_next, z_next)

                else:
                    # drone is mid-transit on a connection (restricted zone,
                    # which takes 2 turns). it's between z_prev and z_next.
                    connection_name = f"{z_prev}-{z_next}"
                    return (connection_name, connection_name)

        # if we're past the drone's final turn, it's sitting at the goal
        if path and turn > path[-1][0]:
            return (None, path[-1][1])

        # shouldn't happen, but just in case
        return (None, path[0][1] if path else "")

    def run(self) -> Generator[dict[str, str], None, None]:
        """runs the simulation, yielding visual state for each turn.

        prints formatted output to terminal AND yields a dict of
        {drone_id: position_string} for the pygame visualizer.

        the position_string is either:
          - a zone name like "roof1" (drone is at that zone)
          - a connection like "roof1-roof2" (drone is in transit)
        """
        print(f"--- SIMULATION START ({self.max_turn} turns) ---")
        print()

        for turn in range(1, self.max_turn + 1):
            # collect movement strings for terminal output
            movements: list[str] = []
            # collect positions for pygame visualization
            visual_state: dict[str, str] = {}

            for d_idx, path in enumerate(self.paths):
                drone_id = f"D{d_idx + 1}"

                # skip drones that have no path (couldn't reach goal)
                if not path:
                    continue

                output, visual_pos = self._get_drone_state(path, turn)

                # always tell pygame where this drone is
                visual_state[drone_id] = visual_pos

                # only add to terminal output if the drone moved
                if output is not None:
                    movements.append(f"{drone_id}-{output}")

            # print to terminal with turn number for clarity
            if movements:
                print(f"Turn {turn:>3}: {' '.join(movements)}")

            # yield pauses here and hands visual_state to pygame.
            # when pygame calls next(), we resume at the top of the loop
            # and process the next turn.
            yield visual_state

        # summary at the end
        print()
        print(f"--- SIMULATION COMPLETE ---")
        print(f"    total turns: {self.max_turn}")
        print(f"    drones delivered: {len([p for p in self.paths if p])}"
              f" / {len(self.paths)}")
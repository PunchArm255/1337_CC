# pathfinder.py - finds the shortest path for each drone using dijkstra
import heapq
from collections import defaultdict
from graph import Graph


class Pathfinder:
    """Plans collision-free paths for all drones using Dijkstra."""

    def __init__(self, graph: Graph, nb_drones: int) -> None:
        self.graph = graph
        self.nb_drones = nb_drones

        # reservation tables: track booked zones and links per turn
        # zone_reservations[turn][zone_name] = count of booked drones
        self.zone_reservations: dict[int, dict[str, int]] = defaultdict(
            lambda: defaultdict(int)
        )
        # link_reservations[turn][frozenset({A, B})] = count of transit drones
        self.link_reservations: dict[
            int, dict[frozenset[str], int]
        ] = defaultdict(lambda: defaultdict(int))

        # search horizon limit to avoid infinite loops if goal is unreachable
        self.max_search_turns = max(
            500, len(self.graph.zones) * (self.nb_drones + 5) + 50
        )

    def _zone_is_free(self, zone_name: str, turn: int) -> bool:
        """Checks if a zone has available capacity at a specific turn.

        Args:
            zone_name: Name of the zone to check.
            turn: Simulation turn number.

        Returns:
            True if zone can accept another drone, False otherwise.
        """
        # start and end hubs have unlimited capacity per subject rules
        if zone_name in (
            self.graph.start_zone.name,
            self.graph.end_zone.name,
        ):
            return True
        zone = self.graph.get_zone(zone_name)
        if zone is None or zone.zone_type == "blocked":
            return False
        booked = self.zone_reservations[turn][zone_name]
        return booked < zone.max_drones

    def _link_is_free(self, z1: str, z2: str, turn: int) -> bool:
        """Checks if a connection has available capacity at a specific turn.

        Args:
            z1: Starting zone name.
            z2: Destination zone name.
            turn: Simulation turn number.

        Returns:
            True if the connection capacity allows traversal, False otherwise.
        """
        # waiting in place doesn't use any connection
        if z1 == z2:
            return True
        conn = self.graph.get_connection(z1, z2)
        if conn is None:
            return False
        link_key = frozenset({z1, z2})
        booked = self.link_reservations[turn][link_key]
        return booked < conn.max_link_capacity

    def _trace_path(
        self,
        end_state: tuple[int, str],
        start_state: tuple[int, str],
        came_from: dict[tuple[int, str], tuple[int, str]],
    ) -> list[tuple[int, str]]:
        """Reconstructs the full path from goal back to start.

        Args:
            end_state: Final (turn, zone) reached at the goal.
            start_state: Initial (turn, zone) where drone started.
            came_from: Map of state transitions used for backtracking.

        Returns:
            List of (turn, zone) steps forming the complete route.
        """
        path: list[tuple[int, str]] = []
        current = end_state
        while current in came_from:
            path.append(current)
            current = came_from[current]
        path.append(start_state)
        path.reverse()
        return path

    def _find_path(self, start_turn: int) -> list[tuple[int, str]]:
        """Runs time-expanded Dijkstra for a single drone.

        Args:
            start_turn: The turn at which the drone departs the start hub.

        Returns:
            List of (turn, zone) tuples if a route is found, else empty list.
        """
        start = self.graph.start_zone.name
        end = self.graph.end_zone.name

        # heap entry: (turn, -priority_score, zone_name)
        # priority score acts as a tie-breaker so priority zones are preferred
        pq: list[tuple[int, int, str]] = [(start_turn, 0, start)]
        visited: set[tuple[int, str]] = set()
        came_from: dict[tuple[int, str], tuple[int, str]] = {}
        best_cost: dict[tuple[int, str], tuple[int, int]] = {
            (start_turn, start): (start_turn, 0)
        }

        while pq:
            curr_turn, neg_p, curr_zone = heapq.heappop(pq)
            state = (curr_turn, curr_zone)
            priority_score = -neg_p

            # goal reached: reconstruct and return path
            if curr_zone == end:
                return self._trace_path(
                    state, (start_turn, start), came_from
                )

            # skip visited states or states exceeding search limit
            if state in visited or curr_turn > self.max_search_turns:
                continue
            visited.add(state)

            # option 1: wait in place for one turn
            wait_turn = curr_turn + 1
            if (
                wait_turn <= self.max_search_turns
                and self._zone_is_free(curr_zone, wait_turn)
            ):
                wait_state = (wait_turn, curr_zone)
                wait_cost = (wait_turn, -priority_score)
                if (
                    wait_state not in visited
                    and wait_cost < best_cost.get(wait_state, (10**9, 0))
                ):
                    best_cost[wait_state] = wait_cost
                    came_from[wait_state] = state
                    heapq.heappush(
                        pq, (wait_turn, -priority_score, curr_zone)
                    )

            # option 2: move to a neighboring zone
            for neighbor in self.graph.get_neighbours(curr_zone):
                neighbor_zone = self.graph.get_zone(neighbor)
                # blocked zones cannot be entered
                if (
                    not neighbor_zone
                    or neighbor_zone.zone_type == "blocked"
                ):
                    continue

                cost = self.graph.get_move_cost(neighbor)
                if cost <= 0:
                    continue

                arrival_turn = curr_turn + cost
                if arrival_turn > self.max_search_turns:
                    continue

                # check connection capacity for all transit turns
                link_ok = True
                for t in range(curr_turn, arrival_turn):
                    if not self._link_is_free(curr_zone, neighbor, t):
                        link_ok = False
                        break

                # move if connection is free and destination has space
                if link_ok and self._zone_is_free(neighbor, arrival_turn):
                    move_state = (arrival_turn, neighbor)
                    if move_state not in visited:
                        # bonus priority score if entering a priority zone
                        p_bonus = (
                            1 if neighbor_zone.zone_type == "priority" else 0
                        )
                        new_p = priority_score + p_bonus
                        move_cost = (arrival_turn, -new_p)

                        # only update and push if this is a better path
                        if move_cost < best_cost.get(move_state, (10**9, 0)):
                            best_cost[move_state] = move_cost
                            came_from[move_state] = state
                            heapq.heappush(
                                pq, (arrival_turn, -new_p, neighbor)
                            )

        return []

    def _reserve_path(self, path: list[tuple[int, str]]) -> None:
        """Marks all zones and links used by a path as booked.

        Args:
            path: The planned route for a drone.
        """
        for j in range(len(path) - 1):
            t_from, z_from = path[j]
            t_to, z_to = path[j + 1]

            # book destination zone at arrival turn
            self.zone_reservations[t_to][z_to] += 1

            # if drone moved, book connection for all transit turns
            if z_from != z_to:
                link_key = frozenset({z_from, z_to})
                for t in range(t_from, t_to):
                    self.link_reservations[t][link_key] += 1

    def solve(self) -> list[list[tuple[int, str]]]:
        """Plans collision-free paths for all drones, one at a time.

        Returns:
            List of paths, one per drone.
        """
        all_paths: list[list[tuple[int, str]]] = []

        for i in range(self.nb_drones):
            # stagger start turns (i // 2) to reduce congestion at start
            start_turn = i // 2
            path = self._find_path(start_turn)

            if not path:
                print(
                    f"  warning: drone D{i + 1} could not find path to goal!"
                )
            else:
                self._reserve_path(path)

            all_paths.append(path)

        return all_paths

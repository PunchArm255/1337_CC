# pathfinder.py - finds the shortest path for each drone using dijkstra
import heapq
from collections import defaultdict
from graph import Graph


class Pathfinder:
    """plans collision-free paths for all drones using dijkstra."""

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

    def _zone_is_free(self, zone_name: str, turn: int) -> bool:
        """checks if a zone has capacity for another drone at this turn."""
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
        """checks if a connection has available capacity at this turn."""
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
        """rebuilds the full path from start to goal by following came_from."""
        path: list[tuple[int, str]] = []
        current = end_state
        while current in came_from:
            path.append(current)
            current = came_from[current]
        path.append(start_state)
        path.reverse()
        return path

    def _find_path(self, start_turn: int) -> list[tuple[int, str]]:
        """runs time-expanded dijkstra for one drone."""
        start = self.graph.start_zone.name
        end = self.graph.end_zone.name

        # priority queue (min-heap): lowest turn popped first
        pq: list[tuple[int, str]] = [(start_turn, start)]
        visited: set[tuple[int, str]] = set()
        came_from: dict[tuple[int, str], tuple[int, str]] = {}

        while pq:
            curr_turn, curr_zone = heapq.heappop(pq)
            state = (curr_turn, curr_zone)

            # goal reached: reconstruct and return path
            if curr_zone == end:
                return self._trace_path(
                    state, (start_turn, start), came_from
                )

            if state in visited:
                continue
            visited.add(state)

            # option 1: wait in place for one turn
            wait_turn = curr_turn + 1
            if self._zone_is_free(curr_zone, wait_turn):
                wait_state = (wait_turn, curr_zone)
                if wait_state not in visited:
                    came_from[wait_state] = state
                    heapq.heappush(pq, wait_state)

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
                        came_from[move_state] = state
                        heapq.heappush(pq, move_state)

        return []

    def _reserve_path(self, path: list[tuple[int, str]]) -> None:
        """marks all zones and links used by a path as booked."""
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
        """plans paths for all drones, one at a time."""
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

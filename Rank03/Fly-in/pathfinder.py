# pathfinder.py — finds the shortest path for each drone using dijkstra
#
# === what this file does ===
# for each drone, we run dijkstra's algorithm to find the cheapest
# (fewest turns) path from start to goal. but there's a twist: we
# also need to make sure drones don't collide with each other.
#
# we solve this by planning drones one at a time and "reserving" each
# drone's path before planning the next one. this way, drone #2 knows
# where drone #1 will be and routes around it.
#
# === what is dijkstra's algorithm? ===
# imagine you're at a train station and want the cheapest route to
# another city. you look at all the direct trains from your station,
# pick the cheapest one, go there, then repeat. you always expand
# the cheapest option first. that's dijkstra in a nutshell.
#
# technically:
#   1. put the start node in a priority queue with cost 0
#   2. pop the cheapest node from the queue
#   3. if it's the goal, we're done — trace back the path
#   4. otherwise, look at all its neighbors, calculate the cost
#      to reach each one, and add them to the queue
#   5. repeat from step 2
#
# the priority queue ensures we always expand the cheapest option first,
# which guarantees we find the optimal path.
#
# === what makes this "time-expanded" dijkstra? ===
# in normal dijkstra, a state is just "which zone am i at?"
# in our version, a state is "which zone am i at, AND what turn is it?"
#
# so (turn=3, zone="roof1") and (turn=5, zone="roof1") are DIFFERENT states.
# this lets us check: "is roof1 occupied at turn 3?" separately from
# "is roof1 occupied at turn 5?"
#
# without the time dimension, we couldn't coordinate multiple drones.
#
# === reservation tables ===
# after finding a path for drone #1, we "book" every zone and connection
# it will use at every turn. when planning drone #2, we check these
# tables to avoid conflicts. it's like booking seats on a train.
#
# ref: https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
# ref: https://docs.python.org/3/library/heapq.html (min-heap / priority queue)
# ref: https://en.wikipedia.org/wiki/Multi-agent_pathfinding

import heapq
from collections import defaultdict
from graph import Graph


class Pathfinder:
    """plans collision-free paths for all drones using time-expanded dijkstra."""

    def __init__(self, graph: Graph, nb_drones: int) -> None:
        self.graph = graph
        self.nb_drones = nb_drones

        # --- reservation tables ---
        # these track which zones and connections are "booked" at each turn.
        # as we solve paths for drones one by one, we fill these tables so
        # that future drones know what's already taken.

        # zone_reservations[turn][zone_name] = how many drones are booked here
        # defaultdict(lambda: defaultdict(int)) means:
        #   - accessing a new turn auto-creates an empty dict
        #   - accessing a new zone in that dict auto-creates 0
        self.zone_reservations: dict[int, dict[str, int]] = defaultdict(
            lambda: defaultdict(int)
        )

        # link_reservations[turn][frozenset({zone1, zone2})] = how many drones
        # are booked on this connection at this turn
        self.link_reservations: dict[int, dict[frozenset[str], int]] = defaultdict(
            lambda: defaultdict(int)
        )

    # -------------------------------------------------------------------------
    # availability checks — used during pathfinding to see if a move is legal
    # -------------------------------------------------------------------------

    def _zone_is_free(self, zone_name: str, turn: int) -> bool:
        """can a drone occupy this zone at this turn?

        start and end zones have unlimited capacity (all drones begin/end there).
        for everything else, check if current bookings are below the zone's limit.
        """
        # start and end are special — unlimited capacity per subject rules
        if zone_name in (self.graph.start_zone.name, self.graph.end_zone.name):
            return True
        zone = self.graph.get_zone(zone_name)
        booked = self.zone_reservations[turn][zone_name]
        return booked < zone.max_drones

    def _link_is_free(self, z1: str, z2: str, turn: int) -> bool:
        """can a drone traverse the connection between z1 and z2 at this turn?

        if z1 == z2, the drone is waiting in place (no connection used).
        otherwise, check if the connection's capacity hasn't been reached.
        """
        if z1 == z2:
            return True  # waiting in place doesn't use any connection
        conn = self.graph.get_connection(z1, z2)
        link_key = frozenset({z1, z2})
        booked = self.link_reservations[turn][link_key]
        return booked < conn.max_link_capacity

    # -------------------------------------------------------------------------
    # path reconstruction — traces back from goal to start using breadcrumbs
    # -------------------------------------------------------------------------

    def _trace_path(
        self,
        end_state: tuple[int, str],
        start_state: tuple[int, str],
        came_from: dict[tuple[int, str], tuple[int, str]]
    ) -> list[tuple[int, str]]:
        """rebuilds the full path by following the came_from breadcrumbs.

        came_from maps each state to the state we came from.
        we start at the goal and walk backwards to the start.
        then reverse to get the path in the right order.
        """
        path: list[tuple[int, str]] = []
        current = end_state
        while current in came_from:
            path.append(current)
            current = came_from[current]
        path.append(start_state)
        path.reverse()
        return path

    # -------------------------------------------------------------------------
    # the core algorithm — dijkstra for a single drone
    # -------------------------------------------------------------------------

    def _find_path(self, start_turn: int) -> list[tuple[int, str]]:
        """runs time-expanded dijkstra for one drone.

        each state in our search is (turn_number, zone_name).
        the priority queue always pops the state with the lowest
        turn number first — this is what makes dijkstra work.

        returns a list of (turn, zone) pairs representing the path,
        or an empty list if no path exists.
        """
        start = self.graph.start_zone.name
        end = self.graph.end_zone.name

        # the priority queue (min-heap). python's heapq sorts by the first
        # element of the tuple, which is the turn number. so the state with
        # the lowest turn always gets popped first — exactly what dijkstra needs.
        # each entry is (turn, zone_name).
        pq: list[tuple[int, str]] = [(start_turn, start)]

        # visited set — once we've processed a (turn, zone) state, we don't
        # need to process it again. dijkstra guarantees that the first time
        # we pop a state, we've found the cheapest way to reach it.
        visited: set[tuple[int, str]] = set()

        # breadcrumb trail — for each state, remembers which state we came from.
        # used to reconstruct the full path once we reach the goal.
        came_from: dict[tuple[int, str], tuple[int, str]] = {}

        while pq:
            # pop the state with the lowest turn number (cheapest to reach)
            curr_turn, curr_zone = heapq.heappop(pq)
            state = (curr_turn, curr_zone)

            # === goal check ===
            # if we've reached the end zone, reconstruct and return the path
            if curr_zone == end:
                return self._trace_path(state, (start_turn, start), came_from)

            # skip if we've already found a better way to this state
            if state in visited:
                continue
            visited.add(state)

            # === option 1: WAIT in place for one turn ===
            # the drone stays where it is. this costs 1 turn.
            # we only do this if the zone still has capacity next turn
            # (another drone might be booked to arrive here).
            wait_turn = curr_turn + 1
            if self._zone_is_free(curr_zone, wait_turn):
                wait_state = (wait_turn, curr_zone)
                if wait_state not in visited:
                    came_from[wait_state] = state
                    heapq.heappush(pq, wait_state)

            # === option 2: MOVE to a neighboring zone ===
            for neighbor in self.graph.get_neighbours(curr_zone):
                # get the cost to enter this neighbor
                # normal/priority = 1 turn, restricted = 2 turns, blocked = huge
                cost = self.graph.get_move_cost(neighbor)
                arrival_turn = curr_turn + cost

                # for restricted zones (cost=2), the drone is "in transit" on the
                # connection for turns between curr_turn and arrival_turn.
                # we need to make sure the connection has capacity for ALL those turns.
                link_ok = True
                for t in range(curr_turn, arrival_turn):
                    if not self._link_is_free(curr_zone, neighbor, t):
                        link_ok = False
                        break

                # only move if: the connection is free AND the destination has space
                if link_ok and self._zone_is_free(neighbor, arrival_turn):
                    move_state = (arrival_turn, neighbor)
                    if move_state not in visited:
                        came_from[move_state] = state
                        heapq.heappush(pq, move_state)

        # if we get here, there's no valid path to the goal for this drone
        return []

    # -------------------------------------------------------------------------
    # reservation — books a drone's path so future drones route around it
    # -------------------------------------------------------------------------

    def _reserve_path(self, path: list[tuple[int, str]]) -> None:
        """marks all zones and connections used by a path as "booked".

        this is called after finding a path for one drone, before
        planning the next drone. it ensures future drones see these
        reservations and avoid conflicts.
        """
        for j in range(len(path) - 1):
            t_from, z_from = path[j]
            t_to, z_to = path[j + 1]

            # book the destination zone at the arrival turn
            self.zone_reservations[t_to][z_to] += 1

            # if the drone actually moved (not waiting), book the connection
            # for every turn it's in transit
            if z_from != z_to:
                link_key = frozenset({z_from, z_to})
                for t in range(t_from, t_to):
                    self.link_reservations[t][link_key] += 1

    # -------------------------------------------------------------------------
    # main entry point — solve all drones
    # -------------------------------------------------------------------------

    def solve(self) -> list[list[tuple[int, str]]]:
        """plans paths for all drones, one at a time.

        drones are staggered: drone 0 and 1 start at turn 0,
        drones 2 and 3 start at turn 1, etc. this prevents all
        drones from trying to leave through the same gate at turn 0,
        which would cause massive congestion at the start zone's
        limited-capacity neighbors.

        returns a list of paths, one per drone. each path is a list
        of (turn, zone_name) pairs.
        """
        all_paths: list[list[tuple[int, str]]] = []

        for i in range(self.nb_drones):
            # stagger start turns to reduce congestion
            # i // 2 means: drone 0,1 -> turn 0, drone 2,3 -> turn 1, etc.
            start_turn = i // 2
            path = self._find_path(start_turn)

            if not path:
                print(f"  warning: drone D{i + 1} could not find a path to goal!")
            else:
                # book this path so the next drone avoids it
                self._reserve_path(path)

            all_paths.append(path)

        return all_paths
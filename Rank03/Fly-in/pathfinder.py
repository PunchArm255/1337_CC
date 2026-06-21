import heapq
from collections import defaultdict
from graph import Graph

class Pathfinder:
    def __init__(self, graph: Graph, nb_drones: int):
        self.graph = graph
        self.nb_drones = nb_drones
        
        # Reservation Tables
        # self.zone_res[turn_number][zone_name] = number_of_drones_booked
        self.zone_res: dict[int, dict[str, int]] = defaultdict(lambda: defaultdict(int))
        # self.link_res[turn_number][frozenset_connection] = number_of_drones_booked
        self.link_res: dict[int, dict[frozenset[str], int]] = defaultdict(lambda: defaultdict(int))

    def _is_zone_available(self, zone_name: str, turn: int) -> bool:
        """Checks if a zone has space at a specific turn."""
        if zone_name in (self.graph.start_zone.name, self.graph.end_zone.name):
            return True # Start and End hubs can hold infinite drones
        zone = self.graph.get_zone(zone_name)
        return self.zone_res[turn][zone_name] < zone.max_drones

    def _is_link_available(self, z1: str, z2: str, turn: int) -> bool:
        """Checks if a connection has space at a specific turn."""
        if z1 == z2: 
            return True # Waiting in place uses no connection
        conn = self.graph.get_connection(z1, z2)
        link_key = frozenset({z1, z2})
        return self.link_res[turn][link_key] < conn.max_link_capacity

    def _find_path_for_one_drone(self, start_turn: int) -> list[tuple[int, str]]:
        """Finds a path factoring in time and reservations."""
        start = self.graph.start_zone.name
        end = self.graph.end_zone.name

        # Priority Queue state: (current_turn, current_zone)
        pq: list[tuple[int, str]] = [(start_turn, start)]
        
        visited = set()
        previous_state = {}

        while pq:
            curr_turn, curr_zone = heapq.heappop(pq)
            state = (curr_turn, curr_zone)

            if curr_zone == end:
                # Path found! Reconstruct it backwards.
                path = []
                curr = state
                while curr in previous_state:
                    path.append(curr)
                    curr = previous_state[curr]
                path.append((start_turn, start))
                path.reverse()
                return path

            if state in visited:
                continue
            visited.add(state)

            # Option 1: WAIT in place for 1 turn (if the zone isn't kicked out by max capacity)
            if self._is_zone_available(curr_zone, curr_turn + 1):
                new_state = (curr_turn + 1, curr_zone)
                if new_state not in visited:
                    previous_state[new_state] = state
                    heapq.heappush(pq, new_state)

            # Option 2: MOVE to a neighbor
            for neighbor in self.graph.get_neighbours(curr_zone):
                cost = self.graph.get_move_cost(neighbor)
                arrival_turn = curr_turn + cost

                # Check if the connection link is free for the whole transit time
                link_ok = True
                for t in range(curr_turn, arrival_turn):
                    if not self._is_link_available(curr_zone, neighbor, t):
                        link_ok = False
                        break
                
                # If link is free AND destination zone has space when we arrive
                if link_ok and self._is_zone_available(neighbor, arrival_turn):
                    new_state = (arrival_turn, neighbor)
                    if new_state not in visited:
                        previous_state[new_state] = state
                        heapq.heappush(pq, new_state)
        
        return [] # Impossible to reach

    def solve(self) -> list[list[tuple[int, str]]]:
        """Runs Dijkstra for all drones and books their paths."""
        all_paths = []
        for i in range(self.nb_drones):
            # We offset the start turn slightly to avoid them all trying to leave at T=0
            path = self._find_path_for_one_drone(start_turn=i // 2) 
            
            # Book the path in our reservation tables!
            for j in range(len(path) - 1):
                t1, z1 = path[j]
                t2, z2 = path[j+1]
                
                self.zone_res[t2][z2] += 1
                if z1 != z2:
                    link_key = frozenset({z1, z2})
                    for t in range(t1, t2):
                        self.link_res[t][link_key] += 1
                        
            all_paths.append(path)
        return all_paths
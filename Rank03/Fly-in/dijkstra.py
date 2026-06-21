import heapq
from graph import Graph

class Pathfinder:
    def __init__(self, graph: Graph):
        self.graph = graph

    def find_basic_path(self) -> list[str]:
        """
        Layer 1: Standard Dijkstra for ONE drone.
        Ignores capacities and collisions. Just finds the fastest route.
        """
        start = self.graph.start_zone.name
        end = self.graph.end_zone.name

        # 1. The Priority Queue. We store tuples of (total_cost, current_zone)
        # It starts with 0 cost at the start_hub.
        pq: list[tuple[int, str]] = [(0, start)]

        # 2. Tracking the shortest known distance to every zone.
        # We initialize everything to infinity, except the start zone which is 0.
        distances: dict[str, int] = {zone: float('inf') for zone in self.graph.zones}
        distances[start] = 0

        # 3. Tracking where we came from so we can rebuild the path at the end.
        # previous_zone["roof1"] = "hub" means we reached roof1 from hub.
        previous_zone: dict[str, str | None] = {zone: None for zone in self.graph.zones}

        # --- THE DIJKSTRA LOOP ---
        while pq:
            # Pop the zone with the lowest total_cost
            current_cost, current_zone = heapq.heappop(pq)

            # If we reached the goal, we can stop searching!
            if current_zone == end:
                break

            # If we somehow pulled an old, worse path from the queue, skip it.
            if current_cost > distances[current_zone]:
                continue

            # Look at all neighbors of our current zone
            for neighbor in self.graph.get_neighbours(current_zone):
                # How much does it cost to enter this neighbor? (1 for normal, 2 for restricted)
                move_cost = self.graph.get_move_cost(neighbor)
                
                # The new total cost if we take this path
                new_total_cost = current_cost + move_cost

                # If we found a strictly better (cheaper) path to this neighbor...
                if new_total_cost < distances[neighbor]:
                    distances[neighbor] = new_total_cost       # Update the shortest distance
                    previous_zone[neighbor] = current_zone     # Remember how we got here
                    
                    # Push this new state into our priority queue
                    heapq.heappush(pq, (new_total_cost, neighbor))

        # --- PATH RECONSTRUCTION ---
        # We start at the end zone and walk backwards using our previous_zone dictionary.
        path: list[str] = []
        current = end
        
        while current is not None:
            path.append(current)
            current = previous_zone[current]

        # The path is backwards (goal -> roof2 -> roof1 -> hub). Reverse it!
        path.reverse()

        # If the start zone isn't the first item, it means no valid path was found.
        if path[0] != start:
            return []

        return path

# --- TESTER ---
if __name__ == "__main__":
    from parser import map_parser
    
    parsed_map = map_parser("map.txt")
    g = Graph(parsed_map)
    pf = Pathfinder(g)
    
    shortest_path = pf.find_basic_path()
    print(f"Shortest path for 1 drone: {shortest_path}")
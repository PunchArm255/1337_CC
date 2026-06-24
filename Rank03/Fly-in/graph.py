# graph.py — turns the flat MapStructure into something we can navigate
#
# the parser gives us a list of zones and a list of connections.
# that's fine for storage, but for pathfinding we need fast lookups:
#   - "what zones are connected to zone X?" (adjacency list)
#   - "what's the connection object between zone A and zone B?" (connection map)
#
# this class builds both of those structures from the raw parsed data.
#
# ref: https://en.wikipedia.org/wiki/Adjacency_list
# ref: https://www.geeksforgeeks.org/graph-and-its-representations/

from data import Zone, Connection, MapStructure


class Graph:
    """graph representation of the drone network.

    builds an adjacency list and a connection lookup table from the
    parsed map. the adjacency list tells us which zones are neighbors,
    and the connection map lets us quickly find a connection's properties
    (like capacity) given two zone names.
    """

    def __init__(self, map_structure: MapStructure) -> None:
        self.zones = map_structure.zones
        self.start_zone = map_structure.start_hub
        self.end_zone = map_structure.end_hub

        # connection lookup: frozenset({zone1, zone2}) -> Connection
        # using frozenset because connections are bidirectional:
        # frozenset({"A", "B"}) == frozenset({"B", "A"})
        # so we don't have to worry about which order we pass the names
        self.connections: dict[frozenset[str], Connection] = {}

        # adjacency list: zone_name -> [list of neighbor zone names]
        # this is the classic graph representation for traversal.
        # we initialize it with all zone names so even isolated zones
        # (no connections) still have an empty list, avoiding KeyErrors.
        self.adjacency: dict[str, list[str]] = {
            z_name: [] for z_name in self.zones
        }

        # build both structures from the connection list
        for cnx in map_structure.connections:
            # store the connection object keyed by the zone pair
            k = frozenset({cnx.zone1, cnx.zone2})
            self.connections[k] = cnx
            # add each zone as a neighbor of the other (bidirectional)
            self.adjacency[cnx.zone1].append(cnx.zone2)
            self.adjacency[cnx.zone2].append(cnx.zone1)

    def get_neighbours(self, z_name: str) -> list[str]:
        """returns all zones directly connected to the given zone."""
        return self.adjacency.get(z_name, [])

    def get_connection(self, z_name1: str, z_name2: str) -> Connection | None:
        """looks up the connection between two zones, order doesn't matter."""
        k = frozenset({z_name1, z_name2})
        return self.connections.get(k)

    def get_zone(self, z_name: str) -> Zone | None:
        """looks up a zone by name, returns None if not found."""
        return self.zones.get(z_name)

    def get_move_cost(self, dest_name: str) -> int:
        """returns the movement cost to enter a zone based on its type.

        - normal / priority: 1 turn (priority just gets preferred in pathfinding)
        - restricted: 2 turns (drone spends an extra turn "in transit")
        - blocked: effectively infinite (999999), so dijkstra never picks it
        """
        zone = self.get_zone(dest_name)
        if not zone or zone.zone_type == "blocked":
            return 999999
        if zone.zone_type == "restricted":
            return 2
        return 1
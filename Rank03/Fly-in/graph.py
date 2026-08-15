# graph.py - graph structure for zones and connections
from data import Zone, Connection, MapStructure


class Graph:
    """graph representation of the drone network."""

    def __init__(self, map_structure: MapStructure) -> None:
        if (
            map_structure.start_hub is None
            or map_structure.end_hub is None
        ):
            raise ValueError("map must have valid start and end hubs.")

        self.zones: dict[str, Zone] = map_structure.zones
        self.start_zone: Zone = map_structure.start_hub
        self.end_zone: Zone = map_structure.end_hub

        # connection lookup: frozenset({A, B}) -> connection
        # using frozenset because connections are bidirectional:
        # frozenset({"A", "B"}) == frozenset({"B", "A"})
        self.connections: dict[frozenset[str], Connection] = {}

        # adjacency list: zone_name -> list of neighbor names
        self.adjacency: dict[str, list[str]] = {
            z_name: [] for z_name in self.zones
        }

        # build adjacency list and connection lookup
        for cnx in map_structure.connections:
            k = frozenset({cnx.zone1, cnx.zone2})
            self.connections[k] = cnx
            self.adjacency[cnx.zone1].append(cnx.zone2)
            self.adjacency[cnx.zone2].append(cnx.zone1)

    def get_neighbours(self, z_name: str) -> list[str]:
        """returns all neighboring zones for a given zone."""
        return self.adjacency.get(z_name, [])

    def get_connection(
        self, z_name1: str, z_name2: str
    ) -> Connection | None:
        """looks up the connection object between two zones."""
        k = frozenset({z_name1, z_name2})
        return self.connections.get(k)

    def get_zone(self, z_name: str) -> Zone | None:
        """returns zone object if it exists, else None."""
        return self.zones.get(z_name)

    def get_move_cost(self, dest_name: str) -> int:
        """returns turn cost to enter a zone."""
        zone = self.get_zone(dest_name)
        # blocked zones cannot be entered
        if not zone or zone.zone_type == "blocked":
            return 0
        # restricted zones take 2 turns to enter
        if zone.zone_type == "restricted":
            return 2
        # normal and priority zones cost 1 turn
        return 1

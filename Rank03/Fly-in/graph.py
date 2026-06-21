from data import Zone, Connection, MapStructure

class Graph:
    def __init__(self, map_structure: MapStructure) -> None:
        self.zones = map_structure.zones
        self.start_zone = map_structure.start_hub
        self.end_zone = map_structure.end_hub

        self.connections = {}
        self.adjacency = {z_name: [] for z_name in self.zones}
    
        for cnx in map_structure.connections:
            k = frozenset({cnx.zone1, cnx.zone2})
            self.connections[k] = cnx
            self.adjacency[cnx.zone1].append(cnx.zone2)
            self.adjacency[cnx.zone2].append(cnx.zone1)

    def get_neighbours(self, z_name: str) -> list[str]:
        return self.adjacency.get(z_name, [])

    def get_connection(self, z_name1: str, z_name2: str) -> Connection | None:
        k = frozenset({z_name1, z_name2})
        return self.connections.get(k)
    
    def get_zone(self, z_name: str) -> Zone | None:
        return self.zones.get(z_name)
    
    def get_move_cost(self, dest_name: str) -> int:
        zone = self.get_zone(dest_name)
        if not zone or zone.zone_type == "blocked":
            return 999999
        if zone.zone_type == "restricted":
            return 2
        return 1
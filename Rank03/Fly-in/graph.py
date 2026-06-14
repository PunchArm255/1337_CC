from data import Zone, Connection, MapStructure

class Graph:

    def __init__(self, map_structure: MapStructure) -> None:
        # self.map_structure = map_structure
        self.zones = map_structure.zones
        self.start_zone = map_structure.start_hub
        self.end_zone = map_structure.end_hub
        self.connections = {}

        for connection in map_structure.connections:
            k = frozenset({connection.zone1, connection.zone2})
            self.connections[k] = connection

        self.adjacency = {}

        for z_name in self.zones:
            self.adjacency[z_name] = []

        for connection in map_structure.connections:
            self.adjacency[connection.zone1].append(connection.zone2)
            self.adjacency[connection.zone2].append(connection.zone1)

    def get_neighbours(self, z_name: str) -> list[Zone]:
        return self.adjacency.get(z_name, [])

    def get_connection(self, z_name1, z_name2) -> Connection:
        k = frozenset({z_name1, z_name2})
        return self.connections.get(k, None)

    def get_zone(self, z_name) -> Zone:
        return self.zones.get(z_name, None)


if  __name__ == "__main__":

    from parser import map_parser
    
    g = Graph(map_parser("map.txt"))

    print(f"Adjacent Zones: {g.adjacency}")
    print(f"Neighbours of ROOF1: {g.get_neighbours("roof1")}")
    print(f"{g.get_connection("roof1", "roof2")}")

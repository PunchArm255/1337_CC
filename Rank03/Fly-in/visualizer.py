import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from graph import Graph


class Visualiser:

    def __init__(self, graph: Graph) -> None:
        self.graph = graph
        self.fig, self.axe = plt.subplots(figsize=(10, 8))

    def draw_static(self):
        for connection in self.graph.connections.values():
            zone1 = self.graph.get_zone(connection.zone1)
            zone2 = self.graph.get_zone(connection.zone2)
            self.axe.plot([zone1.x, zone2.x], [zone1.y, zone2.y], color="gray", zorder=1)

        for z_name in self.graph.zones:
            pass


if __name__ == "__main__":

    from parser import map_parser
    
    g = Graph(map_parser("map.txt"))

    viz = Visualiser(g)

    viz.draw_static()
    plt.show()

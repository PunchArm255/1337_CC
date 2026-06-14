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

        ZONE_COLORS = {
            "normal": "steelblue",
            "restricted": "orange",
            "priority": "lightgreen",
            "blocked": "dimgray",
        }

        for zone in self.graph.zones.values():

            if zone.color is not None:
                fill_color = zone.color
            else:
                fill_color = ZONE_COLORS[zone.zone_type]
            
            circle = Circle((zone.x, zone.y), radius=0.4, color=fill_color, zorder=2)
            self.axe.add_patch(circle)


if __name__ == "__main__":

    from parser import map_parser
    
    g = Graph(map_parser("map.txt"))

    viz = Visualiser(g)

    viz.draw_static()
    plt.show()

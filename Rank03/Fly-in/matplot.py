import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Patch
from graph import Graph

class Visualiser:
    def __init__(self, graph: Graph) -> None:
        self.graph = graph
        # figsize=(15, 12) defines the width and height of the window in inches.
        self.fig, self.axe = plt.subplots(figsize=(15, 12))
        
        # Set a dark theme background for better contrast
        self.fig.patch.set_facecolor("#1e1e2e")
        self.axe.set_facecolor("#1e1e2e")

    def draw_static(self) -> None:
        # 1. DRAW CONNECTIONS (zorder=1 so they are in the background)
        for connection in self.graph.connections.values():
            zone1 = self.graph.get_zone(connection.zone1)
            zone2 = self.graph.get_zone(connection.zone2)
            
            # self.axe.plot takes a list of X coordinates and a list of Y coordinates
            self.axe.plot(
                [zone1.x, zone2.x], 
                [zone1.y, zone2.y], 
                color="#6c7086", 
                linewidth=2, 
                zorder=1
            )

        # Dictionary defining default colors for zone types
        ZONE_COLORS = {
            "normal": "#89b4fa",     # Blue
            "restricted": "#fab387", # Orange
            "priority": "#a6e3a1",   # Green
            "blocked": "#45475a",    # Dark Gray
        }

        # 2. CREATE LEGEND LABELS
        z_labels = []
        for z_type, color in ZONE_COLORS.items():
            # Patch creates a colored square for the legend
            z_labels.append(Patch(facecolor=color, label=z_type))

        # 3. DRAW ZONES (zorder=2 so they overlap the lines)
        for zone in self.graph.zones.values():
            # If the parser found a color tag, use it. Otherwise, use the default type color.
            fill_color = zone.color if zone.color else ZONE_COLORS[zone.zone_type]
            
            # Draw the main zone circle
            circle = Circle((zone.x, zone.y), radius=0.4, color=fill_color, zorder=2)
            self.axe.add_patch(circle)
            
            # Highlight Start and End zones with thick, hollow outlines
            if zone == self.graph.start_zone:
                # Note: fill=False is a boolean, NOT a string "false"
                start_stroke = Circle((zone.x, zone.y), radius=0.5, fill=False, edgecolor="#a6e3a1", linewidth=3, zorder=3)
                self.axe.add_patch(start_stroke)
                self.axe.text(zone.x, zone.y + 0.6, "START", color="#a6e3a1", ha="center", weight="bold")
                
            if zone == self.graph.end_zone:
                end_stroke = Circle((zone.x, zone.y), radius=0.5, fill=False, edgecolor="#f9e2af", linewidth=3, zorder=3)
                self.axe.add_patch(end_stroke)
                self.axe.text(zone.x, zone.y + 0.6, "END", color="#f9e2af", ha="center", weight="bold")

            # Draw the zone name inside or near the circle
            self.axe.text(zone.x, zone.y, zone.name, color="white", ha="center", va="center", fontsize=9, zorder=4)

        # 4. FINAL CANVAS CONFIGURATIONS
        self.axe.set_aspect("equal") # Ensures circles are perfectly round, not stretched
        self.axe.axis("off")         # Hides the X and Y grid axes
        
        # Add the legend to the top left, with white text
        legend = self.axe.legend(handles=z_labels, loc="upper left")
        for text in legend.get_texts():
            text.set_color("black")


if __name__ == "__main__":
    from parser import map_parser
    g = Graph(map_parser("map.txt"))
    viz = Visualiser(g)
    viz.draw_static()
    
    plt.tight_layout() # Trims excess margins around the plot
    plt.show()         # Renders the window
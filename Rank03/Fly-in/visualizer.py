import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import pygame
import sys
from graph import Graph
from data import Zone
from parser import ParsingError

class Visualizer:
    def __init__(self, graph: Graph):
        self.graph = graph
        
        pygame.init()
        pygame.font.init()
        
        self.WIDTH, self.HEIGHT = 1200, 1200
        # 1. Added pygame.RESIZABLE flag to allow dynamic window scaling
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Fly-in: Drone Routing Simulation")
        
        # Fonts
        self.font_large = pygame.font.SysFont("Arial", 20, bold=True)
        self.font_small = pygame.font.SysFont("Arial", 14, bold=True)
        
        # 2. Refactored to use elegant HEX codes instead of RGB tuples
        self.COLORS = {
            "bg": "#1E1E2E",           # Dark base
            "line": "#6C7086",         # Subtle gray
            "text": "#FFFFFF",         # White
            "normal": "#89B4FA",       # Blue
            "restricted": "#FAB387",   # Orange
            "priority": "#A6E3A1",     # Green
            "blocked": "#45475A",      # Dark gray
            "start_stroke": "#A6E3A1", # Bright green outline
            "end_stroke": "#F9E2AF"    # Gold outline
        }

        # Calculate initial scale
        self.scale, self.offset_x, self.offset_y, self.max_y = self._calculate_scale()

    def _calculate_scale(self) -> tuple[float, float, float, int]:
        """Calculates scaling to fit the map perfectly on the current screen size."""
        if not self.graph.zones:
            return 1.0, 0.0, 0.0, 0

        xs = [z.x for z in self.graph.zones.values()]
        ys = [z.y for z in self.graph.zones.values()]
        
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        
        map_width = max(max_x - min_x, 1)
        map_height = max(max_y - min_y, 1)

        usable_width = self.WIDTH * 0.8
        usable_height = self.HEIGHT * 0.8

        scale = min(usable_width / map_width, usable_height / map_height)

        offset_x = (self.WIDTH / 2) - ((map_width * scale) / 2) - (min_x * scale)
        offset_y = (self.HEIGHT / 2) - ((map_height * scale) / 2) - (min_y * scale)

        return scale, offset_x, offset_y, max_y

    def _get_pixel_coords(self, zone: Zone) -> tuple[int, int]:
        """Converts logical coordinates to screen pixels and inverts the Y axis."""
        px = int(zone.x * self.scale + self.offset_x)
        py = int((self.max_y - zone.y) * self.scale + self.offset_y)
        return px, py

    def _get_fill_color(self, zone: Zone) -> str:
        """Gets the fill color: Custom if defined in map, else default type color."""
        if zone.color:
            return zone.color
        return self.COLORS.get(zone.zone_type, self.COLORS["normal"])

    def _draw_legend(self):
        legend_items = [
            ("Normal", self.COLORS["normal"]),
            ("Restricted", self.COLORS["restricted"]),
            ("Priority", self.COLORS["priority"]),
            ("Blocked", self.COLORS["blocked"])
        ]
        
        start_x, start_y = 20, 20
        for name, color in legend_items:
            pygame.draw.circle(self.screen, color, (start_x + 10, start_y + 10), 8)
            text_surf = self.font_small.render(name, True, self.COLORS["text"])
            self.screen.blit(text_surf, (start_x + 25, start_y + 2))
            start_y += 25

    def _draw_static_map(self):
        self.screen.fill(self.COLORS["bg"])

        # 1. Draw Connections
        for connection in self.graph.connections.values():
            z1 = self.graph.get_zone(connection.zone1)
            z2 = self.graph.get_zone(connection.zone2)
            
            p1 = self._get_pixel_coords(z1)
            p2 = self._get_pixel_coords(z2)
            pygame.draw.line(self.screen, self.COLORS["line"], p1, p2, 4)

        # 2. Draw Zones
        for zone in self.graph.zones.values():
            pos = self._get_pixel_coords(zone)
            radius = 20
            
            # --- FILL CIRCLE ---
            fill_color = self._get_fill_color(zone)
            try:
                pygame.draw.circle(self.screen, fill_color, pos, radius)
            except ValueError:
                # Fallback just in case parser accepted a bad color string
                pygame.draw.circle(self.screen, self.COLORS["normal"], pos, radius)

            # --- BORDER CIRCLE (Type Indicator) ---
            if zone == self.graph.start_zone:
                border_color = self.COLORS["start_stroke"]
            elif zone == self.graph.end_zone:
                border_color = self.COLORS["end_stroke"]
            else:
                border_color = self.COLORS.get(zone.zone_type, self.COLORS["normal"])
                
            # radius + 4 makes the outline slightly larger than the filled circle
            # width = 3 means "draw only the edge", giving us a perfect border!
            pygame.draw.circle(self.screen, border_color, pos, radius + 4, 3)

            # --- TEXT RENDER (Above the circle) ---
            # If start or end zone, use large font and border color. Else, small white.
            if zone == self.graph.start_zone or zone == self.graph.end_zone:
                text_color = border_color
                font_to_use = self.font_large
            else:
                text_color = self.COLORS["text"]
                font_to_use = self.font_small

            name_text = font_to_use.render(zone.name, True, text_color)
            # pos[1] - radius - 18 pushes the text exactly above the top border
            name_rect = name_text.get_rect(center=(pos[0], pos[1] - radius - 18))
            self.screen.blit(name_text, name_rect)

        self._draw_legend()

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                
                # --- THE RESIZE FIX ---
                elif event.type == pygame.VIDEORESIZE:
                    # 1. Update our internal width and height
                    self.WIDTH, self.HEIGHT = event.w, event.h
                    
                    # 2. DO NOT call set_mode() here! It drops the mouse drag.
                    # Instead, we just grab the new surface the OS created for us.
                    self.screen = pygame.display.get_surface()
                    
                    # 3. Recalculate the map scale so it stays perfectly centered!
                    self.scale, self.offset_x, self.offset_y, self.max_y = self._calculate_scale()

            self._draw_static_map()
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    from parser import map_parser
    try:
        parsed_map = map_parser("map.txt")
        g = Graph(parsed_map)
        viz = Visualizer(g)
        viz.run()
    except ParsingError as e:
        print(e)
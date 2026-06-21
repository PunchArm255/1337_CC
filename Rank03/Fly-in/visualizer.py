import pygame
import sys
from graph import Graph
from data import Zone

class Visualizer:
    def __init__(self, graph: Graph):
        self.graph = graph
        
        pygame.init()
        pygame.font.init()
        
        self.WIDTH, self.HEIGHT = 1200, 800
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Fly-in: Drone Routing Simulation")
        
        # 1. Fonts reduced slightly to maintain crispness
        self.font_large = pygame.font.SysFont("Arial", 26, bold=True)
        self.font_small = pygame.font.SysFont("Arial", 16, bold=True)
        self.font_ui = pygame.font.SysFont("Arial", 14, bold=True)
        
        self.COLORS = {
            "bg": "#1E1E2E",
            "line": "#6C7086",
            "text": "#FFFFFF",
            "normal": "#89B4FA",
            "restricted": "#FAB387",
            "priority": "#A6E3A1",
            "blocked": "#45475A",
            "start_stroke": "#A6E3A1",
            "end_stroke": "#F9E2AF",
            "panel_bg": (30, 30, 46, 210) # 210 = semi-transparent alpha channel!
        }

        self.scale, self.offset_x, self.offset_y, self.max_y = self._calculate_scale()

    def _calculate_scale(self) -> tuple[float, float, float, int]:
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
        px = int(zone.x * self.scale + self.offset_x)
        py = int((self.max_y - zone.y) * self.scale + self.offset_y)
        return px, py

    def _get_fill_color(self, zone: Zone) -> str:
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
        
        start_x, start_y = 30, 30
        for name, color in legend_items:
            pygame.draw.circle(self.screen, color, (start_x + 12, start_y + 12), 10)
            text_surf = self.font_small.render(name, True, self.COLORS["text"])
            self.screen.blit(text_surf, (start_x + 35, start_y + 2))
            start_y += 30

    def draw_ui(self, current_turn: int, max_turns: int):
        """Draws the transparent control panel and turn counter."""
        panel_width, panel_height = 240, 100
        pos_x = self.WIDTH - panel_width - 30
        pos_y = 30

        # Create a surface with SRCALPHA so we can have transparency
        panel = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        panel.fill(self.COLORS["panel_bg"])
        
        # Add a sleek border around the panel
        pygame.draw.rect(panel, self.COLORS["line"], panel.get_rect(), 2, border_radius=8)
        self.screen.blit(panel, (pos_x, pos_y))

        # Render Turn Counter
        turn_str = f"TURN: {current_turn} / {max_turns}"
        turn_color = self.COLORS["start_stroke"] if current_turn == max_turns else self.COLORS["text"]
        turn_text = self.font_large.render(turn_str, True, turn_color)
        self.screen.blit(turn_text, (pos_x + 20, pos_y + 15))

        # Render Controls Guide
        ctrl1 = self.font_ui.render("[SPACE] Advance Turn", True, self.COLORS["text"])
        ctrl2 = self.font_ui.render("[ESC] Exit Simulation", True, self.COLORS["text"])
        self.screen.blit(ctrl1, (pos_x + 20, pos_y + 55))
        self.screen.blit(ctrl2, (pos_x + 20, pos_y + 75))

    def _draw_static_map(self):
        self.screen.fill(self.COLORS["bg"])

        # Lines scaled down to 4
        for connection in self.graph.connections.values():
            z1 = self.graph.get_zone(connection.zone1)
            z2 = self.graph.get_zone(connection.zone2)
            pygame.draw.line(self.screen, self.COLORS["line"], self._get_pixel_coords(z1), self._get_pixel_coords(z2), 4)

        # Zones scaled back to 30 radius
        for zone in self.graph.zones.values():
            pos = self._get_pixel_coords(zone)
            radius = 30
            
            fill_color = self._get_fill_color(zone)
            try:
                pygame.draw.circle(self.screen, fill_color, pos, radius)
            except ValueError:
                pygame.draw.circle(self.screen, self.COLORS["normal"], pos, radius)

            if zone == self.graph.start_zone:
                border_color = self.COLORS["start_stroke"]
            elif zone == self.graph.end_zone:
                border_color = self.COLORS["end_stroke"]
            else:
                border_color = self.COLORS.get(zone.zone_type, self.COLORS["normal"])
                
            # Border slightly hugging the circle
            pygame.draw.circle(self.screen, border_color, pos, radius + 5, 4)

            # Name Text above circle
            if zone == self.graph.start_zone or zone == self.graph.end_zone:
                text_color = border_color
                font_to_use = self.font_large
            else:
                text_color = self.COLORS["text"]
                font_to_use = self.font_small

            name_text = font_to_use.render(zone.name, True, text_color)
            name_rect = name_text.get_rect(center=(pos[0], pos[1] - radius - 20))
            self.screen.blit(name_text, name_rect)

        self._draw_legend()

    def draw_drone(self, drone_id: str, pos: tuple[float, float]):
        """Scaled down the drone to be sharper and proportionate."""
        x, y = int(pos[0]), int(pos[1])
        size = 15  # Reduced from 20
        
        color_body = "#F38BA8"
        color_arm = "#11111B"
        color_rotor = "#94E2D5"
        color_text = "#FFFFFF"
        
        offset = int(size * 0.7)
        
        pygame.draw.line(self.screen, color_arm, (x - offset, y - offset), (x + offset, y + offset), 3)
        pygame.draw.line(self.screen, color_arm, (x - offset, y + offset), (x + offset, y - offset), 3)
        
        for dx, dy in [(-1, -1), (1, 1), (-1, 1), (1, -1)]:
            rotor_x, rotor_y = x + dx * offset, y + dy * offset
            pygame.draw.circle(self.screen, color_rotor, (rotor_x, rotor_y), int(size * 0.45))
            pygame.draw.circle(self.screen, color_arm, (rotor_x, rotor_y), int(size * 0.45), 1)
            
        pygame.draw.circle(self.screen, color_body, (x, y), int(size * 0.7))
        pygame.draw.circle(self.screen, color_arm, (x, y), int(size * 0.7), 2)
        
        d_text = self.font_ui.render(drone_id, True, color_text)
        text_bg = pygame.Surface(d_text.get_size())
        text_bg.fill(self.COLORS["bg"])
        d_rect = d_text.get_rect(center=(x, y + size + 12))
        
        self.screen.blit(text_bg, d_rect)
        self.screen.blit(d_text, d_rect)
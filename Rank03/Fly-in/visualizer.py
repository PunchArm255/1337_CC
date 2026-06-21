import pygame
from pygame import gfxdraw  # Required for Anti-Aliased shapes
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
        
        self.font_title = pygame.font.SysFont("Arial", 46, bold=True)
        self.font_large = pygame.font.SysFont("Arial", 36, bold=True)
        self.font_small = pygame.font.SysFont("Arial", 20, bold=True)
        
        # 1. UPGRADE: gfxdraw requires actual Pygame Color objects, not hex strings
        self.COLORS = {
            "bg": pygame.Color("#1E1E2E"),
            "line": pygame.Color("#6C7086"),
            "text": pygame.Color("#FFFFFF"),
            "normal": pygame.Color("#89B4FA"),
            "restricted": pygame.Color("#FAB387"),
            "priority": pygame.Color("#A6E3A1"),
            "blocked": pygame.Color("#45475A"),
            "start_stroke": pygame.Color("#A6E3A1"),
            "end_stroke": pygame.Color("#F9E2AF")
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

    def _get_fill_color(self, zone: Zone) -> pygame.Color:
        if zone.color:
            try:
                return pygame.Color(zone.color)
            except ValueError:
                pass
        return self.COLORS.get(zone.zone_type, self.COLORS["normal"])

    # 2. THE ANTI-ALIASING HELPER
    def _draw_aa_circle(self, surface, color, pos, radius, width=0):
        """Draws butter-smooth circles using gfxdraw."""
        x, y = int(pos[0]), int(pos[1])
        if width == 0:
            # Filled circle needs both filled_circle and aacircle to smooth the edges
            gfxdraw.filled_circle(surface, x, y, radius, color)
            gfxdraw.aacircle(surface, x, y, radius, color)
        else:
            # To make a thick outline, we draw multiple concentric anti-aliased rings
            for r in range(radius - width, radius + 1):
                gfxdraw.aacircle(surface, x, y, r, color)

    def _draw_legend(self):
        legend_items = [
            ("Normal", self.COLORS["normal"]),
            ("Restricted", self.COLORS["restricted"]),
            ("Priority", self.COLORS["priority"]),
            ("Blocked", self.COLORS["blocked"])
        ]
        
        start_x, start_y = 40, 40
        for name, color in legend_items:
            self._draw_aa_circle(self.screen, color, (start_x + 15, start_y + 15), 14)
            text_surf = self.font_small.render(name, True, self.COLORS["text"])
            self.screen.blit(text_surf, (start_x + 40, start_y + 2))
            start_y += 40

    def draw_hud(self, current_turn: int, max_turn: int):
        """Draws the Turn Counter and Controls overlay."""
        # --- TURN COUNTER (Top Center) ---
        turn_text = f"TURN: {current_turn} / {max_turn}"
        turn_surf = self.font_title.render(turn_text, True, self.COLORS["text"])
        turn_rect = turn_surf.get_rect(center=(self.WIDTH // 2, 50))
        self.screen.blit(turn_surf, turn_rect)

        # --- CONTROLS (Bottom Right) ---
        controls_text = "[SPACE] Next Turn   |   [R] Restart   |   [ESC] Quit"
        ctrl_surf = self.font_small.render(controls_text, True, self.COLORS["text"])
        ctrl_rect = ctrl_surf.get_rect(bottomright=(self.WIDTH - 40, self.HEIGHT - 30))
        self.screen.blit(ctrl_surf, ctrl_rect)

    def _draw_static_map(self):
        self.screen.fill(self.COLORS["bg"])

        for connection in self.graph.connections.values():
            z1 = self.graph.get_zone(connection.zone1)
            z2 = self.graph.get_zone(connection.zone2)
            
            p1 = self._get_pixel_coords(z1)
            p2 = self._get_pixel_coords(z2)
            pygame.draw.line(self.screen, self.COLORS["line"], p1, p2, 6)

        for zone in self.graph.zones.values():
            pos = self._get_pixel_coords(zone)
            radius = 45 
            
            fill_color = self._get_fill_color(zone)
            self._draw_aa_circle(self.screen, fill_color, pos, radius)

            if zone == self.graph.start_zone:
                border_color = self.COLORS["start_stroke"]
            elif zone == self.graph.end_zone:
                border_color = self.COLORS["end_stroke"]
            else:
                border_color = self.COLORS.get(zone.zone_type, self.COLORS["normal"])
                
            self._draw_aa_circle(self.screen, border_color, pos, radius + 8, width=6)

            if zone == self.graph.start_zone or zone == self.graph.end_zone:
                text_color = border_color
                font_to_use = self.font_large
            else:
                text_color = self.COLORS["text"]
                font_to_use = self.font_small

            name_text = font_to_use.render(zone.name, True, text_color)
            name_rect = name_text.get_rect(center=(pos[0], pos[1] - radius - 26))
            self.screen.blit(name_text, name_rect)

        self._draw_legend()

    def draw_drone(self, drone_id: str, pos: tuple[float, float]):
        x, y = int(pos[0]), int(pos[1])
        size = 20
        
        color_body = pygame.Color("#F38BA8")
        color_arm = pygame.Color("#11111B")
        color_rotor = pygame.Color("#94E2D5")
        
        offset = int(size * 0.7)
        
        # Arms
        pygame.draw.line(self.screen, color_arm, (x - offset, y - offset), (x + offset, y + offset), 4)
        pygame.draw.line(self.screen, color_arm, (x - offset, y + offset), (x + offset, y - offset), 4)
        
        # Rotors
        for dx, dy in [(-1, -1), (1, 1), (-1, 1), (1, -1)]:
            rotor_x, rotor_y = x + dx * offset, y + dy * offset
            self._draw_aa_circle(self.screen, color_rotor, (rotor_x, rotor_y), int(size * 0.45))
            self._draw_aa_circle(self.screen, color_arm, (rotor_x, rotor_y), int(size * 0.45), width=2)
            
        # Chassis
        self._draw_aa_circle(self.screen, color_body, (x, y), int(size * 0.7))
        self._draw_aa_circle(self.screen, color_arm, (x, y), int(size * 0.7), width=2)
        
        d_text = self.font_small.render(drone_id, True, self.COLORS["text"])
        text_bg = pygame.Surface(d_text.get_size())
        text_bg.fill(self.COLORS["bg"])
        d_rect = d_text.get_rect(center=(x, y + size + 15))
        
        self.screen.blit(text_bg, d_rect)
        self.screen.blit(d_text, d_rect)
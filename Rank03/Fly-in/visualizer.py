# visualizer.py - pygame graphical interface for the drone simulation
import os

# silence pygame prompt and enable retina/hidpi resolution
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
os.environ["SDL_VIDEO_ALLOW_HIGHDPI"] = "1"

import pygame  # noqa: E402
from graph import Graph  # noqa: E402
from data import Zone  # noqa: E402

# rgb color palette (catppuccin mocha inspired)
COLOR_BG = (30, 30, 46)
COLOR_LINE = (108, 112, 134)
COLOR_TEXT = (255, 255, 255)
COLOR_NORMAL = (137, 180, 250)
COLOR_RESTRICTED = (250, 179, 135)
COLOR_PRIORITY = (166, 227, 161)
COLOR_BLOCKED = (69, 71, 90)
COLOR_START = (166, 227, 161)
COLOR_END = (249, 226, 175)
COLOR_DRONE_BODY = (243, 139, 168)
COLOR_DRONE_ARM = (17, 17, 27)
COLOR_DRONE_ROTOR = (148, 226, 213)
COLOR_LABEL_BG = (49, 50, 68, 230)
COLOR_PANEL_BG = (30, 30, 46, 210)


class Visualizer:
    """handles pygame rendering for the drone network simulation."""

    def __init__(self, graph: Graph) -> None:
        self.graph = graph

        pygame.init()
        pygame.font.init()

        self.width = 1200
        self.height = 800
        # resizable display window
        self.screen = pygame.display.set_mode(
            (self.width, self.height), pygame.RESIZABLE
        )
        pygame.display.set_caption("Fly-in: Drone Routing Simulation")

        # system fonts for badges and labels
        self.font_turn = pygame.font.SysFont("Arial", 16, bold=True)
        self.font_label = pygame.font.SysFont("Arial", 13, bold=True)
        self.font_small = pygame.font.SysFont("Arial", 11, bold=True)

        # compute map scale and centering offsets
        self.scale, self.offset_x, self.offset_y, self.max_y = (
            self._calculate_layout()
        )

    def _calculate_layout(self) -> tuple[float, float, float, int]:
        """computes scaling and offsets to center the map nicely."""
        if not self.graph.zones:
            return 1.0, 0.0, 0.0, 0

        xs = [z.x for z in self.graph.zones.values()]
        ys = [z.y for z in self.graph.zones.values()]

        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)

        map_w = max(max_x - min_x, 1)
        map_h = max(max_y - min_y, 1)

        # leave ~14% margin around edges
        usable_w = self.width * 0.86
        usable_h = self.height * 0.86

        scale = min(usable_w / map_w, usable_h / map_h)

        # center coordinates in window
        offset_x = (self.width / 2) - ((map_w * scale) / 2) - (min_x * scale)
        offset_y = (self.height / 2) - ((map_h * scale) / 2) - (min_y * scale)

        return scale, offset_x, offset_y, max_y

    def zone_to_pixel(self, zone: Zone) -> tuple[int, int]:
        """converts map coordinates to screen pixels.

        the y-axis is flipped because in map coordinates y goes up,
        while in pygame screen coordinates y goes down (max_y - zone.y).
        """
        px = int(zone.x * self.scale + self.offset_x)
        py = int((self.max_y - zone.y) * self.scale + self.offset_y)
        return px, py

    def recalculate_on_resize(self, new_width: int, new_height: int) -> None:
        """updates display dimensions and recalculates layout on resize."""
        self.width = new_width
        self.height = new_height
        self.screen = pygame.display.set_mode(
            (self.width, self.height), pygame.RESIZABLE
        )
        self.scale, self.offset_x, self.offset_y, self.max_y = (
            self._calculate_layout()
        )

    def _get_zone_type_color(self, zone_type: str) -> tuple[int, int, int]:
        """maps zone type to standard color tuple."""
        if zone_type == "restricted":
            return COLOR_RESTRICTED
        if zone_type == "priority":
            return COLOR_PRIORITY
        if zone_type == "blocked":
            return COLOR_BLOCKED
        return COLOR_NORMAL

    def _get_zone_fill_color(
        self, zone: Zone
    ) -> tuple[int, int, int] | pygame.Color:
        """determines fill color for a zone."""
        # use custom color string if specified in map file
        if zone.color:
            try:
                return pygame.Color(zone.color)
            except ValueError:
                pass
        return self._get_zone_type_color(zone.zone_type)

    def draw_background(self) -> None:
        """draws background, connections, zone nodes, and labels."""
        self.screen.fill(COLOR_BG)

        # 1. draw connection lines behind nodes
        for connection in self.graph.connections.values():
            z1 = self.graph.get_zone(connection.zone1)
            z2 = self.graph.get_zone(connection.zone2)
            if z1 and z2:
                p1 = self.zone_to_pixel(z1)
                p2 = self.zone_to_pixel(z2)
                pygame.draw.line(self.screen, COLOR_LINE, p1, p2, 3)

        # 2. draw zone circles and borders
        radius = 24
        for zone in self.graph.zones.values():
            pos = self.zone_to_pixel(zone)
            fill_color = self._get_zone_fill_color(zone)

            # fill node circle
            pygame.draw.circle(self.screen, fill_color, pos, radius)

            # border ring: start/end hubs get distinct highlighted borders
            if zone == self.graph.start_zone:
                border_color = COLOR_START
            elif zone == self.graph.end_zone:
                border_color = COLOR_END
            else:
                border_color = self._get_zone_type_color(zone.zone_type)

            pygame.draw.circle(self.screen, border_color, pos, radius + 3, 3)

            # text label above zone node
            text_color = (
                border_color
                if zone in (self.graph.start_zone, self.graph.end_zone)
                else COLOR_TEXT
            )
            name_surf = self.font_label.render(zone.name, True, text_color)
            name_rect = name_surf.get_rect(
                center=(pos[0], pos[1] - radius - 14)
            )
            self.screen.blit(name_surf, name_rect)

    def draw_legend(self) -> None:
        """draws a small compact legend in the top-left corner."""
        items: list[tuple[str, tuple[int, int, int]]] = [
            ("Normal", COLOR_NORMAL),
            ("Restricted", COLOR_RESTRICTED),
            ("Priority", COLOR_PRIORITY),
            ("Blocked", COLOR_BLOCKED),
        ]

        x, y = 16, 16
        for name, color in items:
            pygame.draw.circle(self.screen, color, (x + 5, y + 6), 5)
            text_surf = self.font_small.render(name, True, COLOR_TEXT)
            self.screen.blit(text_surf, (x + 16, y))
            y += 18

    def draw_turn_counter(
        self, current_turn: int, max_turns: int, is_finished: bool
    ) -> None:
        """draws a compact turn counter badge in the top-right corner."""
        turn_str = f"Turn: {current_turn} / {max_turns}"
        turn_color = COLOR_START if is_finished else COLOR_TEXT

        text_surf = self.font_turn.render(turn_str, True, turn_color)
        pad_x, pad_y = 12, 6
        badge_w = text_surf.get_width() + pad_x * 2
        badge_h = text_surf.get_height() + pad_y * 2

        pos_x = self.width - badge_w - 16
        pos_y = 16

        # transparent panel with border
        badge = pygame.Surface((badge_w, badge_h), pygame.SRCALPHA)
        badge.fill(COLOR_PANEL_BG)
        pygame.draw.rect(
            badge, COLOR_LINE, badge.get_rect(), 1, border_radius=6
        )
        self.screen.blit(badge, (pos_x, pos_y))
        self.screen.blit(text_surf, (pos_x + pad_x, pos_y + pad_y))

    def draw_drone(self, drone_id: str, pos: tuple[float, float]) -> None:
        """draws a drone sprite at the specified pixel coordinates."""
        x, y = int(pos[0]), int(pos[1])
        size = 12
        offset = int(size * 0.7)

        # cross arms
        pygame.draw.line(
            self.screen,
            COLOR_DRONE_ARM,
            (x - offset, y - offset),
            (x + offset, y + offset),
            2,
        )
        pygame.draw.line(
            self.screen,
            COLOR_DRONE_ARM,
            (x - offset, y + offset),
            (x + offset, y - offset),
            2,
        )

        # rotors at endpoints
        rotor_r = max(int(size * 0.35), 2)
        for dx, dy in [(-1, -1), (1, 1), (-1, 1), (1, -1)]:
            rx, ry = x + dx * offset, y + dy * offset
            pygame.draw.circle(
                self.screen, COLOR_DRONE_ROTOR, (rx, ry), rotor_r
            )

        # central body
        body_r = max(int(size * 0.6), 3)
        pygame.draw.circle(self.screen, COLOR_DRONE_BODY, (x, y), body_r)

        # drone id pill badge centered below sprite
        label = self.font_small.render(drone_id, True, COLOR_TEXT)
        pad_x, pad_y = 4, 2
        pill_w = label.get_width() + pad_x * 2
        pill_h = label.get_height() + pad_y * 2

        pill_surf = pygame.Surface((pill_w, pill_h), pygame.SRCALPHA)
        pill_rect = pygame.Rect(0, 0, pill_w, pill_h)
        pygame.draw.rect(
            pill_surf, COLOR_LABEL_BG, pill_rect, border_radius=pill_h // 2
        )

        pill_screen_rect = pill_surf.get_rect(center=(x, y + size + 10))
        self.screen.blit(pill_surf, pill_screen_rect)
        label_rect = label.get_rect(center=pill_screen_rect.center)
        self.screen.blit(label, label_rect)

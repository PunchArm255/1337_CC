# visualizer.py — pygame-based graphical display for the drone simulation
#
# draws the zone graph, drone sprites, legend, and control panel.
# the visualizer doesn't run the simulation itself — it just receives
# positions from main.py and draws them.
#
# === design decisions ===
# - catppuccin mocha color palette (dark theme that's easy on the eyes)
# - HiDPI/retina support via pygame.SCALED flag (no more pixelation)
# - zones drawn as circles with type-colored borders
# - drones drawn as small sprites with rotor details
# - semi-transparent UI panel with turn counter and controls
#
# === how scaling works ===
# zones have integer coordinates in the map file (like x=3, y=4).
# we need to convert these to pixel positions on screen. we find the
# bounding box of all zones, then scale and center it to fit the window.
#
# ref: https://www.pygame.org/docs/
# ref: https://www.pygame.org/docs/ref/display.html#pygame.display.set_mode
# ref: https://github.com/catppuccin/catppuccin (color palette)

import os
import pygame
from graph import Graph
from data import Zone

# tell SDL to render at the display's native resolution on HiDPI/retina screens.
# without this, pygame renders at 1x (logical pixels) and the OS upscales it,
# which is what causes the pixelation. this must be set BEFORE pygame.init().
os.environ['SDL_VIDEO_ALLOW_HIGHDPI'] = '1'


class Visualizer:
    """handles all pygame rendering for the drone simulation."""

    # -- color palette (catppuccin mocha inspired) --
    COLORS = {
        "bg":           "#1E1E2E",     # dark background
        "line":         "#6C7086",     # connection lines
        "text":         "#FFFFFF",     # general text
        "normal":       "#89B4FA",     # blue for normal zones
        "restricted":   "#FAB387",     # orange for restricted zones
        "priority":     "#A6E3A1",     # green for priority zones
        "blocked":      "#45475A",     # dark gray for blocked zones
        "start_stroke": "#A6E3A1",     # green border for start hub
        "end_stroke":   "#F9E2AF",     # yellow border for end hub
        "drone_body":   "#F38BA8",     # pink drone body
        "drone_arm":    "#11111B",     # dark drone arms
        "drone_rotor":  "#94E2D5",     # teal drone rotors
        # label_bg is the pill behind drone IDs (semi-transparent dark surface)
        "label_bg":     (49, 50, 68, 230),
        # panel_bg needs an alpha channel for transparency (RGBA)
        "panel_bg":     (30, 30, 46, 210),
    }

    def __init__(self, graph: Graph) -> None:
        self.graph = graph

        pygame.init()
        pygame.font.init()

        # window dimensions — these get updated on resize
        self.width = 1200
        self.height = 800

        # RESIZABLE lets the user drag the window edges to resize.
        # we don't use SCALED because it conflicts with RESIZABLE on
        # macOS — resize events stop working properly with both flags.
        self.screen = pygame.display.set_mode(
            (self.width, self.height),
            pygame.RESIZABLE
        )
        pygame.display.set_caption("Fly-in: Drone Routing Simulation")

        # fonts — using system arial, different sizes for different elements
        self.font_title = pygame.font.SysFont("Arial", 26, bold=True)
        self.font_label = pygame.font.SysFont("Arial", 16, bold=True)
        self.font_small = pygame.font.SysFont("Arial", 14, bold=True)

        # compute the scale and offset to fit the map in the window
        self.scale, self.offset_x, self.offset_y, self.max_y = (
            self._calculate_layout()
        )

    # -------------------------------------------------------------------------
    # coordinate math — converting map coords to screen pixels
    # -------------------------------------------------------------------------

    def _calculate_layout(self) -> tuple[float, float, float, int]:
        """computes scale and offsets to center the map in the window.

        looks at all zone coordinates, finds the bounding box, then
        calculates a scale factor so the map fits in 80% of the window.
        the remaining 20% is padding.

        returns (scale, offset_x, offset_y, max_y).
        max_y is stored because we flip the y-axis (map y goes up,
        screen y goes down).
        """
        if not self.graph.zones:
            return 1.0, 0.0, 0.0, 0

        xs = [z.x for z in self.graph.zones.values()]
        ys = [z.y for z in self.graph.zones.values()]

        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)

        # how big the map is in map-coordinates
        map_w = max(max_x - min_x, 1)
        map_h = max(max_y - min_y, 1)

        # leave 20% padding on each side
        usable_w = self.width * 0.8
        usable_h = self.height * 0.8

        # scale to fit — pick the smaller scale so nothing goes off-screen
        scale = min(usable_w / map_w, usable_h / map_h)

        # center the map in the window
        offset_x = (self.width / 2) - ((map_w * scale) / 2) - (min_x * scale)
        offset_y = (self.height / 2) - ((map_h * scale) / 2) - (min_y * scale)

        return scale, offset_x, offset_y, max_y

    def zone_to_pixel(self, zone: Zone) -> tuple[int, int]:
        """converts a zone's map coordinates to screen pixel coordinates.

        the y-axis is flipped because in map coordinates, y increases upward,
        but in pygame, y increases downward. so we do (max_y - zone.y).
        """
        px = int(zone.x * self.scale + self.offset_x)
        py = int((self.max_y - zone.y) * self.scale + self.offset_y)
        return px, py

    def recalculate_on_resize(self, new_width: int, new_height: int) -> None:
        """called when the window is resized — recomputes layout.

        we need to recreate the display surface at the new size,
        not just grab the existing one. pygame.display.set_mode()
        with RESIZABLE creates a fresh surface matching the new
        window dimensions.
        """
        self.width = new_width
        self.height = new_height
        # recreate the surface at the new dimensions
        self.screen = pygame.display.set_mode(
            (self.width, self.height), pygame.RESIZABLE
        )
        self.scale, self.offset_x, self.offset_y, self.max_y = (
            self._calculate_layout()
        )

    # -------------------------------------------------------------------------
    # drawing the static map (zones and connections)
    # -------------------------------------------------------------------------

    def _get_zone_color(self, zone: Zone) -> str:
        """returns the fill color for a zone.

        if the map file specified a color, use that.
        otherwise fall back to the zone type's default color.
        """
        if zone.color:
            return zone.color
        return self.COLORS.get(zone.zone_type, self.COLORS["normal"])

    def draw_background(self) -> None:
        """draws the full static map: background, connections, zones, labels.

        this gets called every frame, but it's fine because pygame is
        efficient at drawing simple shapes. the order matters:
          1. fill background (clears previous frame)
          2. draw connection lines (behind everything)
          3. draw zone circles (on top of lines)
          4. draw zone labels (on top of circles)
        """
        self.screen.fill(self.COLORS["bg"])

        # --- draw connections as lines between zones ---
        for connection in self.graph.connections.values():
            z1 = self.graph.get_zone(connection.zone1)
            z2 = self.graph.get_zone(connection.zone2)
            if z1 and z2:
                p1 = self.zone_to_pixel(z1)
                p2 = self.zone_to_pixel(z2)
                pygame.draw.line(
                    self.screen, self.COLORS["line"], p1, p2, 4
                )

        # --- draw zone circles with borders ---
        radius = 30
        for zone in self.graph.zones.values():
            pos = self.zone_to_pixel(zone)

            # fill circle with zone color
            fill_color = self._get_zone_color(zone)
            try:
                pygame.draw.circle(self.screen, fill_color, pos, radius)
            except ValueError:
                # if the map's color string is invalid, fall back to default
                pygame.draw.circle(
                    self.screen, self.COLORS["normal"], pos, radius
                )

            # border color — start and end hubs get special colors
            if zone == self.graph.start_zone:
                border_color = self.COLORS["start_stroke"]
            elif zone == self.graph.end_zone:
                border_color = self.COLORS["end_stroke"]
            else:
                border_color = self.COLORS.get(
                    zone.zone_type, self.COLORS["normal"]
                )

            # border ring around the circle
            pygame.draw.circle(
                self.screen, border_color, pos, radius + 5, 4
            )

            # --- zone name label above the circle ---
            # start and end hubs use their border color for text
            # but same font size as everything else to keep it clean
            if zone == self.graph.start_zone or zone == self.graph.end_zone:
                text_color = border_color
            else:
                text_color = self.COLORS["text"]

            name_surf = self.font_label.render(zone.name, True, text_color)
            name_rect = name_surf.get_rect(
                center=(pos[0], pos[1] - radius - 20)
            )
            self.screen.blit(name_surf, name_rect)

    # -------------------------------------------------------------------------
    # legend — zone type color reference (top-left corner)
    # -------------------------------------------------------------------------

    def draw_legend(self) -> None:
        """draws the zone type color legend in the top-left corner."""
        items = [
            ("Normal",     self.COLORS["normal"]),
            ("Restricted", self.COLORS["restricted"]),
            ("Priority",   self.COLORS["priority"]),
            ("Blocked",    self.COLORS["blocked"]),
        ]

        x, y = 30, 30
        for name, color in items:
            pygame.draw.circle(self.screen, color, (x + 12, y + 12), 10)
            text_surf = self.font_label.render(name, True, self.COLORS["text"])
            self.screen.blit(text_surf, (x + 35, y + 2))
            y += 30

    # -------------------------------------------------------------------------
    # UI panel — turn counter, controls, and restart button (top-right corner)
    # -------------------------------------------------------------------------

    def draw_ui_panel(
        self,
        current_turn: int,
        max_turns: int,
        is_finished: bool
    ) -> None:
        """draws the transparent control panel in the top-right corner.

        shows the current turn, keyboard controls, and a restart hint.
        the panel uses SRCALPHA for semi-transparency (alpha = 210/255).
        """
        panel_w, panel_h = 260, 120
        pos_x = self.width - panel_w - 30
        pos_y = 30

        # create a surface with transparency support
        panel = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
        panel.fill(self.COLORS["panel_bg"])
        # rounded border for that sleek look
        pygame.draw.rect(
            panel, self.COLORS["line"], panel.get_rect(), 2, border_radius=8
        )
        self.screen.blit(panel, (pos_x, pos_y))

        # turn counter — turns green when simulation is finished
        turn_str = f"TURN: {current_turn} / {max_turns}"
        turn_color = (
            self.COLORS["start_stroke"] if is_finished
            else self.COLORS["text"]
        )
        turn_surf = self.font_title.render(turn_str, True, turn_color)
        self.screen.blit(turn_surf, (pos_x + 20, pos_y + 12))

        # control hints
        controls = [
            "[SPACE] Advance Turn",
            "[R] Restart Simulation",
            "[ESC] Exit",
        ]
        cy = pos_y + 50
        for ctrl in controls:
            ctrl_surf = self.font_small.render(
                ctrl, True, self.COLORS["text"]
            )
            self.screen.blit(ctrl_surf, (pos_x + 20, cy))
            cy += 20

    # -------------------------------------------------------------------------
    # drone sprite — the little flying machine
    # -------------------------------------------------------------------------

    def draw_drone(self, drone_id: str, pos: tuple[float, float]) -> None:
        """draws a single drone sprite at the given pixel position.

        the drone is made of:
          - two crossed lines (the arms)
          - four small circles at the ends (the rotors)
          - one larger circle in the center (the body)
          - a text label below (the drone ID)

        it's all done with basic pygame shapes — no images needed.
        """
        x, y = int(pos[0]), int(pos[1])
        size = 15
        offset = int(size * 0.7)

        # draw the crossed arms
        pygame.draw.line(
            self.screen, self.COLORS["drone_arm"],
            (x - offset, y - offset), (x + offset, y + offset), 3
        )
        pygame.draw.line(
            self.screen, self.COLORS["drone_arm"],
            (x - offset, y + offset), (x + offset, y - offset), 3
        )

        # draw four rotors at the arm endpoints
        rotor_r = int(size * 0.45)
        for dx, dy in [(-1, -1), (1, 1), (-1, 1), (1, -1)]:
            rx, ry = x + dx * offset, y + dy * offset
            pygame.draw.circle(
                self.screen, self.COLORS["drone_rotor"], (rx, ry), rotor_r
            )
            pygame.draw.circle(
                self.screen, self.COLORS["drone_arm"], (rx, ry), rotor_r, 1
            )

        # draw the center body
        body_r = int(size * 0.7)
        pygame.draw.circle(
            self.screen, self.COLORS["drone_body"], (x, y), body_r
        )
        pygame.draw.circle(
            self.screen, self.COLORS["drone_arm"], (x, y), body_r, 2
        )

        # drone ID label below the sprite — pill-shaped with rounded corners
        label = self.font_small.render(drone_id, True, self.COLORS["text"])
        pad_x, pad_y = 6, 3  # horizontal and vertical padding around text
        pill_w = label.get_width() + pad_x * 2
        pill_h = label.get_height() + pad_y * 2
        # create a transparent surface for the pill background
        pill_surf = pygame.Surface((pill_w, pill_h), pygame.SRCALPHA)
        # draw a rounded rect (the pill shape) onto it
        pill_rect = pygame.Rect(0, 0, pill_w, pill_h)
        pygame.draw.rect(
            pill_surf, self.COLORS["label_bg"], pill_rect,
            border_radius=pill_h // 2  # fully rounded ends = pill shape
        )
        # position the pill centered below the drone
        pill_screen_rect = pill_surf.get_rect(center=(x, y + size + 14))
        self.screen.blit(pill_surf, pill_screen_rect)
        # draw the text centered inside the pill
        label_rect = label.get_rect(center=pill_screen_rect.center)
        self.screen.blit(label, label_rect)
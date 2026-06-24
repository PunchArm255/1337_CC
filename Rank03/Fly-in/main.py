# main.py — orchestrates the entire fly-in simulation
#
# this is the entry point. it ties everything together:
#   1. parse the map file
#   2. build the graph
#   3. run the pathfinder (dijkstra)
#   4. create the simulation engine
#   5. run the pygame visualization loop
#
# the pygame loop handles:
#   - SPACE: advance one turn (with smooth animation)
#   - R: restart the simulation from turn 0 (replay same paths)
#   - ESC: quit
#   - window resize: recalculate layout
#
# === how the animation works ===
# when you press SPACE, we don't just teleport drones to their new
# positions. instead, we smoothly interpolate between the old position
# and the new position over ~25 frames (at 60fps, that's about 0.4 sec).
#
# the interpolation uses "smoothstep" — a math function that starts
# slow, speeds up, then slows down again. it looks way more natural
# than linear movement.
#
# ref: https://en.wikipedia.org/wiki/Smoothstep

import sys
import pygame
from parser import map_parser, ParsingError
from graph import Graph
from pathfinder import Pathfinder
from simulation import SimulationEngine
from visualizer import Visualizer


def get_drone_pixel_pos(
    viz: Visualizer,
    graph: Graph,
    state_str: str
) -> tuple[float, float]:
    """converts a drone's state string to pixel coordinates.

    a drone's state is either:
      - a zone name like "roof1" -> pixel position of that zone
      - a connection like "roof1-roof2" -> midpoint between the two zones
        (for drones in transit to restricted zones)
    """
    if "-" in state_str:
        # drone is on a connection — position it at the midpoint
        z1_name, z2_name = state_str.split("-")
        z1 = graph.get_zone(z1_name)
        z2 = graph.get_zone(z2_name)
        p1 = viz.zone_to_pixel(z1)
        p2 = viz.zone_to_pixel(z2)
        return ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)
    else:
        # drone is at a zone — position it at the zone's center
        zone = graph.get_zone(state_str)
        return viz.zone_to_pixel(zone)


def smoothstep(t: float) -> float:
    """attempt at smooth interpolation — eases in and out.

    takes a value t between 0 and 1, returns a smoothed value also
    between 0 and 1. the curve starts slow, speeds up in the middle,
    and slows down at the end. makes drone movement feel natural.

    the formula is: 3t² - 2t³ (also written as t² * (3 - 2t))
    this is a standard technique in computer graphics.

    ref: https://en.wikipedia.org/wiki/Smoothstep
    """
    return t * t * (3.0 - 2.0 * t)


def run_simulation(
    graph: Graph,
    paths: list[list[tuple[int, str]]],
    nb_drones: int,
    viz: Visualizer
) -> None:
    """main pygame loop — handles events, animation, and rendering.

    this function runs until the user presses ESC or closes the window.
    it can be called again for a restart (same graph and paths).
    """
    # create the simulation engine and get its generator
    engine = SimulationEngine(graph, paths)
    sim_gen = engine.run()

    max_turns = engine.max_turn
    current_turn = 0

    # drone position tracking for animation
    # prev = where drones were before the last SPACE press
    # target = where drones should be after the animation finishes
    start_name = graph.start_zone.name
    prev_state = {f"D{i + 1}": start_name for i in range(nb_drones)}
    target_state = dict(prev_state)

    # animation progress: 0.0 = just started, 1.0 = finished
    anim_progress = 1.0
    anim_speed = 0.04  # how fast the animation plays (higher = faster)

    clock = pygame.time.Clock()
    running = True

    print("press [SPACE] to advance, [R] to restart, [ESC] to quit")
    print()

    while running:
        # --- event handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # window close button
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                elif event.key == pygame.K_SPACE:
                    # advance one turn (only if animation is done and turns remain)
                    if anim_progress >= 1.0 and current_turn < max_turns:
                        try:
                            # save current positions as the animation start
                            prev_state = dict(target_state)
                            # get next turn's positions from the generator
                            target_state = next(sim_gen)
                            # reset animation to play from the beginning
                            anim_progress = 0.0
                            current_turn += 1
                        except StopIteration:
                            pass

                elif event.key == pygame.K_r:
                    # restart — re-run the simulation with the same paths
                    # we return from this function and main() calls us again
                    return

            elif event.type == pygame.VIDEORESIZE:
                # window was resized — recalculate zone positions
                viz.recalculate_on_resize(event.w, event.h)

        # --- update animation ---
        if anim_progress < 1.0:
            anim_progress += anim_speed
            if anim_progress > 1.0:
                anim_progress = 1.0

        # apply smoothstep to make the animation ease in/out
        smooth_t = smoothstep(anim_progress)

        # --- draw everything ---

        # 1. draw the static map (background, connections, zones)
        viz.draw_background()

        # 2. draw drones at their interpolated positions
        for drone_id in target_state:
            # get pixel positions for the old and new states
            old_pos = get_drone_pixel_pos(
                viz, graph, prev_state.get(drone_id, start_name)
            )
            new_pos = get_drone_pixel_pos(
                viz, graph, target_state.get(drone_id, start_name)
            )

            # linear interpolation between old and new, curved by smoothstep
            # when smooth_t = 0 -> drone is at old_pos
            # when smooth_t = 1 -> drone is at new_pos
            current_x = old_pos[0] + (new_pos[0] - old_pos[0]) * smooth_t
            current_y = old_pos[1] + (new_pos[1] - old_pos[1]) * smooth_t

            viz.draw_drone(drone_id, (current_x, current_y))

        # 3. draw the UI panel on top of everything
        is_finished = (current_turn >= max_turns)
        viz.draw_ui_panel(current_turn, max_turns, is_finished)

        # 4. draw the legend
        viz.draw_legend()

        # flip the display buffer (show what we drew)
        pygame.display.flip()

        # cap at 60 fps — no need to burn CPU cycles faster than that
        clock.tick(60)


def main() -> None:
    """entry point — parses the map, runs pathfinding, and starts the viz."""
    # accept map file as command-line argument, default to "map.txt"
    if len(sys.argv) > 1:
        map_file = sys.argv[1]
    else:
        map_file = "map.txt"

    # --- step 1: parse the map file ---
    try:
        parsed_map = map_parser(map_file)
    except ParsingError as e:
        print(f"parsing error: {e}")
        return

    print(f"loaded map: {map_file}")
    print(f"  zones: {len(parsed_map.zones)}")
    print(f"  connections: {len(parsed_map.connections)}")
    print(f"  drones: {parsed_map.nb_drones}")
    print()

    # --- step 2: build the graph ---
    graph = Graph(parsed_map)

    # --- step 3: run pathfinding ---
    print("calculating routes with dijkstra...")
    pf = Pathfinder(graph, parsed_map.nb_drones)
    paths = pf.solve()
    print(f"pathfinding complete!")
    print()

    # --- step 4: create visualizer (only once, reused on restart) ---
    viz = Visualizer(graph)

    # --- step 5: run the simulation loop (restarts come back here) ---
    while True:
        run_simulation(graph, paths, parsed_map.nb_drones, viz)
        # if run_simulation returns, the user pressed R (restart)
        print()
        print("--- RESTARTING SIMULATION ---")
        print()


if __name__ == "__main__":
    main()
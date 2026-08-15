# main.py - entry point and execution loop for fly-in
import os
import sys

# silence pygame prompt
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import pygame  # noqa: E402
from parser import map_parser, ParsingError  # noqa: E402
from graph import Graph  # noqa: E402
from pathfinder import Pathfinder  # noqa: E402
from simulation import SimulationEngine  # noqa: E402
from visualizer import Visualizer  # noqa: E402


def get_drone_pixel_pos(
    viz: Visualizer, graph: Graph, state_str: str
) -> tuple[float, float]:
    """converts a drone's state string to screen pixel coordinates."""
    # if state is "zoneA-zoneB", drone is in transit (draw at midpoint)
    if "-" in state_str:
        z1_name, z2_name = state_str.split("-")
        z1 = graph.get_zone(z1_name)
        z2 = graph.get_zone(z2_name)
        if z1 and z2:
            p1 = viz.zone_to_pixel(z1)
            p2 = viz.zone_to_pixel(z2)
            return ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)

    # otherwise drone is resting at a single zone node
    zone = graph.get_zone(state_str)
    if zone:
        px, py = viz.zone_to_pixel(zone)
        return float(px), float(py)
    return 0.0, 0.0


def smoothstep(t: float) -> float:
    """eases in and out between 0 and 1 using the 3t^2 - 2t^3 curve."""
    return t * t * (3.0 - 2.0 * t)


def run_simulation(
    graph: Graph,
    paths: list[list[tuple[int, str]]],
    nb_drones: int,
    viz: Visualizer,
) -> None:
    """handles pygame event loop, animation, and rendering."""
    engine = SimulationEngine(graph, paths)
    sim_gen = engine.run()

    max_turns = engine.max_turn
    current_turn = 0

    # all drones start at the starting hub
    start_name = graph.start_zone.name
    prev_state = {f"D{i + 1}": start_name for i in range(nb_drones)}
    target_state = dict(prev_state)

    anim_progress = 1.0
    anim_speed = 0.05  # animation step per frame (~20 frames total)

    clock = pygame.time.Clock()
    running = True

    print("Controls: [SPACE] advance, [R] restart, [ESC] quit")
    print()

    while running:
        # process user input events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit(0)

                elif event.key == pygame.K_SPACE:
                    # advance once previous animation is complete
                    if anim_progress >= 1.0 and current_turn < max_turns:
                        try:
                            prev_state = dict(target_state)
                            target_state = next(sim_gen)
                            anim_progress = 0.0
                            current_turn += 1
                        except StopIteration:
                            pass

                elif event.key == pygame.K_r:
                    # restart simulation
                    return

            elif event.type == pygame.VIDEORESIZE:
                viz.recalculate_on_resize(event.w, event.h)

        # advance animation progress
        if anim_progress < 1.0:
            anim_progress += anim_speed
            if anim_progress > 1.0:
                anim_progress = 1.0

        smooth_t = smoothstep(anim_progress)

        # render background, nodes, and connections
        viz.draw_background()

        # interpolate drone positions smoothly between turns
        for drone_id in target_state:
            old_pos = get_drone_pixel_pos(
                viz, graph, prev_state.get(drone_id, start_name)
            )
            new_pos = get_drone_pixel_pos(
                viz, graph, target_state.get(drone_id, start_name)
            )

            current_x = old_pos[0] + (new_pos[0] - old_pos[0]) * smooth_t
            current_y = old_pos[1] + (new_pos[1] - old_pos[1]) * smooth_t

            viz.draw_drone(drone_id, (current_x, current_y))

        is_finished = current_turn >= max_turns
        viz.draw_turn_counter(current_turn, max_turns, is_finished)
        viz.draw_legend()

        pygame.display.flip()
        clock.tick(60)


def main() -> None:
    """main program entry point."""
    map_file = sys.argv[1] if len(sys.argv) > 1 else "map.txt"

    # step 1: parse map file
    try:
        parsed_map = map_parser(map_file)
    except ParsingError as e:
        print(f"Parsing error: {e}")
        return

    print(f"Loaded map: {map_file}")
    print(f"  zones: {len(parsed_map.zones)}")
    print(f"  connections: {len(parsed_map.connections)}")
    print(f"  drones: {parsed_map.nb_drones}")
    print()

    # step 2: construct graph
    graph = Graph(parsed_map)

    # step 3: calculate collision-free paths
    print("Calculating routes with dijkstra...")
    pf = Pathfinder(graph, parsed_map.nb_drones)
    paths = pf.solve()
    print("Pathfinding complete!")
    print()

    # step 4: initialize pygame visualizer
    viz = Visualizer(graph)

    # step 5: run interactive loop (pressing R restarts loop)
    while True:
        run_simulation(graph, paths, parsed_map.nb_drones, viz)
        print()
        print("--- RESTARTING SIMULATION ---")
        print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # exit cleanly on ctrl+c without traceback
        print("\nSimulation aborted by user.")
        try:
            pygame.quit()
        except Exception:
            pass
        sys.exit(0)

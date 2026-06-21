import pygame
import sys
from parser import map_parser
from graph import Graph
from pathfinder import Pathfinder
from simulation import SimulationEngine
from visualizer import Visualizer

def get_target_pixels(viz: Visualizer, graph: Graph, state_str: str) -> tuple[float, float]:
    if "-" in state_str:
        z1, z2 = state_str.split("-")
        p1 = viz._get_pixel_coords(graph.get_zone(z1))
        p2 = viz._get_pixel_coords(graph.get_zone(z2))
        return ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)
    else:
        return viz._get_pixel_coords(graph.get_zone(state_str))

def main():
    try:
        parsed_map = map_parser("map.txt")
    except Exception as e:
        print(e)
        return

    graph = Graph(parsed_map)
    
    print("Calculating optimal routes...")
    pf = Pathfinder(graph, parsed_map.nb_drones)
    paths = pf.solve()
    
    engine = SimulationEngine(graph, paths)
    
    # 1. We instantiate the generator for the first time
    sim_generator = engine.run()
    
    viz = Visualizer(graph)
    
    start_hub_name = graph.start_zone.name
    
    # Initial State setup
    prev_visual_state = {f"D{i+1}": start_hub_name for i in range(parsed_map.nb_drones)}
    target_visual_state = dict(prev_visual_state)
    
    anim_progress = 1.0  
    anim_speed = 0.04    
    current_turn = 0     # <--- Tracks our current turn for the HUD

    clock = pygame.time.Clock()
    running = True
    
    print("Launch Successful! Press [SPACEBAR] to advance, [R] to restart.")

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                
                # --- RESTART ENGINE LOGIC ---
                elif event.key == pygame.K_r:
                    print("\n--- RESTARTING SIMULATION ---")
                    # Throw away the old generator and create a brand new one
                    sim_generator = engine.run()
                    # Reset all visual states back to the start hub
                    prev_visual_state = {f"D{i+1}": start_hub_name for i in range(parsed_map.nb_drones)}
                    target_visual_state = dict(prev_visual_state)
                    # Reset animation and turn counter
                    anim_progress = 1.0
                    current_turn = 0
                
                # --- SPACEBAR LOGIC ---
                elif event.key == pygame.K_SPACE:
                    if anim_progress >= 1.0:
                        try:
                            prev_visual_state = dict(target_visual_state)
                            target_visual_state = next(sim_generator)
                            anim_progress = 0.0
                            current_turn += 1  # <--- Increment the Turn Counter
                        except StopIteration:
                            print("All drones delivered! Press R to restart.")

            elif event.type == pygame.VIDEORESIZE:
                viz.WIDTH, viz.HEIGHT = event.w, event.h
                viz.screen = pygame.display.get_surface()
                viz.scale, viz.offset_x, viz.offset_y, viz.max_y = viz._calculate_scale()
                
        # Animation Math
        if anim_progress < 1.0:
            anim_progress += anim_speed
            if anim_progress > 1.0:
                anim_progress = 1.0
        
        t = anim_progress
        smooth_t = t * t * (3.0 - 2.0 * t)

        # 1. Draw Map
        viz._draw_static_map()
        
        # 2. Draw Drones
        for drone_id in target_visual_state.keys():
            old_str = prev_visual_state.get(drone_id, start_hub_name)
            new_str = target_visual_state.get(drone_id, start_hub_name)
            
            start_x, start_y = get_target_pixels(viz, graph, old_str)
            end_x, end_y = get_target_pixels(viz, graph, new_str)
            
            current_x = start_x + (end_x - start_x) * smooth_t
            current_y = start_y + (end_y - start_y) * smooth_t
            
            viz.draw_drone(drone_id, (current_x, current_y))

        # 3. Draw HUD Overlay (Drawn last so it sits on top of everything)
        viz.draw_hud(current_turn, engine.max_turn)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
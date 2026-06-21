from graph import Graph

class SimulationEngine:
    def __init__(self, graph: Graph, all_paths: list[list[tuple[int, str]]]):
        self.graph = graph
        self.paths = all_paths
        # Find the absolute last turn any drone arrives at the goal
        self.max_turn = max((path[-1][0] for path in all_paths if path), default=0)

    def run(self):
        """
        Generates the terminal output AND yields the state for Pygame.
        """
        print(f"--- SIMULATION START (Total Turns: {self.max_turn}) ---")
        
        # Loop through every simulation turn (1 to Max)
        for turn in range(1, self.max_turn + 1):
            turn_output = []
            
            # Dictionary telling Pygame where every drone is { "D1": "roof1", "D2": "hub-roof1" }
            visual_state = {} 
            
            for d_idx, path in enumerate(self.paths):
                drone_id = f"D{d_idx + 1}"
                
                # Check where this drone is during this specific turn
                for j in range(len(path) - 1):
                    t_prev, z_prev = path[j]
                    t_next, z_next = path[j+1]
                    
                    if t_prev < turn <= t_next:
                        if z_prev == z_next:
                            # Drone is waiting. Subject says: "Drones that do not move are omitted"
                            visual_state[drone_id] = z_prev
                        elif turn == t_next:
                            # Drone arrived at its destination this turn
                            turn_output.append(f"{drone_id}-{z_next}")
                            visual_state[drone_id] = z_next
                        else:
                            # Drone is in mid-air transit towards a restricted zone
                            turn_output.append(f"{drone_id}-{z_prev}-{z_next}")
                            visual_state[drone_id] = f"{z_prev}-{z_next}"
                        break
                    
                    # If the turn is past the drone's final arrival, it's at the goal
                    elif turn > path[-1][0]:
                        visual_state[drone_id] = path[-1][1]

            # Print to terminal exactly as the subject requests
            if turn_output:
                print(" ".join(turn_output))
            
            # YIELD pauses the function here and hands the visual_state to Pygame!
            yield visual_state
            
        print("--- SIMULATION COMPLETE ---")
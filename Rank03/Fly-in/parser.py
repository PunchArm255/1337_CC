import re
from data import MapStructure, Zone, Connection

class ParsingError(Exception):
    pass

def metadata_parser(line_num: int, line: str) -> dict[str, str]:
    # Catch unclosed brackets
    if '[' in line and ']' not in line:
        raise ParsingError(f"[Line {line_num}] Error: Unclosed metadata bracket.")
    
    result = re.search(r"\[(.*?)\]", line)
    if not result:
        return {}

    pairs = result.group(1).split()
    metadata = {}
    
    for p in pairs:
        if '=' in p:
            k, v = p.split('=', 1)
            if not v:
                raise ParsingError(f"[Line {line_num}] Error: Metadata key '{k}' has no value.")
            metadata[k] = v

    return metadata

def map_parser(filepath: str) -> MapStructure:
    new_map = MapStructure()
    parsed_drones = False
    seen_connections = set()
    parsing_connections = False 

    try:
        with open(filepath, "r") as f:
            for line_num, line in enumerate(f, start=1):
                line = line.strip()

                # Nuke inline comments and re-strip
                if '#' in line:
                    line = line.split('#', 1)[0].strip()

                # Ignore empty lines
                if not line:
                    continue

                # B. nb_drones Errors
                if not parsed_drones:
                    if not line.startswith('nb_drones:'):
                        raise ParsingError(f"[Line {line_num}] Error: 'nb_drones:' must be the first meaningful line.")
                    
                    val_str = line.split(':', 1)[1].strip()
                    if not val_str:
                        raise ParsingError(f"[Line {line_num}] Error: 'nb_drones:' has no value.")
                    try:
                        nb_drones = int(val_str)
                        if nb_drones <= 0:
                            raise ValueError()
                        new_map.nb_drones = nb_drones
                        parsed_drones = True
                    except ValueError:
                        raise ParsingError(f"[Line {line_num}] Error: 'nb_drones' must be a positive integer.")
                    continue
                
                if line.startswith('nb_drones:'):
                    raise ParsingError(f"[Line {line_num}] Error: 'nb_drones:' defined multiple times.")

                # C. Zone Definition Errors
                if line.startswith(('start_hub:', 'end_hub:', 'hub:')):
                    if parsing_connections:
                        raise ParsingError(f"[Line {line_num}] Error: Hubs must be defined before connections.")

                    # Remove metadata block to cleanly extract name and coordinates
                    core_line = re.sub(r"\[.*?\]", "", line).strip()
                    core_parts = core_line.split()

                    if len(core_parts) != 4:
                        raise ParsingError(f"[Line {line_num}] Error: Zone missing name or coordinates.")

                    prefix, name, x_str, y_str = core_parts

                    if '-' in name:
                        raise ParsingError(f"[Line {line_num}] Error: Zone names cannot contain a dash.")
                    
                    if name in new_map.zones:
                        raise ParsingError(f"[Line {line_num}] Error: Duplicate zone name '{name}'.")

                    try:
                        x = int(x_str)
                        y = int(y_str)
                    except ValueError:
                        raise ParsingError(f"[Line {line_num}] Error: Coordinates must be integers.")

                    metadata = metadata_parser(line_num, line)

                    z_type = metadata.get("zone", "normal")
                    if z_type not in ["normal", "blocked", "restricted", "priority"]:
                        raise ParsingError(f"[Line {line_num}] Error: Invalid zone type '{z_type}'.")

                    try:
                        max_drones = int(metadata.get("max_drones", 1))
                        if max_drones <= 0:
                            raise ValueError()
                    except ValueError:
                        raise ParsingError(f"[Line {line_num}] Error: 'max_drones' must be a positive integer.")

                    new_zone = Zone(
                        name=name,
                        x=x,
                        y=y,
                        zone_type=z_type,
                        max_drones=max_drones,
                        color=metadata.get("color")
                    )

                    new_map.zones[name] = new_zone

                    if prefix == 'start_hub:':
                        if new_map.start_hub is not None:
                            raise ParsingError(f"[Line {line_num}] Error: Multiple start_hub definitions.")
                        new_map.start_hub = new_zone
                    elif prefix == 'end_hub:':
                        if new_map.end_hub is not None:
                            raise ParsingError(f"[Line {line_num}] Error: Multiple end_hub definitions.")
                        new_map.end_hub = new_zone

                # D. Connection Errors
                elif line.startswith('connection:'):
                    parsing_connections = True
                    
                    core_line = re.sub(r"\[.*?\]", "", line).strip()
                    core_parts = core_line.split()
                    
                    if len(core_parts) != 2:
                        raise ParsingError(f"[Line {line_num}] Error: Invalid connection format.")
                        
                    connection_str = core_parts[1]
                    
                    if connection_str.count('-') != 1:
                        raise ParsingError(f"[Line {line_num}] Error: Connection pair must contain exactly one dash.")
                        
                    zone1, zone2 = connection_str.split('-')
                    
                    if zone1 not in new_map.zones or zone2 not in new_map.zones:
                        raise ParsingError(f"[Line {line_num}] Error: Connection references undefined zone(s).")
                        
                    if zone1 == zone2:
                        raise ParsingError(f"[Line {line_num}] Error: Self-connections are not allowed.")
                        
                    # Catch duplicate connections regardless of order (a-b vs b-a)
                    sorted_pair = tuple(sorted([zone1, zone2]))
                    if sorted_pair in seen_connections:
                        raise ParsingError(f"[Line {line_num}] Error: Duplicate connection detected.")
                    seen_connections.add(sorted_pair)

                    metadata = metadata_parser(line_num, line)
                    
                    try:
                        max_link = int(metadata.get("max_link_capacity", 1))
                        if max_link <= 0:
                            raise ValueError()
                    except ValueError:
                        raise ParsingError(f"[Line {line_num}] Error: 'max_link_capacity' must be a positive integer.")

                    cnx = Connection(
                        zone1=zone1,
                        zone2=zone2,
                        max_link_capacity=max_link
                    )
                    new_map.connections.append(cnx)

                # E. Unknown Line Errors
                else:
                    raise ParsingError(f"[Line {line_num}] Error: Unrecognized line format.")

        # F. End-of-File Structural Errors
        if not parsed_drones:
            raise ParsingError("Error: File is empty or missing 'nb_drones'.")
        if new_map.start_hub is None:
            raise ParsingError("Error: No 'start_hub' defined in the file.")
        if new_map.end_hub is None:
            raise ParsingError("Error: No 'end_hub' defined in the file.")

    # A. File-Level Errors
    except FileNotFoundError:
        raise ParsingError(f"Error: File not found -> {filepath}")
    except PermissionError:
        raise ParsingError(f"Error: Permission denied to read file -> {filepath}")

    return new_map

# def main():
#     try:
#         map_parser("map.txt")
#         print("Everything works perfectly!")
#     except ParsingError as e:
#         print(e)

# main()
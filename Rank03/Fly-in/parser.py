import re
from data import MapStructure, Zone, Connection


class ParsingError(Exception):
    pass


def metadata_parser(line: str) -> dict[str, str]:
    result = re.search(r"\[(.*?)\]", line)
    if not result:
        return {}

    pairs = result.group(1).split()

    metadata = {}
    for p in pairs:
        if '=' in p:
            k, v = p.split('=', 1)
            metadata[k] = v

    return metadata

def map_parser(filepath: str) -> MapStructure:
    new_map = MapStructure()

    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()

            if not line or line.startswith('#'):
                continue

            if line.startswith('nb_drones:'):
                new_map.nb_drones = int(line.split(':')[1].strip())

            elif line.startswith(('start_hub:', 'end_hub:', 'hub:')):
                parts = line.split() 
                metadata = metadata_parser(line)
                
                z_type = metadata.get("zone", "normal")
                if z_type not in ["normal", "blocked", "restricted", "priority"]:
                    raise ParsingError(f"[ERROR] - Invalid zone type '{z_type}' on line: {line}")

                new_zone = Zone(
                    name=parts[1],
                    x=int(parts[2]),
                    y=int(parts[3]),
                    zone_type=z_type,
                    max_drones=int(metadata.get("max_drones", 1)),
                    color=metadata.get("color")
                )

                new_map.zones[parts[1]] = new_zone

                if line.startswith('start_hub:'):
                    if new_map.start_hub is not None:
                        raise ValueError("Parsing Error: Multiple start hubs detected.")
                    new_map.start_hub = new_zone
                    
                elif line.startswith('end_hub:'):
                    if new_map.end_hub is not None:
                        raise ValueError("Parsing Error: Multiple end hubs detected.")
                    new_map.end_hub = new_zone

            elif line.startswith('connection:'):
                parts = line.split()
                zone1, zone2 = parts[1].split('-')
                
                metadata = metadata_parser(line)

                if zone1 not in new_map.zones or zone2 not in new_map.zones:
                    raise ValueError(f"[ERROR] - Connection references unknown zones on line: {line}")

                cnx = Connection(
                    zone1=zone1,
                    zone2=zone2,
                    max_link_capacity=int(metadata.get("max_link_capacity", 1))
                )
                new_map.connections.append(cnx)

    if new_map.start_hub is None or new_map.end_hub is None:
        raise ParsingError("[ERROR] Map must have exactly one start_hub and one end_hub.")

    return new_map
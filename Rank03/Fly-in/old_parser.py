import re
from data import MapStructure, Zone, Connection


class ParsingError(Exception):
    pass


class MapParser:

    def __init__(self) -> None:
        self.map = MapStructure()
        self.line_num = 0
        self.parsed_drones = False
        self.connections_started = False
        self.seen_connections: set[tuple[str, str]] = set()

    def _parse_metadata(self, line: str) -> dict[str, str]:
        if '[' in line and ']' not in line:
            raise ParsingError(
                f"[Line {self.line_num}] Error: Unclosed metadata bracket."
            )

        result = re.search(r"\[(.*?)\]", line)
        if not result:
            return {}

        pairs = result.group(1).split()
        metadata: dict[str, str] = {}

        for p in pairs:
            if '=' not in p:
                raise ParsingError(
                    f"[Line {self.line_num}] Error: "
                    f"Invalid metadata token '{p}' — expected key=value format."
                )
            k, v = p.split('=', 1)
            if not k:
                raise ParsingError(
                    f"[Line {self.line_num}] Error: "
                    f"Metadata key cannot be empty."
                )
            if not v:
                raise ParsingError(
                    f"[Line {self.line_num}] Error: "
                    f"Metadata key '{k}' has no value."
                )
            metadata[k] = v

        return metadata

    def _parse_nb_drones(self, line: str) -> None:
        if self.parsed_drones:
            raise ParsingError(
                f"[Line {self.line_num}] Error: "
                f"'nb_drones:' defined multiple times."
            )

        val_str = line.split(':', 1)[1].strip()
        if not val_str:
            raise ParsingError(
                f"[Line {self.line_num}] Error: 'nb_drones:' has no value."
            )

        try:
            nb_drones = int(val_str)
        except ValueError:
            raise ParsingError(
                f"[Line {self.line_num}] Error: "
                f"'nb_drones' must be a positive integer, got '{val_str}'."
            )

        if nb_drones <= 0:
            raise ParsingError(
                f"[Line {self.line_num}] Error: "
                f"'nb_drones' must be a positive integer, got '{nb_drones}'."
            )

        self.map.nb_drones = nb_drones
        self.parsed_drones = True

    def _parse_hub_line(self, line: str) -> None:
        if self.connections_started:
            raise ParsingError(
                f"[Line {self.line_num}] Error: "
                f"Zone definitions must appear before connections."
            )

        core_line = re.sub(r"\[.*?\]", "", line).strip()
        core_parts = core_line.split()

        if len(core_parts) < 4:
            raise ParsingError(
                f"[Line {self.line_num}] Error: "
                f"Zone line is missing name or coordinates."
            )
        if len(core_parts) > 4:
            raise ParsingError(
                f"[Line {self.line_num}] Error: "
                f"Zone line has unexpected extra content."
            )

        prefix, name, x_str, y_str = core_parts

        if not name:
            raise ParsingError(
                f"[Line {self.line_num}] Error: Zone name cannot be empty."
            )
        if '-' in name:
            raise ParsingError(
                f"[Line {self.line_num}] Error: "
                f"Zone name '{name}' cannot contain a dash."
            )

        if name in self.map.zones:
            raise ParsingError(
                f"[Line {self.line_num}] Error: "
                f"Duplicate zone name '{name}'."
            )

        try:
            x = int(x_str)
        except ValueError:
            raise ParsingError(
                f"[Line {self.line_num}] Error: "
                f"X coordinate must be an integer, got '{x_str}'."
            )

        try:
            y = int(y_str)
        except ValueError:
            raise ParsingError(
                f"[Line {self.line_num}] Error: "
                f"Y coordinate must be an integer, got '{y_str}'."
            )

        metadata = self._parse_metadata(line)

        z_type = metadata.get("zone", "normal")
        if z_type not in ["normal", "blocked", "restricted", "priority"]:
            raise ParsingError(
                f"[Line {self.line_num}] Error: "
                f"Invalid zone type '{z_type}'."
            )

        max_drones_str = metadata.get("max_drones", "1")
        try:
            max_drones = int(max_drones_str)
        except ValueError:
            raise ParsingError(
                f"[Line {self.line_num}] Error: "
                f"'max_drones' must be a positive integer, "
                f"got '{max_drones_str}'."
            )
        if max_drones <= 0:
            raise ParsingError(
                f"[Line {self.line_num}] Error: "
                f"'max_drones' must be a positive integer, "
                f"got '{max_drones}'."
            )

        # Check hub multiplicity BEFORE adding to zones
        if prefix == 'start_hub:' and self.map.start_hub is not None:
            raise ParsingError(
                f"[Line {self.line_num}] Error: "
                f"Multiple 'start_hub' definitions."
            )
        if prefix == 'end_hub:' and self.map.end_hub is not None:
            raise ParsingError(
                f"[Line {self.line_num}] Error: "
                f"Multiple 'end_hub' definitions."
            )

        new_zone = Zone(
            name=name,
            x=x,
            y=y,
            zone_type=z_type,
            max_drones=max_drones,
            color=metadata.get("color")
        )

        self.map.zones[name] = new_zone

        if prefix == 'start_hub:':
            self.map.start_hub = new_zone
        elif prefix == 'end_hub:':
            self.map.end_hub = new_zone

    def _parse_connection_line(self, line: str) -> None:
        self.connections_started = True

        core_line = re.sub(r"\[.*?\]", "", line).strip()
        core_parts = core_line.split()

        if len(core_parts) < 2:
            raise ParsingError(
                f"[Line {self.line_num}] Error: "
                f"Connection line is missing zone pair."
            )
        if len(core_parts) > 2:
            raise ParsingError(
                f"[Line {self.line_num}] Error: "
                f"Connection line has unexpected extra content."
            )

        connection_str = core_parts[1]
        dash_count = connection_str.count('-')

        if dash_count == 0:
            raise ParsingError(
                f"[Line {self.line_num}] Error: "
                f"Connection pair must contain a dash separating two zone names."
            )
        if dash_count > 1:
            raise ParsingError(
                f"[Line {self.line_num}] Error: "
                f"Connection pair has too many dashes — "
                f"zone names cannot contain dashes."
            )

        zone1, zone2 = connection_str.split('-')

        if not zone1 or not zone2:
            raise ParsingError(
                f"[Line {self.line_num}] Error: "
                f"Connection zone names cannot be empty."
            )

        if zone1 == zone2:
            raise ParsingError(
                f"[Line {self.line_num}] Error: "
                f"A zone cannot connect to itself ('{zone1}')."
            )

        if zone1 not in self.map.zones:
            raise ParsingError(
                f"[Line {self.line_num}] Error: "
                f"Connection references undefined zone '{zone1}'."
            )
        if zone2 not in self.map.zones:
            raise ParsingError(
                f"[Line {self.line_num}] Error: "
                f"Connection references undefined zone '{zone2}'."
            )

        sorted_pair = tuple(sorted([zone1, zone2]))
        if sorted_pair in self.seen_connections:
            raise ParsingError(
                f"[Line {self.line_num}] Error: "
                f"Duplicate connection '{zone1}-{zone2}'."
            )

        metadata = self._parse_metadata(line)

        max_link_str = metadata.get("max_link_capacity", "1")
        try:
            max_link = int(max_link_str)
        except ValueError:
            raise ParsingError(
                f"[Line {self.line_num}] Error: "
                f"'max_link_capacity' must be a positive integer, "
                f"got '{max_link_str}'."
            )
        if max_link <= 0:
            raise ParsingError(
                f"[Line {self.line_num}] Error: "
                f"'max_link_capacity' must be a positive integer, "
                f"got '{max_link}'."
            )

        self.seen_connections.add(sorted_pair)
        self.map.connections.append(Connection(
            zone1=zone1,
            zone2=zone2,
            max_link_capacity=max_link
        ))

    def parse(self, filepath: str) -> MapStructure:
        try:
            f = open(filepath, "r")
        except FileNotFoundError:
            raise ParsingError(
                f"Error: File not found — '{filepath}'"
            )
        except PermissionError:
            raise ParsingError(
                f"Error: Permission denied when reading '{filepath}'"
            )

        with f:
            for line_num, line in enumerate(f, start=1):
                self.line_num = line_num

                line = line.strip()
                if '#' in line:
                    line = line.split('#', 1)[0].strip()
                if not line:
                    continue

                if not self.parsed_drones:
                    if not line.startswith('nb_drones:'):
                        raise ParsingError(
                            f"[Line {self.line_num}] Error: "
                            f"'nb_drones:' must be the first meaningful line."
                        )
                    self._parse_nb_drones(line)
                    continue

                if line.startswith('nb_drones:'):
                    self._parse_nb_drones(line)

                elif line.startswith(('start_hub:', 'end_hub:', 'hub:')):
                    self._parse_hub_line(line)

                elif line.startswith('connection:'):
                    self._parse_connection_line(line)

                else:
                    raise ParsingError(
                        f"[Line {self.line_num}] Error: "
                        f"Unrecognized line — '{line}'."
                    )

        if not self.parsed_drones:
            raise ParsingError(
                "Error: File is empty or contains only comments."
            )
        if self.map.start_hub is None:
            raise ParsingError(
                "Error: No 'start_hub' defined in the map."
            )
        if self.map.end_hub is None:
            raise ParsingError(
                "Error: No 'end_hub' defined in the map."
            )

        return self.map


def map_parser(filepath: str) -> MapStructure:
    return MapParser().parse(filepath)

def main():
    try:
        map_parser("map.txt")
        print("Everything works perfectly!")
    except ParsingError as e:
        print(e)

if __name__ == "__main__":
    main()

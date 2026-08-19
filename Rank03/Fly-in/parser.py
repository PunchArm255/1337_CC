# parser.py - reads and validates the map input file
import re
from data import MapStructure, Zone, Connection


class ParsingError(Exception):
    """Custom exception raised for map parsing and validation errors."""

    pass


class MapParser:
    """Stateful parser that reads a map file and produces a MapStructure."""

    def __init__(self) -> None:
        self.map = MapStructure()
        self.line_num = 0
        # state trackers to enforce ordering: drones -> zones -> connections
        self.parsed_drones = False
        self.connections_started = False
        # frozenset to detect duplicate connections like A-B and B-A
        self.seen_connections: set[frozenset[str]] = set()

    def _parse_metadata(self, line: str) -> dict[str, str]:
        """Extracts key=value pairs from the [...] metadata block.

        Args:
            line: Raw input line containing optional metadata.

        Returns:
            Dictionary of parsed key-value metadata pairs.
        """
        result = re.search(r" \[(.*?)\]$", line)
        if not result:
            return {}  # metadata is optional

        # split on whitespace to extract key=value pairs
        pairs = result.group(1).split()
        metadata: dict[str, str] = {}

        for p in pairs:
            if "=" not in p:
                raise ParsingError(
                    f"[Line {self.line_num}] Error: "
                    f"Invalid metadata format '{p}'. Expected 'key=value'."
                )
            k, v = p.split("=", 1)
            if not k or not v:
                raise ParsingError(
                    f"[Line {self.line_num}] Error: "
                    f"Metadata key or value cannot be empty in '{p}'."
                )
            if k in metadata:
                raise ParsingError(
                    f"[Line {self.line_num}] Error: "
                    f"Duplicate metadata key '{k}' found."
                )
            metadata[k] = v

        return metadata

    def _parse_nb_drones(self, line: str) -> None:
        """Parses the 'nb_drones: <number>' line.

        Args:
            line: Raw line containing the drone count definition.
        """
        if self.parsed_drones:
            raise ParsingError(
                f"[Line {self.line_num}] Error: "
                "'nb_drones:' defined multiple times!"
            )

        # extract number after colon
        nb_str = line.split(":", 1)[1].strip()

        try:
            nb_drones = int(nb_str)
            if nb_drones <= 0:
                raise ValueError
        except ValueError:
            raise ParsingError(
                f"[Line {self.line_num}] Error: "
                f"'nb_drones' must be a positive integer, got '{nb_str}'."
            )

        self.map.nb_drones = nb_drones
        self.parsed_drones = True

    def _parsed_hubs(self, line: str) -> None:
        """Parses a zone line: start_hub:, end_hub:, or hub:.

        Args:
            line: Raw line defining a zone and its metadata.
        """
        # zones must be defined before connections
        if self.connections_started:
            raise ParsingError(
                f"[Line {self.line_num}] Error: "
                "Zones must be defined before connections."
            )

        # strip out the metadata block to parse core elements
        core_line = re.sub(r" \[(.*?)\]$", "", line).strip()
        core_parts = core_line.split()

        if len(core_parts) != 4:
            raise ParsingError(
                f"[Line {self.line_num}] Error: "
                "Invalid zone format. Expected: <type>: <name> <x> <y>."
            )

        prefix, name, x_str, y_str = core_parts

        if prefix not in ("start_hub:", "end_hub:", "hub:"):
            raise ParsingError(
                f"[Line {self.line_num}] Error: "
                f"Invalid zone prefix '{prefix}'."
            )

        # zone names cannot contain dashes because connections use dashes
        if "-" in name:
            raise ParsingError(
                f"[Line {self.line_num}] Error: "
                f"Zone name '{name}' cannot contain a dash."
            )

        # all zone names must be unique
        if name in self.map.zones:
            raise ParsingError(
                f"[Line {self.line_num}] Error: "
                f"Duplicate zone name '{name}'."
            )

        try:
            x, y = int(x_str), int(y_str)
        except ValueError:
            raise ParsingError(
                f"[Line {self.line_num}] Error: "
                f"Coordinates must be integers. Got x='{x_str}', y='{y_str}'."
            )

        metadata = self._parse_metadata(line)
        allowed_zone_keys = {"zone", "max_drones", "color"}
        for k in metadata:
            if k not in allowed_zone_keys:
                raise ParsingError(
                    f"[Line {self.line_num}] Error: "
                    f"Unknown metadata key '{k}' for a zone."
                    f"\n- Allowed keys: 'zone', 'max_drones', 'color'."
                )

        # ignore max_drones on start_hub and end_hub per subject update
        if prefix in ("start_hub:", "end_hub:"):
            metadata.pop("max_drones", None)

        z_type = metadata.get("zone", "normal")
        if z_type not in ["normal", "blocked", "restricted", "priority"]:
            raise ParsingError(
                f"[Line {self.line_num}] Error: "
                f"Invalid zone type '{z_type}'."
            )

        # start_hub and end_hub cannot be blocked
        if prefix in ("start_hub:", "end_hub:") and z_type == "blocked":
            raise ParsingError(
                f"[Line {self.line_num}] Error: "
                f"start/end hubs cannot be defined as blocked zones."
            )

        try:
            max_drones = int(metadata.get("max_drones", "1"))
            if max_drones <= 0:
                raise ValueError
        except ValueError:
            raise ParsingError(
                f"[Line {self.line_num}] Error: "
                "'max_drones' must be a positive integer."
            )

        # exactly one start and one end hub allowed
        if prefix == "start_hub:" and self.map.start_hub is not None:
            raise ParsingError(
                f"[Line {self.line_num}] Error: "
                "Multiple 'start_hub' definitions!"
            )
        if prefix == "end_hub:" and self.map.end_hub is not None:
            raise ParsingError(
                f"[Line {self.line_num}] Error: "
                "Multiple 'end_hub' definitions!"
            )

        new_zone = Zone(name, x, y, z_type, max_drones, metadata.get("color"))
        self.map.zones[name] = new_zone

        if prefix == "start_hub:":
            self.map.start_hub = new_zone
        elif prefix == "end_hub:":
            self.map.end_hub = new_zone

    def _parse_connections(self, line: str) -> None:
        """Parses a connection line: connection: <zone1>-<zone2> [metadata].

        Args:
            line: Raw line defining a connection between two zones.
        """
        self.connections_started = True

        core_line = re.sub(r" \[(.*?)\]$", "", line).strip()
        core_parts = core_line.split()

        if len(core_parts) != 2 or core_parts[0] != "connection:":
            raise ParsingError(
                f"[Line {self.line_num}] Error: "
                "Invalid format. Expected: connection: <zone1>-<zone2>"
            )

        connection_str = core_parts[1]

        if connection_str.count("-") != 1:
            raise ParsingError(
                f"[Line {self.line_num}] Error: "
                "Connection must contain exactly one dash."
            )

        zone1, zone2 = connection_str.split("-")

        if zone1 == zone2:
            raise ParsingError(
                f"[Line {self.line_num}] Error: "
                "A zone cannot connect to itself."
            )

        # both zones must already be defined
        if zone1 not in self.map.zones or zone2 not in self.map.zones:
            raise ParsingError(
                f"[Line {self.line_num}] Error: "
                "Connection refers to an undefined zone."
            )

        # frozenset treats A-B and B-A as the exact same connection
        connection_pair = frozenset({zone1, zone2})
        if connection_pair in self.seen_connections:
            raise ParsingError(
                f"[Line {self.line_num}] Error: "
                f"Duplicate connection '{zone1}-{zone2}'."
            )
        self.seen_connections.add(connection_pair)

        metadata = self._parse_metadata(line)
        allowed_cnx_keys = {"max_link_capacity"}
        for k in metadata:
            if k not in allowed_cnx_keys:
                raise ParsingError(
                    f"[Line {self.line_num}] Error: "
                    f"Unknown metadata key '{k}' for a connection."
                    f"\n- Allowed key: 'max_link_capacity'."
                )
        try:
            max_link = int(metadata.get("max_link_capacity", "1"))
            if max_link <= 0:
                raise ValueError
        except ValueError:
            raise ParsingError(
                f"[Line {self.line_num}] Error: "
                "'max_link_capacity' must be a positive integer."
            )

        self.map.connections.append(Connection(zone1, zone2, max_link))

    def parse(self, filepath: str) -> MapStructure:
        """Reads and parses a map file into a validated MapStructure.

        Args:
            filepath: Path to the input map file.

        Returns:
            The parsed and validated MapStructure object.
        """
        try:
            with open(filepath, "r") as f:
                for line_num, line in enumerate(f, start=1):
                    self.line_num = line_num
                    line = line.strip()

                    # ignore comments
                    if "#" in line:
                        line = line.split("#", 1)[0].strip()
                    if not line:
                        continue

                    # first non-empty line must be nb_drones
                    if (
                        not self.parsed_drones
                        and not line.startswith("nb_drones:")
                    ):
                        raise ParsingError(
                            f"[Line {self.line_num}] Error: "
                            "'nb_drones:' must be the first line."
                        )

                    # dispatch line according to its prefix
                    if line.startswith("nb_drones:"):
                        self._parse_nb_drones(line)
                    elif line.startswith(("start_hub:", "end_hub:", "hub:")):
                        self._parsed_hubs(line)
                    elif line.startswith("connection:"):
                        self._parse_connections(line)
                    else:
                        raise ParsingError(
                            f"[Line {self.line_num}] Error: "
                            "Unrecognized line syntax."
                        )

        except FileNotFoundError:
            raise ParsingError(f"Error: Could not find map at '{filepath}'")
        except PermissionError:
            raise ParsingError(f"Error: Read permission denied '{filepath}'")

        if not self.parsed_drones:
            raise ParsingError("Error: Map file empty or missing config.")
        if self.map.start_hub is None or self.map.end_hub is None:
            raise ParsingError(
                "Error: Map must contain exactly one 'start_hub' "
                "and one 'end_hub'."
            )
        return self.map


def map_parser(filepath: str) -> MapStructure:
    """Convenience wrapper to parse a map file in one call.

    Args:
        filepath: Path to the map file to parse.

    Returns:
        The parsed MapStructure.
    """
    return MapParser().parse(filepath)


if __name__ == "__main__":
    try:
        parsed_map = map_parser("map.txt")
        print(
            "Parsed successfully:",
            len(parsed_map.zones),
            "zones found."
        )
    except ParsingError as e:
        print(e)

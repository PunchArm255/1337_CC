# parser.py — reads a map file and builds a MapStructure from it
#
# the map format is defined by the fly-in subject. this parser reads
# it line by line, validates everything, and builds up a MapStructure
# that the rest of the program uses. it's strict on purpose — any
# bad input gets caught here with a clear error message.
#
# parsing order enforced by the subject:
#   1. nb_drones must come first
#   2. zones (start_hub, end_hub, hub) must all be defined before connections
#   3. connections reference zones by name, so zones must exist first
#
# ref: https://docs.python.org/3/library/re.html (regex for metadata parsing)
# ref: https://docs.python.org/3/library/functions.html#enumerate (line numbering)

import re
from data import MapStructure, Zone, Connection


class ParsingError(Exception):
    """custom exception for parser errors so we can catch them specifically."""
    pass


class MapParser:
    """stateful parser that reads a map file and produces a MapStructure.

    it's stateful because it tracks things like "have we seen nb_drones yet?"
    and "have connections started?" across multiple lines. each line gets
    dispatched to the right handler based on its prefix.
    """

    def __init__(self) -> None:
        self.map = MapStructure()
        self.line_num = 0
        # state trackers — these enforce the ordering rules
        self.parsed_drones = False      # have we seen nb_drones yet?
        self.connections_started = False  # have we started parsing connections?
        # frozenset to check for duplicate connections like A-B and B-A
        self.seen_connections: set[frozenset[str]] = set()

    def _parse_metadata(self, line: str) -> dict[str, str]:
        """extracts key=value pairs from the [...] block in a line.

        example: "[zone=restricted color=red max_drones=2]"
        returns: {"zone": "restricted", "color": "red", "max_drones": "2"}

        if there's no [...] block, returns empty dict (metadata is optional).
        all values come back as strings — the caller converts them as needed.
        """
        # finding the first '[' and extracting metadata until the first ']'
        result = re.search(r"\[(.*?)\]", line)
        if not result:
            return {}  # no metadata found

        # split on whitespace to get individual key=value pairs
        pairs = result.group(1).split()
        metadata = {}

        for p in pairs:
            if '=' not in p:
                raise ParsingError(
                    f"[Line {self.line_num}] Error: "
                    f"Invalid metadata format '{p}'. Expected 'key=value'."
                )
            # split on first '=' only, in case the value contains '='
            k, v = p.split('=', 1)
            if not k or not v:
                raise ParsingError(
                    f"[Line {self.line_num}] Error: "
                    f"Metadata key or value cannot be empty in '{p}'."
                )
            metadata[k] = v

        return metadata

    def _parse_nb_drones(self, line: str) -> None:
        """parses the 'nb_drones: N' line.

        this must be the very first non-comment, non-empty line in the file.
        the number must be a positive integer (no zero, no negatives).
        """
        if self.parsed_drones:
            raise ParsingError(
                f"[Line {self.line_num}] Error: "
                "'nb_drones:' defined multiple times!"
            )

        # grab everything after the colon
        nb_str = line.split(':', 1)[1].strip()

        try:
            nb_drones = int(nb_str)
            if nb_drones <= 0:
                raise ValueError

        except ValueError:
            raise ParsingError(
                f"[Line {self.line_num}] Error: "
                f"'nb_drones must be a positive integer, got {nb_str}'"
            )

        self.map.nb_drones = nb_drones
        self.parsed_drones = True

    def _parsed_hubs(self, line: str) -> None:
        """parses a zone line: start_hub, end_hub, or regular hub.

        format: <type> <name> <x> <y> [metadata]
        the [...] metadata block is optional. this method handles all
        three zone types since they share the same format.
        """
        # zones must come before connections — the subject enforces this
        if self.connections_started:
            raise ParsingError(
                f"[Line {self.line_num}] Error: "
                 "Zones must be defined BEFORE connections."
            )

        # strip out the metadata block so we can cleanly split the core parts
        # e.g. "hub: roof1 3 4 [zone=restricted]" -> "hub: roof1 3 4"
        core_line = re.sub(r"\[.*?\]", "", line).strip()
        core_parts = core_line.split()

        # expecting exactly 4 parts: prefix, name, x, y
        if len(core_parts) != 4:
            raise ParsingError(
                f"[Line {self.line_num}] Error: "
                "Invalid zone format. Expected: <type> <name> <x> <y>."
            )

        prefix, name, x_str, y_str = core_parts

        # zone names can't have dashes because connections use dashes as separators
        if '-' in name:
            raise ParsingError(
                f"[Line {self.line_num}] Error: "
                f"Zone name '{name}' cannot contain a dash."
            )
        # every zone must have a unique name
        if name in self.map.zones:
            raise ParsingError(
                f"[Line {self.line_num}] Error: "
                f"Duplicate zone name '{name}'"
            )

        # coordinates must be valid integers
        try:
            x, y = int(x_str), int(y_str)
        except ValueError:
            raise ParsingError(
                f"[Line {self.line_num}] Error: "
                f"Coordinates must be integers. Got x='{x_str}', y='{y_str}'."
            )

        # extract and validate metadata
        metadata = self._parse_metadata(line)
        z_type = metadata.get("zone", "normal")

        if z_type not in ["normal", "blocked", "restricted", "priority"]:
            raise ParsingError(
                f"[Line {self.line_num}] Error: "
                f"Invalid zone type '{z_type}'."
            )

        try:
            max_drones = int(metadata.get("max_drones", "1"))
            if max_drones <= 0:
                raise ValueError
        except ValueError:
            raise ParsingError(
                f"[Line {self.line_num}] Error: "
                "'max_drones' must be a positive integer!"
            )

        # make sure we don't have duplicate start or end hubs
        if prefix == "start_hub:" and self.map.start_hub is not None:
            raise ParsingError(
                f"[Line {self.line_num}] Error: "
                "Multiple 'start_hub' definitions!"
            )
        if prefix == "end_hub" and self.map.end_hub is not None:
            raise ParsingError(
                f"[Line {self.line_num}] Error: "
                "Multiple 'end_hub' definitions!"
            )

        # create the zone and register it
        new_zone = Zone(name, x, y, z_type, max_drones, metadata.get("color"))
        self.map.zones[name] = new_zone

        # also set it as start or end hub if that's what the prefix says
        if prefix == 'start_hub:':
            self.map.start_hub = new_zone
        if prefix == 'end_hub:':
            self.map.end_hub = new_zone

    def _parse_connections(self, line: str) -> None:
        """parses a connection line: connection: <zone1>-<zone2> [metadata].

        connections are bidirectional. both zones must already be defined.
        duplicates (A-B and B-A count as the same) are rejected.
        """
        # once we start seeing connections, no more zones allowed
        self.connections_started = True

        # strip metadata block, same approach as zone parsing
        core_line = re.sub(r"\[.*?\]", "", line).strip()
        core_parts = core_line.split()

        if len(core_parts) != 2:
            raise ParsingError(
                f"[Line {self.line_num}] Error: "
                "Invalid format. Expected connection: <zone1>-<zone2>"
            )

        connection_str = core_parts[1]

        # exactly one dash expected — zone names can't contain dashes
        if connection_str.count('-') != 1:
            raise ParsingError(
                f"[Line {self.line_num}] Error: "
                "Connection must contain exactly one dash."
            )

        zone1, zone2 = connection_str.split('-')

        # self-loops make no sense for drone routing
        if zone1 == zone2:
            raise ParsingError(
                f"[Line {self.line_num}] Error: "
                "A zone cannot connect to itself."
            )

        # both zones must already be defined (zones come before connections)
        if zone1 not in self.map.zones or zone2 not in self.map.zones:
            raise ParsingError(
                f"[Line {self.line_num}] Error: "
                "Connection refers to an unidentified zone."
            )

        # check for duplicates using frozenset so A-B and B-A are the same
        connection_pair = frozenset({zone1, zone2})
        if connection_pair in self.seen_connections:
            raise ParsingError(
                f"[Line {self.line_num}] Error: "
                f"Duplicate connection '{zone1}-{zone2}.'"
            )
        self.seen_connections.add(connection_pair)

        # parse optional metadata (max_link_capacity)
        metadata = self._parse_metadata(line)
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
        """main entry point — reads a file and returns a validated MapStructure.

        goes through the file line by line, strips comments, and dispatches
        each line to the right handler. after all lines are parsed, does a
        final sanity check to make sure we have everything we need.
        """
        try:
            with open(filepath, "r") as f:
                for line_num, line in enumerate(f, start=1):
                    self.line_num = line_num
                    line = line.strip()

                    # strip inline comments (anything after #)
                    if '#' in line:
                        line = line.split('#', 1)[0].strip()
                    if not line:
                        continue

                    # nb_drones must be the very first real line
                    if not self.parsed_drones and not line.startswith("nb_drones:"):
                        raise ParsingError(
                            f"[Line {self.line_num}] Error: "
                            "'nb_drones' must be the first configuration line."
                        )

                    # dispatch to the right handler based on prefix
                    if line.startswith("nb_drones:"):
                        self._parse_nb_drones(line)
                    elif line.startswith(("start_hub", "end_hub", "hub")):
                        self._parsed_hubs(line)
                    elif line.startswith("connection"):
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

        # final validation — make sure we got everything we need
        if not self.parsed_drones:
            raise ParsingError("Error: Map file empty or missing config.")
        if self.map.start_hub is None or self.map.end_hub is None:
            raise ParsingError(
                "Error: Map must contain exactly one 'start_hub' "
                "and one 'end_hub'."
            )
        return self.map


# convenience function so you can just call map_parser("file.txt")
# instead of doing MapParser().parse("file.txt") everywhere
def map_parser(filepath: str) -> MapStructure:
    """shortcut to parse a map file in one call."""
    return MapParser().parse(filepath)


if __name__ == "__main__":
    try:
        parsed_map = map_parser("map.txt")
        print("Everything works perfectly! Found", len(parsed_map.zones), "zones.")
    except ParsingError as e:
        print(e)

import re
from data import MapStructure, Zone, Connection


class ParsingError(Exception):
    pass


class MapParser:
    def __init__(self) -> None:
        self.map = MapStructure()
        self.line_num = 0
        # state trackers
        self.parsed_drones = False
        self.connections_started = False
        # frozenset to check for duplicate connections
        self.seen_connections: set[frozenset[str]] = set()

    def _parse_metadata(self, line: str) -> dict[str, str]:
        # finding the first '[' and extracting metadata until the first ']'
        result = re.search(r"\[(.*?)\]", line)
        if not result:
            return {} # no metadata found

        pairs = result.group(1).split()
        metadata = {}

        for p in pairs:
            if '=' not in p:
                raise ParsingError(
                    f"[Line {self.line_num}] Error: "
                    f"Invalid metadata format '{p}'. Expected 'key=value'."
                )
            k, v = p.split('=', 1)
            if not k or not v:
                raise ParsingError(
                    f"[Line {self.line_num}] Error: "
                    f"Metadata key or value cannot be empty in '{p}'."
                )
            metadata[k] = v

        return metadata

    def _parse_nb_drones(self, line: str) -> None:
        if self.parsed_drones:
            raise ParsingError(
                f"[Line {self.line_num}] Error: "
                "'nb_drones:' defined multiple times!"
            )

        nb_str = line.split(':', 1)[1].strip()

        try:
            nb_drones = nb_str
            if nb_drones <= 0:
                raise ValueError

        except ValueError:
            raise ParsingError(
                f"[Line {self.line_num}] Error: "
                f"'nb_drones must be a positive integer, got {nb_str}'"
            )
        
        self.map.nb_drones = nb_drones
        self.parsed_drones = True

    def _parsed_hubs():
        pass

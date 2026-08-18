# data.py - data models for zones, connections, and maps
from dataclasses import dataclass, field


@dataclass
class Zone:
    """Represents a single zone in the drone network."""

    name: str
    x: int
    y: int
    zone_type: str = "normal"
    max_drones: int = 1
    color: str | None = None


@dataclass
class Connection:
    """Represents a bidirectional link between two zones."""

    zone1: str
    zone2: str
    max_link_capacity: int = 1


@dataclass
class MapStructure:
    """The complete parsed result of a map file."""

    nb_drones: int = 0
    start_hub: Zone | None = None
    end_hub: Zone | None = None
    # all zones indexed by name for quick lookup
    zones: dict[str, Zone] = field(default_factory=dict)
    # flat list of all connections in the map
    connections: list[Connection] = field(default_factory=list)

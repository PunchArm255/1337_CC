from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Zone:
    """represents a single zone in the drone network."""
    name: str
    x: int
    y: int
    zone_type: str = "normal"
    max_drones: int = 1
    color: Optional[str] = None


@dataclass
class Connection:
    """represents a bidirectional link between two zones."""
    zone1: str
    zone2: str
    max_link_capacity: int = 1


@dataclass
class MapStructure:
    """the complete parsed result of a map file."""
    nb_drones: int = 0
    start_hub: Optional[Zone] = None
    end_hub: Optional[Zone] = None
    zones: dict[str, Zone] = field(default_factory=dict)
    connections: list[Connection] = field(default_factory=list)

# data.py — the data structures that represent a parsed map
#
# these are just containers (dataclasses) that hold the raw info
# from the map file. they don't do any logic themselves — parser.py
# fills them in, and graph.py / pathfinder.py read from them.
#
# using dataclasses here because they auto-generate __init__, __repr__,
# and __eq__ for us. less boilerplate, same result as writing a class
# with a manual __init__.
#
# ref: https://docs.python.org/3/library/dataclasses.html

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Zone:
    """represents a single zone (node) in the drone network.

    every zone has a name, coordinates for visualization, a type that
    determines movement cost, a capacity limit, and an optional color.
    """
    name: str                          # unique identifier, no dashes allowed
    x: int                             # x coordinate (for visualization positioning)
    y: int                             # y coordinate (for visualization positioning)
    zone_type: str = "normal"          # one of: normal, blocked, restricted, priority
    max_drones: int = 1                # how many drones can occupy this zone at once
    color: Optional[str] = None        # optional display color from the map file


@dataclass
class Connection:
    """represents a bidirectional link (edge) between two zones.

    connections define where drones can fly between. they also have
    a capacity limit — how many drones can use this connection at
    the same time in a single turn.
    """
    zone1: str                         # name of the first zone
    zone2: str                         # name of the second zone
    max_link_capacity: int = 1         # max drones traversing this link per turn


@dataclass
class MapStructure:
    """the complete parsed result of a map file.

    this is what the parser builds up line by line and what gets
    passed to the graph constructor. it holds everything: drone count,
    start/end zones, all zones, and all connections.
    """
    nb_drones: int = 0                 # total number of drones to simulate
    start_hub: Optional[Zone] = None   # the starting zone (all drones begin here)
    end_hub: Optional[Zone] = None     # the goal zone (all drones must reach here)
    # dict keyed by zone name for O(1) lookup during parsing
    zones: dict[str, Zone] = field(default_factory=dict)
    # list of all connections (order doesn't matter, graph builds adjacency from this)
    connections: list[Connection] = field(default_factory=list)

from dataclasses import dataclass

@dataclass
class Edge:
    u: int
    v: int
    cost: int
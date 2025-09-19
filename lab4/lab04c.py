from collections.abc import Sequence
from dataclasses import dataclass

@dataclass
class Node:
    low: int
    high: int
    recip_res: float
    left: "Node | None" = None
    right: "Node | None" = None

    @property
    def is_leaf(self) -> bool:
        return self.high - self.low == 1
    
    @classmethod
    def make(cls, seq: list[int], i: int, j: int) -> "Node":
        if  j - i == 1:
            # a leaf node
            return cls(i, j, 1/seq[i])
        else:
            high_of_low: int = (i + j) // 2
            left_child: Node = cls.make(seq, i, high_of_low)
            right_child: Node = cls.make(seq, high_of_low, j)
            return cls(i, j, left_child.recip_res + right_child.recip_res, left_child, right_child)
    


class ParallelPencils:
    def __init__(self, lengths: Sequence[int]):
        ...
        super().__init__()


    def add_length(self, i: int, l: int) -> None:
        ...


    def get_resistance(self, i: int, j: int) -> float:
        ...

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
    
    def set(self, idx: int, val: float) -> None:
        if not (self.low <= idx < self.high):
            return
        elif self.is_leaf:
            self.recip_res = 1 / val
            return
        else:
            self.left.set(idx, val)
            self.right.set(idx, val)
            self.recip_res = self.left.recip_res + self.right.recip_res
            return
    
    def query(self, query_low: int, query_high: int) -> float:
        if query_low <= self.low and self.high <= query_high:
            return self.recip_res
        elif self.high <= query_low or query_high <= self.low:
            return 0
        else:
            return self.left.query(query_low, query_high) + self.right.query(query_low, query_high)
        
class ParallelPencils:
    def __init__(self, lengths: Sequence[int]):
        self.seq: list[int] = list(lengths)
        self.n: int = len(lengths)
        self.root: Node = Node.make(self.seq, 0, self.n)
        super().__init__()

    def add_length(self, i: int, l: int) -> None:
        self.seq[i] += l
        self.root.set(i, self.seq[i])

    def get_resistance(self, i: int, j: int) -> float:
        recip_sum: float = self.root.query(i, j)
        return 1/recip_sum if recip_sum > 0 else float('inf')

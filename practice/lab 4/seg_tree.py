from dataclasses import dataclass

@dataclass
class Node:
    low: int
    high: int
    val: int
    left: "Node | None" = None
    right: " Node | None" = None

    @classmethod
    def make(cls, seq: list[int], l: int, h: int):
        if h - l == 1:
            return cls(low=l, high=h, val=seq[l])
        else:
            high_of_left = (l + h) // 2
            l_child = cls.make(seq, l, high_of_left)
            r_child = cls.make(seq, high_of_left, h)
            return cls(low=l, high=h, val=min(l_child.val, r_child.val), left=l_child, right=r_child)
        
    @property
    def is_leaf(self):
        return self.high - self.low == 1
    
    def query(self, query_low, query_high):
        if query_low <= self.low and self.high <= query_high:
            return self.val
        elif query_high <= self.low and self.high <= query_low:
            return float('inf')
        else:
            l_ans = self.left.query(query_low, query_high)
            r_ans = self.right.query(query_low, query_high)
            return min(l_ans, r_ans)
    
    def set(self, idx, val):
        if not (self.left <= idx < self.right):
            return
        if self.is_leaf:
            self.val = val
        else:
            self.left.set(idx, val)
            self.right.set(idx, val)
            self.val = min(self.left.val, self.right.val)

class RangeMin:
    def __init__(self, seq):
        self.seq = seq
        self.n = len(seq)
        self.root = Node.make(seq, 0, self.n)
        super().__init__()

    def range_min(self, query_low, query_high):
        self.root.range_min(query_low, query_high)

    def __setitem__(self, idx, val):
        self.root.set(idx, val)
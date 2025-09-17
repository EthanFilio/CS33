from dataclasses import dataclass

@dataclass
class Node:
    low: int
    high: int
    val: int
    left: "Node | None" = None
    right: "Node | None" = None

    @classmethod
    def make(cls, seq, l, h):
        if h - l == 1:
            # leaf node already
            return cls(l, h, seq[l])
        else:
            high_of_left = (l + h) // 2
            l_child = cls.make(seq, l, high_of_left)
            r_child = cls.make(seq, high_of_left, h)
            return cls(l, h, min(l_child.val, r_child.val), l_child, r_child)
    
    @property
    def is_leaf(self):
        return self.high - self.low == 1
    
    def range_min(self, query_low, query_high):
        if query_low <= self.low and self.high <= query_high:
            return self.val
        elif self.high <= query_low or query_high <= self.low:
            return float('inf')
        else:
            return min(self.left.range_min(query_low, query_high), self.right.range_min(query_low, query_high))
        
    def set(self, idx, val):
        if not (self.low <= idx < self.high):
            return
        if self.is_leaf:
            self.val = val
        else:
            self.left.set(idx, val)
            self.right.set(idx, val)

class RangeMin:
    def __init__(self, seq):
        self.seq = seq
        self.n = len(seq)
        self.root = Node.make(seq, 0, self.n)
        super().__init__()
    
    def range_min(self, query_low, query_high):
        return self.root.range_min(query_low, query_high)
    
    def __setitem__(self, idx, val):
        self.root.set(idx, val)

n, q = map(int, input().split())
seq = list(map(int, input().split()))
r = RangeMin(seq)

for _ in range(q):
    q_low, q_high = map(int, input().split())
    print(f"{r.range_min(q_low - 1, q_high)}")


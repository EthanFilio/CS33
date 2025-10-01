class Node:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
        self.dist = 1 + (right.dist if right else 0)

def meld(a, b):
    if not a: return b
    if not b: return a
    if a.val < b.val:
        a, b = b, a

    new_right = meld(a.right, b)
    new_node = Node(a.val, a.left, new_right)

    if not new_node.left or (new_node.left.dist < new_node.right.dist):
        new_node.left, new_node.right = new_node.right, new_node.left
    new_node.dist = 1 + (new_node.right.dist if new_node.right else 0)
    
    return new_node

def insert(root, val):
    return meld(root, Node(val))


def pop(root):
    return meld(root.left, root.right) if root else None

class SugarHeap:
    def __init__(self):
        self.root = None
        self.offset = 0
        self.total_sum = 0
        self.size = 0
        self.history = [(self.root, self.offset, self.total_sum, self.size)]
        super().__init__()

    def push(self, s: int) -> None:
        self.root = insert(self.root, s - self.offset)
        self.total_sum += s
        self.size += 1
        self._save_state()

    def pop(self) -> int:
        max_val = self.root.val + self.offset
        self.root = pop(self.root)
        self.total_sum -= max_val
        self.size -= 1
        self._save_state()
        return max_val

    def sugar_sum(self) -> int:
        return self.total_sum

    def add_sugar(self, v: int) -> None:
        self.offset += v
        self.total_sum += v * self.size
        self._save_state()

    def time_travel(self, k: int) -> None:
        self.root, self.offset, self.total_sum, self.size = self.history[k]
        self._save_state()

    def _save_state(self):
        self.history.append((self.root, self.offset, self.total_sum, self.size))

sugar_heap = SugarHeap()
sugar_heap.push(1)
sugar_heap.push(2)
sugar_heap.add_sugar(1)
level = sugar_heap.pop()
assert level == 3
sugar_heap.time_travel(2)
assert sugar_heap.sugar_sum() == 3
